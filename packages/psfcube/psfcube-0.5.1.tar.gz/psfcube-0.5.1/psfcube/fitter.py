#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as mpl
import warnings

from propobject import BaseObject

from modefit.baseobjects import BaseFitter

from .model import read_psfmodel
from .chromatic_model import sigma_chromaticity
from .tools import kwargs_update
from .chromatic_model import LBDAREF

FITKEY  = "slpsf"
USE_LEASTSQ = True


def fit_slice(slice_, fitbuffer=None,
              psfmodel="NormalMoffatTilted", fitted_indexes=None,
              lbda=None, centroids=None, centroids_err=[2,2],
              adjust_errors=True, force_centroid=False,
              **kwargs):
    """ Fit PSF Slice without forcing it's shape

    Parameters
    ----------

    Returns
    -------
    SlicePSF
    """
    from .tools import kwargs_update
    slpsf = SlicePSF(slice_, psfmodel=psfmodel,
                    fitbuffer=fitbuffer, fitted_indexes=fitted_indexes)

    
    if centroids is None:
        xcentroid, ycentroid = None, None
    elif len(centroids) !=2:
        raise TypeError("given centroid should be None or [x,y]")
    else:
        xcentroid, ycentroid = centroids

    # - Fitting 
    fit_default = slpsf.get_guesses(xcentroid=xcentroid,            ycentroid=ycentroid,
                                    xcentroid_err=centroids_err[0], ycentroid_err=centroids_err[1])
    if force_centroid:
        fit_default["xcentroid_fixed"] = True
        fit_default["ycentroid_fixed"] = True

    fit_parameters = kwargs_update(fit_default, **kwargs)
    slpsf.fit( **fit_parameters )
    # - Fitting
    
    dof = slpsf.npoints - slpsf.model.nparam
    if slpsf.fitvalues["chi2"] / dof>2 and adjust_errors and not USE_LEASTSQ:
        from .tools import fit_intrinsic
        model = slpsf.model.get_model(slpsf._xfitted, slpsf._yfitted)
        intrinsic = fit_intrinsic(slpsf._datafitted, model, slpsf._errorfitted, dof, intrinsic_guess=None)
        slpsf.set_intrinsic_error(intrinsic / np.sqrt(2) )
        slpsf.fit( **fit_parameters )
    
    return slpsf



def header_to_adr_param(header_, no_end_para_bounds=270, end_para_bounds=10):
    """ Function that reads the header trying to find the parallactic angle and airmass information. 
    Returns:
    {parangle_guess:VALUE, parangle_boundaries:[VALUE,VALUE],
     airmass_guess: VALUE,  airmass_boundaries:[VALUE,VALUE]}

    """
    dict_out = {}
    #
    # Paralactic angle
    #
    start_para_key = [k for k in header_.keys() if k in ["TEL_PA", "PARANGL","PA"]]
    start_para_key = None if len(start_para_key) == 0 else start_para_key[0]
    try:
        start_para = float(header_[start_para_key])
        if start_para<-360: # Values meaning no information, like -999
            start_para_key = None
    except:
        start_para_key = None
        
    end_para_key = [k for k in header_.keys() if k in ["END_PA", "PA_END"]]
    end_para_key = None if len(end_para_key) == 0 else end_para_key[0]
    try:
        end_para  = float(header_[end_para_key])
        if end_para<-360: # Values meaning no information, like -999
            end_para_key = None
    except:
        end_para_key = None
        
    if start_para_key is None:
        warnings.warn("Cannot find a parangle_guess, no TEL_PA in the header. parangle_guess set to 0")
        dict_out["parangle_guess"] = 0
        dict_out["parangle_boundaries"] = [-270,270]
    elif end_para_key is None:
        dict_out["parangle_guess"] = start_para+10
        dict_out["parangle_boundaries"] = [start_para-no_end_para_bounds,start_para+no_end_para_bounds]
    else:
        dict_out["parangle_guess"] = np.mean([start_para,end_para])
        dict_out["parangle_boundaries"] = (np.sort([start_para,end_para])+ [-20,20]).tolist() # buffer to avoid issue with end_para== start_para

    #
    # AIRMASS
    #
    start_airmass_key = [k for k in header_.keys() if k in ["TEL_AIR", "TELAIR", "AIRMASS","TEL_Z"]]
    start_airmass_key = None if len(start_airmass_key) == 0 else start_airmass_key[0]
    try:
        start_airmass = float(header_[start_airmass_key])
        if start_airmass<0: # Values meaning no information, like -999
            start_airmass_key = None
    except:
        start_airmass_key = None
        
    end_airmass_key = [k for k in header_.keys() if k in ["END_AIR", "ENDAIR","AIREND","ENDZ","END_Z"]]
    end_airmass_key = None if len(end_airmass_key) == 0 else end_airmass_key[0]
    try:
        end_airmass  = float(header_[end_airmass_key])
        if end_airmass<0: # Values meaning no information, like -999
            end_airmass_key = None
    except:
        end_airmass_key = None
        
    if start_airmass_key is None:
        warnings.warn("Cannot find a parangle_guess, no TEL_PA in the header. parangle_guess set to 0")
        dict_out["airmass_guess"] = 1.2
        dict_out["airmass_boundaries"] = [1.00005,3]
    elif end_airmass_key is None:
        dict_out["airmass_guess"] = start_airmass+0.2
        dict_out["airmass_boundaries"] = [1.00005,start_airmass*1.5]
    else:
        dict_out["airmass_guess"] = np.mean([start_airmass,end_airmass])
        dict_out["airmass_boundaries"] = np.sort([start_airmass,end_airmass])
    
    return dict_out
# ====================== #
#                        #
#    PSF Classes         #
#                        #
# ====================== #
class SlicePSFCollection( BaseObject ):
    """ """
    PROPERTIES = ["slices","cube"]
    DERIVED_PROPERTIES = ["adrfitter"]


    def __init__(self, cube=None):
        """ """
        if cube is not None:
            self.set_cube(cube)
            
    # =================== #
    #   Methods           #
    # =================== #
    # --------- #
    #  GETTER   # 
    # --------- #

    # = Models
    def get_chromatic_profile_model(self):
        """ """
        from . import chromatic_model
        cmodel = chromatic_model.ChromaticNormalMoffat()
        used_slindexes  =  self.slindexes[~self.fetch_outlier()]
        cmodel.set_data( *[self.get_fitted_value(k, slindexes=used_slindexes)
                               for k in ["sigma","alpha","eta","lbda",
                                          "sigma.err","alpha.err","eta.err"] ] )
        
        adrmodel = chromatic_model.ADRModel(self.adrfitter.model.adr, 
                                            self.adrfitter.fitvalues["xref"], self.adrfitter.fitvalues["yref"], 
                                            unit=self.adrfitter.model._unit
                                            )
        cmodel.set_adrmodel(adrmodel)
        return cmodel
        
    # = fetch Outlier
    def fetch_outlier(self, used_slindexes=None, fitkey=FITKEY, ell_exclusion_to_zero=0.05):
        """ """
        from astropy.stats import mad_std
        ell    = self.get_fitted_value("ell",        slindexes=used_slindexes, fitkey=fitkey)
        ellerr = self.get_fitted_value("ell.err",        slindexes=used_slindexes, fitkey=fitkey)
        xy  = self.get_fitted_value("xy" ,     slindexes=used_slindexes, fitkey=fitkey)
        xyerr = self.get_fitted_value("xy.err",        slindexes=used_slindexes, fitkey=fitkey)
        # Excluded because boundaries
        flag = np.asarray(( np.abs(ell-np.nanmedian(ell))>mad_std(ell[ell==ell])*4 ) + ( np.abs(xy-np.nanmedian(xy))>mad_std(xy[xy==xy])*4),
                              dtype="bool")

        if np.all(flag):
            print("ALL slices have been considered as outlier... set all of them as non-outlier")
            return ~flag
        return flag

        
    # = Get Fitted Parameters
    def get_ellipse_parameters(self, used_slindexes=None, fitkey=FITKEY, exclusion_to_zero=0.05):
        """ estimate the (achromatic) elliptical parameter 

        Returns
        -------
        [mean_ell, mean_ell.err [nMAD], mean_xy, mean_xy.err [nMAD]], mask_removed (True =removed)
        """
        from astropy.stats import mad_std
        if used_slindexes is None:
            used_slindexes = self.slindexes[~self.fetch_outlier()]
            
        ell    = self.get_fitted_value("ell",        slindexes=used_slindexes, fitkey=fitkey)
        xy  = self.get_fitted_value("xy" ,     slindexes=used_slindexes, fitkey=fitkey)

        
        # Excluded because boundaries
        return  [np.average(ell), mad_std(ell)/np.sqrt(len(ell)-1),
                     np.average(xy), mad_std(xy)]
        
    def get_sigma_ratio(self, used_slindexes=None, fitkey=FITKEY):
        """ """
        from astropy.stats import mad_std
        if used_slindexes is None:
            used_slindexes = self.slindexes[~self.fetch_outlier()]
            
        sigma_ratio    = self.get_fitted_value("sigma_ratio",  slindexes=used_slindexes, fitkey=fitkey)
        return np.nanmean(sigma_ratio), mad_std(sigma_ratio)

    def get_amplitude_ratio(self, used_slindexes=None, fitkey=FITKEY):
        """ """
        from astropy.stats import mad_std
        if used_slindexes is None:
            used_slindexes = self.slindexes[~self.fetch_outlier()]
            

        amplitude_ratio    = self.get_fitted_value("amplitude_ratio",  slindexes=used_slindexes, fitkey=fitkey)
        return np.nanmean(amplitude_ratio), mad_std(amplitude_ratio)

    def get_sigma_parameters(self, used_slindexes=None, fitkey=FITKEY, adjust_errors=True, intrinsic=0):
        """ """
        if used_slindexes is None:
            used_slindexes = self.slindexes[~self.fetch_outlier()]
            
        from scipy.optimize import minimize
        lbdas      = self.get_fitted_value("lbda",        slindexes=used_slindexes, fitkey=fitkey)
        sigma     = self.get_fitted_value("sigma",      slindexes=used_slindexes, fitkey=fitkey)
        sigma_err = self.get_fitted_value("sigma.err",  slindexes=used_slindexes, fitkey=fitkey)
        if intrinsic>0: sigma_err = np.sqrt(sigma_err**2 + intrinsic**2)
            
        def _fmin_(param):
            return np.nansum( np.sqrt((sigma-sigma_chromaticity(lbdas, *param))**2/sigma_err**2))

        
        res  = minimize(_fmin_, [np.nanmedian(sigma), -1/5.], bounds=[[0.5,10], [-1,1]], options={"disp":0})
        chi2_dof = res["fun"] / len(sigma-2)
        if chi2_dof>3 and adjust_errors:
            print("Adjusting error")
            from pysedm.utils.tools import fit_intrinsic
            intrinsic = fit_intrinsic(sigma, sigma_chromaticity(lbdas, *res["x"]), sigma_err, len(sigma-2), intrinsic_guess=None)
            return self.get_sigma_parameters( used_slindexes=used_slindexes, fitkey=fitkey, adjust_errors=False,
                                        intrinsic = intrinsic/1.4)
        
        return res["x"]
    
    # Generic
    def get_fitted_value(self, key, slindexes=None, fitkey=FITKEY):
        """ Once the slices has been fitted and recorded, get their fitvalues parameters. 
        
        Parameters
        ----------
        key: [string]
            which `fitvalues` key do you want? (e.g. xcentroid, ell, ...)

        slindexes: [None or list] -optional-
            for which fitted slices do you want that key?
            If None, all the slices wil be used using the self.slindexes property.

        fitkey: [string] -optional-
            Using which key does the `SlicePSF` object created using `fit_slice()` method has been stored.
            [do not change if you don't know]

        Returns
        -------
        1d-array
        """
        if slindexes is None:
            slindexes = self.slindexes
            
        # - Special case, LBDA
        if key in ["lbda","lbdas", "lbdarange"]:
            v = np.asarray([ self.slices[slindex]["lbdarange"] for slindex in slindexes ])
            if key in ["lbda","lbdas"]:
                return np.mean(v, axis=1)
            return v
        
        return np.asarray([self.slices[slindex][fitkey].fitvalues[key] for slindex in slindexes])
    
    # --------- #
    #  SETTER   # 
    # --------- #
    def set_cube(self, cube):
        """ attach a cube to this attribute. """
        self._properties['cube'] = cube

    def load_adrfitter(self, spaxel_unit=1, base_parangle=0):
        """ load the ADRfitter method using the cube's adr.
        This methods need to have the cube loaded (see set_cube())
        """
        from pyifu import adrfit
        if self.cube.adr is None: self.cube.load_adr()
        self._derived_properties['adrfitter'] = adrfit.ADRFitter(self.cube.adr.copy(),
                                                        base_parangle=base_parangle, unit=spaxel_unit)

    def extract_slice(self, slindex, lbda_min=None, lbda_max=None, lbdaindex=None,
                          overwrite=False):
        """ extract a slice from the cube and attach it to the current instance 
        using the index 'slindex'

        = Here level method of `add_slice` = 

        Parameters
        ----------
        slindex: [string/float] 
            Name of the slice. You will recover the extracted slice as self.slices[`slindex`]

        // Slice definition

        lbda_min, lbda_max: [float/None] -optional-
            lower and upper wavelength boundaries [in Angstrom] defining the slice.
            [one of these or lbdaindex must be given]
            
        lbdaindex: [int/None] -optional-
            If you want the slice to be a single wavelength, provide it's index.
            [if this is given, lbda_min, lbda_max are ignored]

        // other
        
        overwrite: [bool] -optional-
            If the slice `slindex` already exists, should this extraction overwrite it?
            
        Returns
        -------
        Void
        """
        if lbda_min is None and lbda_max is None and lbdaindex is None:
            raise ValueError("You need to provide at least one of lbda_min, lbda_max or lbdaindex")

        if lbdaindex is not None:
            lbdarange= [self.cube.lbda[lbdaindex],self.cube.lbda[lbdaindex]]
        else:
            lbdarange = [lbda_min if lbda_min is not None else self.cube.lbda[0],
                         lbda_max if lbda_max is not None else self.cube.lbda[-1]]
                
        # The Slice
        slice_ = self.cube.get_slice(lbda_min=lbda_min, lbda_max=lbda_max,
                                         index=lbdaindex, usemean=True, data='data',
                                         slice_object=True)
        if np.isnan(np.sum(slice_.data)):
            print("psfcube.fitter.py EXTRACT_SLICE: NaN ")
        # - add it
        self.add_slice(slice_, slindex, lbdarange, overwrite=overwrite)

    def add_slice(self, slice_, slindex, lbdarange=None, overwrite=False):
        """ add a new slice to this instance.
    
        The added slice will be accessible as follows:
        ```python
        self.slices[`slindex`] = { 'slice': `slice_`, 'lbdarange': `lbdarange` }
        ```

        Parameters
        ----------
        slice_: [pyifu's Slice]
            The Slice you want to add
            
        slindex: [string/float]
            Name of the slice. You will recover the given  slice as self.slices[`slindex`]

        lbdarange: [float/float] -optional-
            the wavelength range for the slice. This is not mandatory but you should.
            
        // other
        
        overwrite: [bool] -optional-
            If the slice `slindex` already exists, should this extraction overwrite it?
        
        Returns
        -------
        Void
        """
        if slindex in self.slices and not overwrite:
            raise ValueError("slice %d already exists"%slindex)
        
        self.slices[slindex] = {'slice':slice_, 'lbdarange':lbdarange}

    # --------- #
    #  FITTER   # 
    # --------- #    
    # - PSF Slice fitter
    def fit_slice(self, slindex, psfmodel="NormalMoffatTilted",
                    centroids=None, centroids_err=[2,2],
                    adjust_errors=True,
                    fitkey=FITKEY, **kwargs):
        """ fit a PSF on a slice using the fit_slice() function

        Parameters
        ----------
        slindex: [string/float]
            Name of the slice you want to fit.
        
        // PSF Fitting
        
        psfmodel: [string] -optional-
            Name of the model used to fit the PSF e.g.:
            - BiNormalFlat:    PSF + Constant      (1 background param)
            - BiNormalTilted:  PSF + Tilted plane  (3 background params)
            - BiNormalCurved:  PSF + Curved Plane  (5 background params)
        

        centroids: [None/[float,float]] -optional-
            To help the fit, would you have an idea of the PSF centroid?

        centroids_err: [float, float] -optional-
            What would be the -/+ error on you centroid position guess.
            = This is ignored if `centroids` is not provided.

        adjust_errors: [bool] -optional-
            Once the first fit has ran and if the chi2/dof is too high (>2), 
            shall this add an intrinsic dispersion to all points to get closer
            to a chi2/dof and then rerun the fit?
            = you should = 
            
        // other

        fitkey: [string/None] -optional-
            The returned SlicePSF object will be strored as `self.slices[`slindex`][`fitkey`] 
            except if fitkey is None.

        Returns
        -------
        SlicePSF [the object containing the psf fitting methods and results]
        """
        self._test_index_(slindex)
        slpsf = fit_slice(self.slices[slindex]['slice'], psfmodel=psfmodel,
                        centroids=centroids, centroids_err=centroids_err,
                        adjust_errors=adjust_errors, **kwargs)
        
        # - shall this be recorded
        if fitkey is not None:
            self.slices[slindex][fitkey] = slpsf
        
        return slpsf

    # - ADR fitter
    def fit_adr(self, used_slindexes=None, fitkey=FITKEY,
                    parangle=None, spaxel_unit=None, error_floor=0.02,
                    show=False, show_prop={},
                    ignore_upper_airmass=True,
                     **kwargs):
        """ Fits the adr parameters 

        [This method needs that you have fitted the slices using fit_slice() 
        and stored the results using `fitkey`]
        
        = This method uses pyifu.adrfit (see the load_adrfitter() method ) = 

        Parameters
        ----------
        used_slindexes: [None/list] -optional-
            list of slindex you want to use.
            If None, all the known slices will be used (`self.slindexes`)
            
        fitkey: [string/None] -optional-
            The returned SlicePSF object will be strored as `self.slices[`slindex`][`fitkey`] 
            except if fitkey is None.

        // fit
        spaxel_unit: [float] -optional-
            Size of the spaxels in arcsec. 
            (this parameter is not fitted as this is degenerated with the airmass)
            If not provided during the load_adrfitter, it is suggested that you set it here.

        parangle: [float] -optional-
            Initial guess for the paralactic angle added to the header's one.
            Note: **kwargs goes to `adrfitter.fit()` as modefit fit properties.
        
        error_floor: [float] -optional-
            Minimal error added to the centroid positions to avoid convergence issues
            
        ignore_upper_airmass: [bool] -optional-
            Ignore the upper airmass value. This could help the flexibility of the fit if the spaxel_unit is not
            perfectly known. 

        // other

        show: [bool] -optional-
            Shall this plot the results.
        
        show_prop: [dict] -optional-
            dictionary sent as kwargs for adrfitter.show(**show_prop)
            e.g.: {"ax":ax, "show":False}

        
        **kwargs goes to adrfitter.fit() [modefit fit prop kwargs]

        Returns
        -------
        dict (fitvalues)
        """

        if used_slindexes is None:
            used_slindexes = self.slindexes[~self.fetch_outlier()]

        lbda  = np.mean([self.slices[slindex]['lbdarange'] for slindex in used_slindexes], axis=1)
        x0    = self.get_fitted_value("xcentroid",slindexes=used_slindexes,     fitkey=fitkey)
        x0err = np.asarray(self.get_fitted_value("xcentroid.err",slindexes=used_slindexes, fitkey=fitkey))+error_floor
        y0    = self.get_fitted_value("ycentroid",slindexes=used_slindexes,     fitkey=fitkey)
        y0err = np.asarray(self.get_fitted_value("ycentroid.err",slindexes=used_slindexes, fitkey=fitkey))+error_floor
        
        if spaxel_unit is not None: self.adrfitter.model._unit = spaxel_unit
        self.adrfitter.set_data(lbda, x0, y0, x0err, y0err)
        
        # ADR Guesses based on header information
        guess_adr_param = header_to_adr_param(self.cube.header)
        
        # Overwrite
        if parangle is not None:
            guess_adr_param["parangle_guess"] = parangle
            guess_adr_param["parangle_boundaries"] = [parangle-10,parangle+10]
        if ignore_upper_airmass:
            guess_adr_param["airmass_boundaries"] = [1.0005, guess_adr_param["airmass_guess"]*1.4]
            
        
        default_guesses = {k:v for k,v in guess_adr_param.items()}
        default_guesses["xref_guess"] = np.mean(x0)
        default_guesses["yref_guess"] = np.mean(y0)

        self.adrfitter.fit( **kwargs_update(default_guesses,**kwargs) )
        
        if self.adrfitter.dof> 0 and self.adrfitter.fitvalues["chi2"] / self.adrfitter.dof >5:
            print("WARNING: ADR fit chi2/dof of %.1f - most likely a badly fitted point is causing trouble"%(self.adrfitter.fitvalues["chi2"] / self.adrfitter.dof))
            
        if show:
            self.adrfitter.show(**show_prop)
            
        return self.adrfitter.fitvalues


    # --------- #
    # PLOTTING  # 
    # --------- #
    def show_ellipse(self, used_slindexes=None, show_model=True):
        """ """
        
        if used_slindexes is None:
            used_slindexes = self.slindexes
            
        mask_removed = self.fetch_outlier(used_slindexes=used_slindexes)
        kept_slindexes = np.asarray(used_slindexes)[~mask_removed]
        rejected_slindexes = np.asarray(used_slindexes)[mask_removed]
        
        #                 #
        #    Data         #
        #                 #
        [mean_ell, mean_ellerr, mean_xy, mean_xyerr]  = self.get_ellipse_parameters(used_slindexes=kept_slindexes)
        #                 #
        #    Axis         #
        #                 #
        fig  = mpl.figure(figsize=[6,6])
        
        error_prop   = dict(ls="None", marker="None", ms=0, ecolor="0.7", zorder=1)
        scatter_prop = dict(s=50, zorder=4)

        
        
        fig = self._show_corner_( ["ell","xy"], fig=fig, labels=["ellipticity",r"Angle [rad]"],
                                  expectation=[mean_ell, mean_xy] if show_model else None, expectation_err=[mean_ellerr, mean_xyerr],
                                  used_slindexes = kept_slindexes,
                                  error_prop=error_prop, **scatter_prop )
        
        if np.any(mask_removed):
            scatter_prop_out = dict(s=20, zorder=4, facecolors="None", edgecolors="0.7")
            fig = self._show_corner_( ["ell","xy"], fig=fig, labels=["ellipticity",r"Angle [rad]"],
                                  used_slindexes = rejected_slindexes, show_labels=False,
                                  error_prop=error_prop, **scatter_prop_out )
        
    def show_profile(self, used_slindexes=None, show_model=True,
                         psfmodel="NormalMoffat"):
        """ """
        if used_slindexes is None:
            used_slindexes = self.slindexes
            
        mask_removed = self.fetch_outlier(used_slindexes=used_slindexes)
        kept_slindexes = np.asarray(used_slindexes)[~mask_removed]
        rejected_slindexes = np.asarray(used_slindexes)[mask_removed]

        if psfmodel in ["BiNormal"]:
            profile_parameters = ["sigma","sigma_ratio","amplitude_ratio"]
            labels = ["Scale [std]",r"Scale ratio","Amplitude Ratio"]
        elif psfmodel in ["NormalMoffat", "MoffatNormal"]:
            profile_parameters = ["sigma","alpha","amplitude_ratio"]
            labels = ["Scale [std]",r"Moffat $\alpha$","Amplitude Ratio"]
            show_model = False
        elif psfmodel in ["Moffat"]:
            profile_parameters = ["alpha","beta"]
            labels = [r"Moffat $\alpha$",r"Moffat $\beta$"]
            show_model = False
        else:
            raise ValueError("only BiNormal and NormalMoffat implemented")
        #                 #
        #    Data         #
        #                 #
        if show_model:
            amplitude_ratio, amplitude_ratioerr = self.get_amplitude_ratio( used_slindexes=kept_slindexes)
            sigma_ratio, sigma_ratioerr       = self.get_sigma_ratio(    used_slindexes=kept_slindexes)
        #                 #
        #    Axis         #
        #                 #
        fig  = mpl.figure(figsize=[6,6])
        error_prop   = dict(ls="None", marker="None", ms=0, ecolor="0.7", zorder=1)
        scatter_prop = dict(s=50, zorder=4)
        expectation_color = "C5"
        #   The Figure    #
        fig = self._show_corner_( profile_parameters, fig=fig,
                                  labels=labels,
                                  used_slindexes = kept_slindexes,
                                  expectation=[None,sigma_ratio, amplitude_ratio] if show_model else None,
                                  expectation_err=[None,sigma_ratioerr, amplitude_ratioerr] if show_model else None,
                                  expectation_color=expectation_color,
                                  error_prop=error_prop, **scatter_prop )


        if np.any(mask_removed):
            scatter_prop_out = dict(s=20, zorder=4, facecolors="None", edgecolors="0.7")
            fig = self._show_corner_(  profile_parameters, fig=fig,
                                           used_slindexes = rejected_slindexes,
                                       labels=[None]*len(profile_parameters), show_labels=False,
                                        error_prop=error_prop, **scatter_prop_out )

            
        if show_model:
            lbda = np.linspace(3000,10000,100)
            ax1 = fig.axes[0]
            sigmaref, rho = self.get_sigma_parameters(used_slindexes=used_slindexes)
            ax1.plot(lbda, sigma_chromaticity(lbda, sigmaref, rho=rho), color=expectation_color,
                         scalex=False)
            ax1.plot(lbda, sigma_chromaticity(lbda, sigmaref, rho=-1/5), color="0.5", ls="--", alpha=0.5, zorder=1,
                         scalex=False)
            ax1.text(0.9,0.9, "rho=%.2f"%rho, color=expectation_color,
                         va="top",ha="right", transform = ax1.transAxes)

    def show_adr(self, ax=None, **kwargs):
        """ """
        if 'AIRMASS' not in self.cube.header:
            self.adrfitter.show(ax=ax, guess_airmass=-1.0, **kwargs)
        else:
            self.adrfitter.show(ax=ax, guess_airmass=self.cube.header["AIRMASS"], **kwargs)
        
    # =================== #
    #   Internal          #
    # =================== #
    def _show_kx_v_ky_(self, ax, keyx, keyy, keyxerr=None, keyyerr=None, used_slindexes=None,
                           error_prop={}, **kwargs):
        """ """
        x_ = self.get_fitted_value(keyx, slindexes=used_slindexes)
        dx_ = None if keyxerr is None else self.get_fitted_value(keyxerr, slindexes=used_slindexes)
        y_ = self.get_fitted_value(keyy, slindexes=used_slindexes)
        dy_ = None if keyyerr is None else self.get_fitted_value(keyyerr, slindexes=used_slindexes)
        
        ax.scatter(x_, y_, **kwargs_update( dict(s=50, zorder=4),**kwargs))
        ax.errorbar(x_, y_, xerr=dx_, yerr=dy_,
                        **kwargs_update( dict(ls="None", marker="None", ms=0, ecolor="0.7", zorder=1),**error_prop))
        
    def _show_corner_(self,  parameters, fig=None, used_slindexes=None, error_prop={},
                          expectation=None, expectation_err=None, expectation_color="C5",
                          show_labels=True,
                          labels=None,**kwargs):
        """ """
        n_param = len(parameters)
        if fig is None:
            fig = mpl.figure()

        if labels is None:
            labels = parameters
        if expectation is None: expectation = [None] * n_param
                
        if expectation_err is None: expectation_err = [None] * n_param
                
        for i,xkey in enumerate(parameters):
            for j,ykey in enumerate(parameters):
                if j>i : continue
                ax = fig.add_subplot(n_param,n_param,i*n_param+(j+1))
                if j ==0 and show_labels: ax.set_ylabel(labels[i])
                    
                if ykey == xkey:
                    self._show_kx_v_ky_(ax, "lbda",ykey, keyyerr=ykey+".err",
                                used_slindexes=used_slindexes, error_prop=error_prop, **kwargs)
                    if show_labels: ax.set_xlabel(r"Wavelength [$\AA$]")
                    if expectation[i] is not None:
                        ax.axhline(expectation[i], color=expectation_color)
                        if expectation_err[i] is not None:
                            ax.axhspan(expectation[i]-expectation_err[i],expectation[i]+expectation_err[i],
                                    color=expectation_color, alpha=0.3)
                else:
                    self._show_kx_v_ky_(ax,ykey,xkey, keyxerr=ykey+".err", keyyerr=xkey+".err",
                                    used_slindexes=used_slindexes, error_prop=error_prop, **kwargs)
                    if expectation[i] is not None and expectation[j] is not None:
                        ax.scatter(expectation[j], expectation[i], color=expectation_color,
                                       **kwargs_update(kwargs,**{"marker":"s"}))
                        if expectation_err[i] is not None or expectation_err[j] is not None:
                            ax.errorbar(expectation[j], expectation[i],
                                        xerr=expectation_err[j], yerr=expectation_err[i], 
                                        **kwargs_update(error_prop, **{"ecolor":expectation_color}))
                            
                    if i==n_param-1 and show_labels: ax.set_xlabel(labels[j])
        fig.tight_layout()
        return fig
    # =================== #
    #   Properties        #
    # =================== #
    def _test_index_(self, slindex):
        """ Raises a ValueError if index not in self.slices """
        if slindex not in self.slices:
            raise ValueError("unknown slice '%s'"%slindex)

    # -------
    #  Slice
    # ------- 
    @property
    def slices(self):
        """ """
        if self._properties['slices'] is None:
            self._properties['slices'] = {}
        return self._properties['slices']


    @property
    def slindexes(self):
        """ """
        return np.asarray(list(self.slices.keys()))
    
    # -------
    #  Cube
    # ------- 
    @property
    def cube(self):
        """ """
        return self._properties['cube']

    # ========= #
    # -------
    # ADR
    # -------
    @property
    def adrfitter(self):
        """ """
        return self._derived_properties["adrfitter"]


################################
#                              #
#                              #
#     SLICE FITTER             #
#                              #
#                              #
################################
class PSFFitter( BaseFitter ):
    """ """
    Properties         = ["spaxelhandler"]
    SIDE_PROPERTIES    = ["fit_area","errorscale","intrinsicerror"]
    DERIVED_PROPERTIES = ["fitted_indexes","dataindex",
                          "xfitted","yfitted","datafitted","errorfitted"]
    # -------------- #
    #  SETTER        #
    # -------------- #
    def _set_spaxelhandler_(self, spaxelhandler ) :
        """ """
        self._properties["spaxelhandler"] = spaxelhandler
        
    def set_fit_area(self, polygon):
        """ Provide a polygon. Only data within this polygon will be fit 

        Parameters
        ----------
        polygon: [shapely.geometry.Polygon or array]
            The polygon definition. Spaxels within this area will be fitted.
            This could have 2 formats:
            - array: the vertices. The code will create the polygon using shapely.geometry(polygon)
            - Polygon: i.e. the result of shapely.geometry(polygon)
        
        Returns
        -------
        Void
        """
        if type(polygon) in [np.array, np.ndarray, list]:
            polygon = shapely.geometry(polygon)
        
        self._side_properties['fit_area'] = polygon
        self.set_fitted_indexes(self._spaxelhandler.get_spaxels_within_polygon(polygon))
        
    def set_fitted_indexes(self, indexes):
        """ provide the spaxel indexes that will be fitted """
        self._derived_properties["fitted_indexes"] = indexes
        self._set_fitted_values_()
       
    # ================ #
    #  Properties      #
    # ================ #
    @property
    def _spaxelhandler(self):
        """ """
        return self._properties['spaxelhandler']


    def _set_fitted_values_(self):
        """ """
        x, y = np.asarray(self._spaxelhandler.index_to_xy(self.fitted_indexes)).T
        self._derived_properties['xfitted'] = x
        self._derived_properties['yfitted'] = y
        self._derived_properties['datafitted']  = self._spaxelhandler.data.T[self._fit_dataindex].T
        if USE_LEASTSQ:
            from astropy.stats import mad_std
            
            self._derived_properties['errorfitted'] = mad_std(self._datafitted[self._datafitted==self._datafitted])*1.4
            self.set_error_scale(1)
            self.set_intrinsic_error(0)
            
        else:
            if np.any(self._spaxelhandler.variance.T[self._fit_dataindex]<0):
                warnings.warn("Negative variance detected. These variance at set back to twice the median vairance.")
                var = self._spaxelhandler.variance.T[self._fit_dataindex]
                var[var<=0] = np.nanmedian(var)*2
                self._derived_properties['errorfitted'] = np.sqrt(var)
            else:
                self._derived_properties['errorfitted'] = np.sqrt(self._spaxelhandler.variance.T[self._fit_dataindex]).T
            
            if self._side_properties['errorscale'] is None:
                self.set_error_scale(1)
            
            if self._side_properties['intrinsicerror'] is None:
                self.set_intrinsic_error(0)

    def set_error_scale(self, scaleup):
        """ """
        self._side_properties['errorscale']  = scaleup

    def set_intrinsic_error(self, int_error):
        """ """
        self._side_properties['intrinsicerror'] = int_error
        
    @property
    def _intrinsic_error(self):
        """ """
        return self._side_properties['intrinsicerror']
        
    @property
    def _xfitted(self):
        """ """
        return self._derived_properties['xfitted']
    @property
    def _yfitted(self):
        """ """
        return self._derived_properties['yfitted']
    @property
    def _datafitted(self):
        """ """
        return self._derived_properties['datafitted']
    
    @property
    def _errorfitted(self):
        """ """
        return self._derived_properties['errorfitted'] * self._errorscale + self._intrinsic_error

    @property
    def _errorscale(self):
        """ """
        return self._side_properties['errorscale']
    
    # - indexes and ids
    @property
    def fit_area(self):
        """ polygon of the restricted fitted area (if any) """
        return self._side_properties['fit_area']

    @property
    def fitted_indexes(self):
        """ list of the fitted indexes """
        if self._derived_properties["fitted_indexes"] is None:
            return self._spaxelhandler.indexes
        return self._derived_properties["fitted_indexes"]
    
    @property
    def _fit_dataindex(self):
        """ indices associated with the indexes """
        
        if self._derived_properties["fitted_indexes"] is None:
            return np.arange(self._spaxelhandler.nspaxels)
        # -- Needed to speed up fit
        if self._derived_properties["dataindex"] is None:
            self._derived_properties["dataindex"] = \
              np.in1d( self._spaxelhandler.indexes, self.fitted_indexes)
              
        return self._derived_properties["dataindex"]

class SlicePSF( PSFFitter ):
    """ """
    # =================== #
    #   Methods           #
    # =================== #
    def __init__(self, slice_,
                     fitbuffer=None,fit_area=None,
                     psfmodel="NormalMoffatTilted",
                     fitted_indexes=None):
        """ The SlicePSF fitter object

        Parameters
        ---------- 
        slice_: [pyifu Slice] 
            The slice object that will be fitted
            

        fitbuffer: [float] -optional- 
            = Ignored if fit_area or fitted_indexes are given=

        psfmodel: [string] -optional-
            Name of the PSF model used to fit the slice. 
            examples: 
            - MoffatPlane`N`:a Moffat2D profile + `N`-degree Polynomial2D background 
        
        """
        self.set_slice(slice_)
        # - Setting the model
        self.set_model(read_psfmodel(psfmodel))

        # = Which Data
        if fitted_indexes is not None:
            self.set_fitted_indexes(fitted_indexes)
        elif fit_area is not None:
            self.set_fit_area(fit_area)
        elif fitbuffer is not None:
            self._set_fitted_values_()
            g = self.get_guesses() 
            x,y = self.model.centroid_guess
            self.set_fit_area(shapely.geometry.Point(x,y).buffer(fitbuffer))
        else:
            self._set_fitted_values_()
            
        self.use_minuit = True

    # --------- #
    #  FITTING  #
    # --------- #
    def _get_model_args_(self):
        """ see model.get_loglikelihood"""
        self._set_fitted_values_()
        # corresponding data entry:
        return self._xfitted, self._yfitted, self._datafitted, self._errorfitted

    def get_guesses(self, xcentroid=None, xcentroid_err=2, ycentroid=None, ycentroid_err=2):
        """ you can help to pick the good positions by giving the x and y centroids """
        return self.model.get_guesses(self._xfitted, self._yfitted, self._datafitted,
                            xcentroid=xcentroid, xcentroid_err=xcentroid_err,
                            ycentroid=ycentroid, ycentroid_err=ycentroid_err)

    # --------- #
    #  SETTER   #
    # --------- #
    def set_slice(self, slice_):
        """ set a pyifu slice """
        #from pyifu.spectroscopy import Slice
        #if Slice not in slice_.__class__.__mro__:
        #   raise TypeError("the given slice is not a pyifu Slice (of Child of)")
        self._set_spaxelhandler_(slice_)
        
    # --------- #
    # PLOTTER   #
    # --------- #
    def show_psf(self, ax=None, show=True, savefile=None, nobkgd=True, **kwargs):
        """ """
        import matplotlib.pyplot as mpl
        from .model import get_radial_distance
        if ax is None:
            fig = mpl.figure(figsize=[6,4])
            ax  = fig.add_axes([0.13,0.1,0.77,0.8])
        else:
            fig = ax.figure
            
            
        r_ellipse = get_radial_distance(self._xfitted, self._yfitted, xcentroid=self.fitvalues['xcentroid'],
                                            ycentroid=self.fitvalues['ycentroid'],
                                            yw=self.fitvalues['ell'], xy=self.fitvalues['xy'])
        if nobkgd:
            background = self.model.get_background(self._xfitted, self._yfitted)
            datashown = self._datafitted - background
        else:
            datashown = self._datafitted
        ax.scatter(r_ellipse, datashown, marker="o", zorder=2, s=80, edgecolors="0.7",
                       facecolors=mpl.cm.binary(0.2,0.7))
        ax.errorbar(r_ellipse, datashown, yerr=self._errorfitted,
                    marker="None", ls="None", ecolor="0.7", zorder=1, alpha=0.7)

        
        self.model.display_model(ax, np.linspace(0.0,np.nanmax(r_ellipse),500), nobkgd=nobkgd,
                                     **kwargs)
        
        if savefile:
            fig.savefig(savefile)
        if show:
            fig.show()

    def get_model(self):
        """ """
        from pyifu import get_slice
        return get_slice(self.model.get_model(self._xfitted ,self._yfitted),
                             np.asarray(self.slice.index_to_xy(self.slice.indexes)),
                                    spaxel_vertices=self.slice.spaxel_vertices, variance=None,
                                    indexes=self.slice.indexes)

    
    def show(self, savefile=None, show=True,
                 centroid_prop={}, logscale=True,psf_in_log=True, 
                 vmin="2", vmax="98", ylim_low=None, xlim=[0,10], **kwargs):
        """ """
        import matplotlib.pyplot            as mpl
        from .tools     import kwargs_update
        from pyifu.spectroscopy import get_slice
        
        # -- Axes Definition
        fig = mpl.figure(figsize=(9, 2.5))
        left, width, space = 0.05, 0.15, 0.02
        bottom, height = 0.2, 0.65
        axdata  = fig.add_axes([left+0*(width+space), bottom, width, height])
        axmodel = fig.add_axes([left+1*(width+space), bottom, width, height],
                                   sharex=axdata, sharey=axdata)
        axres   = fig.add_axes([left+2*(width+space), bottom, width, height],
                                   sharex=axdata, sharey=axdata)
        
        axpsf   = fig.add_axes([left+3*(width+space)+space*1.5, bottom, 0.955-(left+3*(width+space)+space), height])

        # = Data
        slice_    = self.slice.data 
        slice_var = self.slice.variance

        model_slice = self.get_model()
        model_      = model_slice.data
        x,y       = np.asarray(self.slice.index_to_xy(self.slice.indexes)).T
        
        res_      = slice_ - model_
        res_slice = get_slice(res_, np.asarray(self.slice.index_to_xy(self.slice.indexes)),
                                    spaxel_vertices=self.slice.spaxel_vertices, variance=None,
                                    indexes=self.slice.indexes)
        # = Plot
        self.slice.show( ax=axdata, vmin=vmin, vmax=vmax , show_colorbar=False, show=False, autoscale=True)
        model_slice.show( ax=axmodel, vmin=vmin, vmax=vmax , show_colorbar=False, show=False, autoscale=True )
        res_slice.show( ax=axres, vmin=vmin, vmax=vmax , show_colorbar=False, show=False, autoscale=True )
        self.show_psf(ax=axpsf, show=False, scalex=False, scaley=False)
        
        # fancy
        [ax_.set_yticklabels([]) for ax_ in fig.axes[1:]]
        axdata.set_title("Data")
        axmodel.set_title("Model")
        axres.set_title("Residual")
            
        axpsf.set_xlabel("Elliptical distance [in spaxels]")
        if xlim is not None:
            axpsf.set_xlim(*xlim)
            
        if psf_in_log:
            if ylim_low is None: ylim_low = 1
            axpsf.set_ylim(ylim_low, slice_.max()*2)
            axpsf.set_yscale("log")

        fig.text(0.95,0.95, "model: %s"%self.model.NAME, fontsize="small",
                     va="top", ha="right")
        fig.figout(savefile=savefile, show=show)
        
    # =================== #
    #  Properties         #
    # =================== #
    @property
    def slice(self):
        """ pyifu slice """
        return self._spaxelhandler

    @property
    def npoints(self):
        """ """
        return len(self._datafitted)

    @property
    def lbda(self):
        """ wavelength of the fitted slice (if given) """
        return self.slice.lbda
