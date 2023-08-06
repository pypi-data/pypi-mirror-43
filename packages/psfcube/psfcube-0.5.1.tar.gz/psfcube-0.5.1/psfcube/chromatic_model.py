#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from propobject import BaseObject
LBDAREF = 7000

# ========================= #
#                           #
#  Chromaticity             #
#                           #
# ========================= #
def sigma_chromaticity(lbda, sigmaref, rho=-1/5., lbdaref=7000):
    """ Evolution of the standard deviation as a function of lbda. """
    return sigmaref * (lbda / lbdaref)**(rho)

#############################
#                           #
#   Classes                 #
#                           #
#############################
class ADRModel( BaseObject ):
    """ """
    PROPERTIES = ["adr","unit","xref","yref"]

    def __init__(self,  adr, xref, yref, unit=1):
        """ """
        self.set_adr(adr, xref, yref, unit=unit)
        
    # =================== #
    #  Methods            #
    # =================== #
    def get_centroid(self, lbda):
        """ """
        return self.adr.refract(self.xref, self.yref, lbda, unit=self.unit)
    
    def set_adr(self, adr, xref, yref, unit=1):
        """ """
        self._properties["adr"]  = adr
        self._properties["xref"] = xref
        self._properties["yref"] = yref
        self._properties["unit"] = unit
        
    # =================== #
    #  Property           #
    # =================== #
    @property
    def adr(self):
        """ """
        return self._properties["adr"]

    @property
    def unit(self):
        """ """
        return self._properties["unit"]

    @property
    def xref(self):
        """ """
        return self._properties["xref"]
    
    @property
    def yref(self):
        """ """
        return self._properties["yref"]


class ChromaticNormalMoffat( BaseObject ):
    """ """
    PROPERTIES = ["sigma","alpha", "eta","lbda",
                      "adrmodel"]

    # ==================== #
    #  Methods             #
    # ==================== #
    def force_fit(self, cube,
                      psfmodel="NormalMoffatCurved",
                      slice_width=None,
                      ell=None, xy=None,
                      ellerr=None, xyerr=None,
                      force_ellipse=True,
                      force_centroid=True,
                      force_sigma=True,force_alpha=True):
        """ 
        slice_width: [int/None]
            How may lbda-slices array do you combine.
            None=>1
            1 means, each slice individually
            2 means you stack 2 slices together (hence having a spectrum with only half the lbda-binning
            ...
        """
        from .fitter import fit_slice
        from astropy.stats import mad_std
        slpsf = {}
        # = Which wavelengths
        if slice_width is None or slice_width == 1:
            slice_width = None
            lbdas = cube.lbda
        elif slice_width<=0:
            raise ValueError("slice_width must be positive or None %d given"%slice_width)
        elif slice_width > 0:
            lbda_min,lbda_max = cube.lbda[::slice_width],cube.lbda[slice_width-1::slice_width]
            if len(lbda_min)>len(lbda_max):
                lbda_min = lbda_min[:len(lbda_max)]
            lbdas = np.mean([lbda_min,lbda_max], axis=0)

        sigma_lbdas = self.get_sigma(lbdas)

        # Moffat
        achromatic_moffat_alpha = self.get_moffat_alpha(False)
        eta = np.nanmean(self.eta)
        etaerr = mad_std(self.eta)*2
        profile_lbda = {"alpha_guess":achromatic_moffat_alpha[0],
                        "alpha_fixed": force_alpha,
                        "alpha_boundaries":[achromatic_moffat_alpha[0]-0.2,achromatic_moffat_alpha[0]+0.2],
                        "centroids_err":[0.05,0.05],
                        "force_centroid":force_centroid,
                        "sigma_fixed":force_sigma,
                        "eta_guess": np.nanmean(self.eta),
                        "eta_boundaries": [np.nanmax([0.1,eta-etaerr]), eta+etaerr]
                        }
        # Ellipse
        if ell is not None:
            profile_lbda["ell_guess"] = ell
            if ellerr is not None: profile_lbda["ell_boundaries"] = [ell-ellerr, ell+ellerr]
        if xy is not None:
            profile_lbda["xy_guess"] = xy
            if xyerr is not None: profile_lbda["xy_boundaries"] = [xy-xyerr, xy+xyerr]
                
        if ell is not None and xy is not None and force_ellipse:
            profile_lbda["ell_fixed"] = True
            profile_lbda["xy_fixed"]  = True
        # 
        # => All Slices
        #
        if slice_width is None:
            for i, l_ in enumerate(cube.lbda):
                profile_lbda["sigma_guess"]      = sigma_lbdas[i]
                profile_lbda["sigma_boundaries"] = [sigma_lbdas[i]-0.1,sigma_lbdas[i]+0.1]
                # Centroid
                profile_lbda["centroids"]      = self.get_position(l_)
                if i%40 == 0:
                    print(i,"/",len(cube.lbda))
                slpsf[i] = fit_slice(cube.get_slice(index=i, slice_object=True),
                                        psfmodel=psfmodel, **profile_lbda)
        # 
        # => Meta Slices
        #
        else:
            for i, l_ in  enumerate(zip(lbda_min,lbda_max)):
                profile_lbda["sigma_guess"]      = sigma_lbdas[i]
                profile_lbda["sigma_boundaries"] = [sigma_lbdas[i]-0.1,sigma_lbdas[i]+0.1]
                # Centroid
                profile_lbda["centroids"]      = self.get_position(np.mean(l_))
                if i%10 == 0:
                    print(i,"/",len(lbdas))
                slpsf[i] = fit_slice(cube.get_slice(lbda_min=l_[0],lbda_max=l_[1], slice_object=True),
                                        psfmodel=psfmodel, **profile_lbda)
        return slpsf
    
    
    # -------- #
    #  GETTER  #
    # -------- #
    def get_position(self, lbda):
        """ """
        return self.adrmodel.get_centroid(lbda)
    
    def get_sigma(self, lbda, lbdaref=LBDAREF):
        """ """
        sigmaref, rho = self.fit_sigma_parameters()
        return sigma_chromaticity(lbda, sigmaref, rho=rho, lbdaref=lbdaref)
    
    def get_moffat_alpha(self, weighted_mean=True):
        """ """
        if weighted_mean and self.alpha_err is not None:
            flagin = ~np.isnan(self.alpha*self.alpha_err)
            return np.average(self.alpha[flagin], weights=1/self.alpha_err[flagin]**2), np.nanstd(self.alpha)/ np.sqrt(self.ndata)
        
        return np.nanmean(self.alpha), np.nanstd(self.alpha)/ np.sqrt(self.ndata)
    
    # -------- #
    #  SETTER  #
    # -------- #
    def set_adrmodel(self, adrmodel):
        """ """
        self._properties["adrmodel"] = adrmodel

        
    def set_data(self, sigma, alpha, eta, lbda,
                     sigma_err=None, alpha_err=None, eta_err=None):
        """ """
        self._properties["sigma"]              = sigma
        self._properties["alpha"]               = alpha
        self._properties["eta"]     = eta
        self._properties["sigma_err"]          = sigma_err
        self._properties["alpha_err"]           = alpha_err
        self._properties["eta_err"] = eta_err
        
        self._properties["lbda"]            = lbda

    # --------- #
    #  FITTER   #
    # --------- #
    def fit_sigma_parameters(self, adjust_errors=True, intrinsic=0):
        """ """
        from scipy.optimize import minimize
        sigma_err = self.sigma_err if self.sigma_err is not None else 1.
        if intrinsic>0: sigma_err = np.sqrt(sigma_err**2 + intrinsic**2)
        
        def _fmin_(param): 
            return np.nansum( np.sqrt((self.sigma-sigma_chromaticity(self.lbda, *param))**2/sigma_err**2))

        res  = minimize(_fmin_, [np.nanmedian(self.sigma), -1/5.], bounds=[[0.5,10], [-1,1]], options={"disp":0})
        if self.sigma_err is not None:
            chi2_dof = res["fun"] / len(self.sigma-2)
            if chi2_dof>3 and adjust_errors:
                print("Adjusting error")
                from pysedm.utils.tools import fit_intrinsic
                intrinsic = fit_intrinsic(self.sigma, sigma_chromaticity(self.lbda, *res["x"]), self.sigma_err, len(self.sigma-2), intrinsic_guess=None)
                return self.fit_sigma_parameters( adjust_errors=False, intrinsic = intrinsic/1.4)
        
        return res["x"]
    
    # ==================== #
    #  Properties          #
    # ==================== #
    
    # - PSF Properties
    @property
    def sigma(self):
        """ """
        return self._properties["sigma"]

    @property
    def alpha(self):
        """ """
        return self._properties["alpha"]

    @property
    def eta(self):
        """ """
        return self._properties["eta"]

    @property
    def sigma_err(self):
        """ """
        return self._properties["sigma_err"]

    @property
    def alpha_err(self):
        """ """
        return self._properties["alpha_err"]

    @property
    def eta_err(self):
        """ """
        return self._properties["eta_err"]
    
    
    @property
    def lbda(self):
        """ """
        return self._properties["lbda"]

    @property
    def ndata(self):
        """ """
        return len(self.lbda)

    @property
    def adrmodel(self):
        """ """
        return self._properties["adrmodel"]
