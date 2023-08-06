#! /usr/bin/env python
# -*- coding: utf-8 -*-

""" PSF Modelisation """


import numpy as np
from scipy.stats import norm
from scipy import integrate
from scipy.special import gamma
from modefit.baseobjects import BaseModel

################################
#                              #
#                              #
#  Main User Functions         #
#                              #
#                              #
################################


def read_psfmodel(psfmodel):
    """ """
    
    if "BiNormalFlat" in psfmodel:
        return BiNormalFlat()
    elif "BiNormalTilted" in psfmodel:
        return BiNormalTilted()
    elif "BiNormalCurved" in psfmodel:
        return BiNormalCurved()
    elif "NormalMoffatFlat" in psfmodel:
        return NormalMoffatFlat()
    elif "NormalMoffatTilted" in psfmodel:
        return NormalMoffatTilted()
    elif "NormalMoffatCurved" in psfmodel:
        return NormalMoffatCurved()
    
    elif "MoffatFlat" in psfmodel:
        return MoffatFlat()
    elif "MoffatTilted" in psfmodel:
        return MoffatTilted()
    elif "MoffatCurved" in psfmodel:
        return MoffatCurved()

    else:
        raise ValueError("Only the '{BiNormal/NormalMoffat}{Flat/Tilted/Curved}' psfmodel has been implemented")


################################
#                              #
#                              #
#  Profile and Background      #
#                              #
#                              #
################################

# ========================= #
#                           #
#  Profiles                 #
#                           #
# ========================= #
"""
# How To build a new profile?

All profile must have the following format:
```python
def name_of_the_profile(x,y,
                        here, define, your, variables,
                        xcentroid=0, ycentroid=0):
     ''' ADD Documentation '''

     do_the_job

     return list_of_values (1darray with the same length as x/y)
```
The profile should be normalize, but this is not mendatory.

"""
def binormal_profile(x, y,
                sigma, sigma_ratio, eta,
                xy, ell,
                xcentroid=0, ycentroid=0,
                amplitude=1):
    """ Return the model profile.
    Here a binormal profile.
    if decomposed
        
    Returns
    -------
    array (model)
            
    """
    print("BINORMAL NOT READY")
    r = get_radial_distance(x, y, xcentroid=xcentroid, ycentroid=ycentroid,  yw=ell, xy=xy)
    n1 = _normal_(r, scale=sigma) 
    n2 = _normal_(r, scale=sigma*sigma_ratio)
    
    return amplitude * ( n1 + eta * n2)

def moffat_profile(x, y, alpha, beta,
                       xy, ell,
                       xcentroid=0, ycentroid=0,
                       amplitude=1):
    """ Return the model profile.
    Here a moffat profile.

    if decomposed
        
    Returns
    -------
    array (model)
    """
    print("MOFFAT NOT READY")    
    r = get_radial_distance(x, y, xcentroid=xcentroid, ycentroid=ycentroid,  yw=ell, xy=xy)
    n1 = _moffat_(r, alpha, beta)
    return amplitude * ( n1 )


def normalmoffat_profile(x, y,
                        sigma, alpha, eta, xy, ell,
                        xcentroid=0, ycentroid=0,
                        amplitude=1,
                        split=False, radius=None):
    """ Return the model profile.
    Here a normal + moffat profile.
    if decomposed
        
    Returns
    -------
    array (model)
    or amplitude, normalization*moffat, eta * normalization*normal
    """
    if x is None and y is None and radius is not None:
        r = radius
    else:
        r = get_radial_distance(x, y, xcentroid=xcentroid, ycentroid=ycentroid,  yw=ell, xy=xy)
    
    beta = _alpha_to_beta_(alpha)
    normal = _normal_(r, scale=sigma) 
    moffat = _moffat_(r, alpha, beta=beta) 
    
    normalization = np.sqrt(ell - xy**2)/( np.pi * (2 * eta * sigma**2 + alpha**2 / (beta - 1)) )
    if split:
        return amplitude, normalization*moffat, normalization*eta * normal
    
    return amplitude * normalization* ( moffat + eta * normal )








def _alpha_to_beta_(alpha, b0=0.25, b1=0.63):
    """ Ratio given by SNIFS """
    return b0+alpha*b1

# Profiles 
def _normal_(r, scale, normed=False):
    """ """
    if not normed:
        return norm.pdf(r, loc=0, scale=scale) * np.sqrt(2*np.pi*scale**2) # unnormalized
    return norm.pdf(r, loc=0, scale=scale)

def _moffat_(r, alpha, beta, normed=False):
    """ """
    norm =  2*(beta-1)/alpha**2 if normed else 1
    return norm * (1 + (r/alpha)**2 )**(-beta)



def get_normalmoffat_normalisation( param_profile,
                                    xbounds=50, ybounds=50,
                                    epsabs=1e-2 ):
    """ measures the normalisation coefficient one should apply to fitvalues["amplitude"] to have 
    the effective amplitude (i.e., integral of the 2D profile model is 1 if "amplitude" equals 1).
    
    
    Parameters
    ----------

    epsabs : float, optional
        Absolute tolerance passed directly to the inner 1-D quadrature integration. 
        # Scipy default is 1.49e-8.



    // from scipy.integrate.dblquad  //

    a, b : float
        The limits of integration in x: a < b

        => a =  xcentroid - xbound
        => b =  xcentroid + xbound

    gfun : callable or float
        The lower boundary curve in y which is a function taking a single floating point argument (x) and returning a floating point result or a float indicating a constant boundary curve.

        => gfun = lambda x:  ycentroid-ybounds

    hfun : callable or float
        The upper boundary curve in y (same requirements as gfun).

        => hfun = lambda x:  ycentroid+ybounds


        
    Return 
    ------
    float, float 
         [normalisation, estimated error]
    """
    args = [param_profile[k] for k in ["sigma", "alpha", "eta", "xy", "ell", "xcentroid", "ycentroid"]]
    return integrate.dblquad(normalmoffat_profile,
                                 param_profile["xcentroid"]-xbounds, param_profile["xcentroid"]+xbounds,
                                 gfun = lambda x:  param_profile["ycentroid"]-ybounds,
                                 hfun = lambda x:  param_profile["ycentroid"]+ybounds,
                                 epsabs=epsabs, args=args)



# ========================= #
#                           #
#  Background               #
#                           #
# ========================= #
def tilted_plane(x, y,
                three_coefs):
    """ """
    return np.dot(np.asarray([np.ones(x.shape[0]), x, y]).T, three_coefs)


def curved_plane(x, y,
                five_coefs):
    """ """
    return np.dot(np.asarray([np.ones(x.shape[0]), x, y, x*y, x*x, y*y]).T, five_coefs)


# ========================= #
#                           #
#  Ellipticity              #
#                           #
# ========================= #
def get_radial_distance(x, y, xcentroid=0, ycentroid=0, yw=0, xy=0):
    """ 
    Parameters
    ----------
    x,y: [array]
        Cartesian Coordinates

    x0,y0: [float] -optional-
        Cartesian coordinate of the ellipse center
        
    ell: [float] -optional-
        similar to ellipticity, it is the coef in front of y (and not x)
        
    xy: [float] -optional-
        similar to angle, it is the coef in from of 2*x*y
    
    Returns
    -------
    radial distance in elliptical coordinates
    """
    dx, dy = (x-xcentroid), (y-ycentroid)
    return np.sqrt(dx**2 + yw * dy**2 + 2 * xy *dx*dy)
    
    
def get_elliptical_distance(x, y, xcentroid=0, ycentroid=0, ell=0, xy=0):
    """
    Parameters
    ----------
    x,y: [array]
        Cartesian Coordinates

    x0,y0: [float] -optional-
        Cartesian coordinate of the ellipse center
        
    ell: [float] -optional-
        Ellipticity [0<ell<1[
        
    xy: [float] -optional-
        Angle of the ellipse [radian]
    
    Returns
    -------
    array for float (elliptical distance)
    """
    c, s  = np.cos(xy), np.sin(xy)
    rot   = np.asarray([[c, s], [-s, c]])
    xx,yy = np.dot(rot, np.asarray([x-xcentroid, y-ycentroid]))
    return np.sqrt(xx**2 + (yy/(1-ell))**2)


################################
#                              #
#                              #
#     SLICE Model              #
#                              #
#                              #
################################

class _PSFSliceModel_( BaseModel ):
    """ Virtual PSFSlice Model Class. You need to define 
    - get_profile 
    - get_background 
    """
    PROFILE_PARAMETERS    = [] # TO BE DEFINED
    BACKGROUND_PARAMETERS = [] # TO BE DEFINED
    
    def __new__(cls,*arg,**kwarg):
        """ Black Magic allowing generalization of Polynomial models """
        # - Profile
        cls.FREEPARAMETERS     = list(cls.PROFILE_PARAMETERS)+list(cls.BACKGROUND_PARAMETERS)
        return super( _PSFSliceModel_, cls).__new__(cls)

    # ================= #
    #    Method         #
    # ================= #
    # ---------- #
    #  SETTER    #
    # ---------- #
    def setup(self, parameters):
        """ """
        self.param_profile    = {k:v for k,v in zip( self.PROFILE_PARAMETERS, parameters[:len(self.PROFILE_PARAMETERS)] )}
        self.param_background = {k:v for k,v in zip( self.BACKGROUND_PARAMETERS, parameters[len(self.PROFILE_PARAMETERS):] )} 
        
    # ---------- #
    #  GETTER    #
    # ---------- #
    def get_loglikelihood(self, x, y, z, dz):
        """ Measure the likelihood to find the data given the model's parameters.
        Set pdf to True to have the array prior sum of the logs (array not in log=pdf).
        In the Fitter define _get_model_args_() that should return the input of this
        """
        res = z - self.get_model(x, y)
        chi2 = np.nansum(res.flatten()**2/dz.flatten()**2)
        return -0.5 * ( chi2 - 2*self.get_logprior() )

    def get_logprior(self):
        """ If you need to return prior value. Do so here. """
        return 0
    
    def get_model(self, x, y):
        """ the profile + background model. """
        return self.get_profile(x,y) + self.get_background(x,y)

    def get_radial_distance(self, x, y):
        """ """
        return get_radial_distance(x, y,
                                xcentroid=self.param_profile["xcentroid"],
                                ycentroid=self.param_profile["ycentroid"],
                                yw=self.param_profile["ell"],
                                xy=self.param_profile["xy"])
    
    # - To Be Defined
    def get_profile(self, x, y):
        """ The profile at the given positions """
        raise NotImplementedError("You must define the get_profile")
    
    def get_background(self, x, y):
        """ The background at the given positions """
        raise NotImplementedError("You must define the get_background")

    def get_radial_profile(self, radius):
        """ """
        return self.get_profile(None, None, radius=radius)

    # ================ #
    #  Properties      #
    # ================ #
    @property
    def fwhm(self):
        """ assuming the get_radial_profile(), this is *twice the radius needed to reach half the centroid flux (in unit of x,y) 
        *Careful, does not account for ellipticity if any*
        ```python
        rmodel = np.linspace(0,20,1000)
        rspec = self.get_radial_profile(rmodel)
        return rmodel[np.argmin(np.abs(rspec-rspec[0]/2.))]
        ```
        """
        rmodel = np.linspace(0,20,1000)
        rspec = self.get_radial_profile(rmodel)
        return rmodel[np.argmin(np.abs(rspec-rspec[0]/2.))]
# ======================================= #
#                                         #
#  BiNormal + Background    Models        #
#                                         #
# ======================================= #

class BiNormalFlat( _PSFSliceModel_ ):
    """ """
    NAME = "binormal-flat"
    PROFILE_PARAMETERS = ["amplitude",
                          "sigma", "sigma_ratio", "eta",
                          "xy", "ell",
                          "xcentroid", "ycentroid"]
    
    BACKGROUND_PARAMETERS = ["bkgd"]
    
    # ================== #
    #  Guess             #
    # ================== #
    def get_guesses(self, x, y, data,
                        xcentroid=None, xcentroid_err=2,
                        ycentroid=None, ycentroid_err=2):
        """ return a dictionary containing simple best guesses """
        flagok     = ~np.isnan(x*y*data)
        x          = x[flagok]
        y          = y[flagok]
        data       = data[flagok]
        
        ampl       = np.nanmax(data)
        if ycentroid is None or xcentroid is None:
            argmaxes   = np.argwhere(data>np.percentile(data,95)).flatten()

        if xcentroid is None:
            xcentroid  = np.nanmean(x[argmaxes])
        if ycentroid is None:
            ycentroid  = np.nanmean(y[argmaxes])
            
        background = np.percentile(data,10)
        low_bounds = -np.percentile(data,0.01)
        self._guess = dict( amplitude_guess=ampl * 5,
                            amplitude_boundaries= [None, None],
                            # - background
                            bkgd_guess=background, bkgd_boundaries=[0, np.percentile(data,99.9)],
                            # centroid
                            xcentroid_guess=xcentroid, xcentroid_boundaries=[xcentroid-xcentroid_err, xcentroid+xcentroid_err],
                            ycentroid_guess=ycentroid, ycentroid_boundaries=[ycentroid-ycentroid_err, ycentroid+ycentroid_err],
                            # ------------------------ #
                            # SEDM DEFAULT VARIABLES   #
                            # ------------------------ #
                            # Ellipticity
                            ell_guess=1, ell_boundaries=[0.2,5],   ell_fixed=False,
                            xy_guess=0, xy_boundaries=[-0.6, 0.6], xy_fixed=False,
                            # Size
                            sigma_guess = 1.3,
                            sigma_boundaries=[0.5, 5],
                            sigma_ratio_guess=2.,
                            sigma_ratio_boundaries=[1.1, 4],
                            sigma_ratio_fixed=False,
                            # Converges faster by allowing degenerated param...
                            # amplitude ratio
                            eta_guess = 3,
                            eta_fixed = False,
                            eta_boundaries = [1.5,5],
                           )
        return self._guess

    # ================== #
    #  Model             #
    # ================== #
    def get_profile(self, x, y, **kwargs):
        """ """
        return binormal_profile(x, y, **{**self.param_profile,**kwargs})
    
    def get_background(self,x,y):
        """ The background at the given positions """
        return self.param_background["bkgd"]

        
    def display_model(self, ax, rmodel, legend=True,
                          nobkgd=True,
                          cmodel = "C1",
                          cgaussian1 = "C0",cgaussian2 = "C2",
                          cbkgd="k", zorder=7, **kwargs):
        """ """
        # the decomposed binormal_profile
        n1 = _normal_(rmodel, scale=self.param_profile['sigma'])
        n2 = _normal_(rmodel, scale=self.param_profile['sigma']*self.param_profile['sigma_ratio'])

        amplitude = self.param_profile['amplitude']
        # and its background
        background = 0 if nobkgd else self.param_background['bkgd']
        
        # - display background
        if not nobkgd:
            ax.axhline(background, ls=":",color=cbkgd, label="background",zorder=zorder)
        
        # - display details
        ax.plot(rmodel, background + n1*coef1*amplitude, ls="-.",color=cgaussian1, label="Core Gaussian",zorder=zorder,
                    **kwargs)
        ax.plot(rmodel, background + n2*coef2*amplitude, ls="-.",color=cgaussian2, label="Tail Gaussian",zorder=zorder,
                    **kwargs)
        # - display full model
        ax.plot(rmodel, background + (n2+n1*eta)*amplitude, 
                    ls="-",color=cmodel,zorder=zorder+1, lw=2, label="PSF Model",
                    **kwargs)

        # - add the legend
        if legend:
            ax.legend(loc="best", ncol=1)
        
    # ============= #
    #  Properties   #
    # ============= #
    @property
    def centroid_guess(self):
        """ """
        return self._guess["xcentroid_guess"], self._guess["ycentroid_guess"]
    
    @property
    def centroid(self):
        """ """
        return self.fitvalues["xcentroid"], self.fitvalues["ycentroid"]
    
    
class BiNormalTilted( BiNormalFlat ):
    """ """
    NAME = "binormal-tilted"
    BACKGROUND_PARAMETERS = ["bkgd","bkgdx","bkgdy"]
    
    def get_background(self, x, y):
        """ The background at the given positions """
        return tilted_plane(x, y, [self.param_background[k] for k in self.BACKGROUND_PARAMETERS])
    
class BiNormalCurved( BiNormalFlat ):
    """ """
    NAME = "binormal-curved"
    BACKGROUND_PARAMETERS = ["bkgd","bkgdx","bkgdy","bkgdxy","bkgdxx","bkgdyy"]
    
    def get_background(self, x, y):
        """ The background at the given positions """
        return curved_plane(x, y, [self.param_background[k] for k in self.BACKGROUND_PARAMETERS])

# ======================================= #
#                                         #
#  NormalMoffat + Background  Models      #
#                                         #
# ======================================= #


class MoffatFlat( _PSFSliceModel_ ):
    """ """
    NAME = "moffat-flat"
    PROFILE_PARAMETERS = ["amplitude",
                          "alpha",  "beta",
                          "xy", "ell",
                          "xcentroid", "ycentroid"]
    
    BACKGROUND_PARAMETERS = ["bkgd"]

    beta_guess = 2.5
    beta_fixed = True
    # ================== #
    #  Guess             #
    # ================== #
    def get_guesses(self, x, y, data,
                        xcentroid=None, xcentroid_err=2,
                        ycentroid=None, ycentroid_err=2):
        """ return a dictionary containing simple best guesses """
        flagok     = ~np.isnan(x*y*data)
        x          = x[flagok]
        y          = y[flagok]
        data       = data[flagok]
        
        ampl       = np.nanmax(data)
        if ycentroid is None or xcentroid is None:
            argmaxes   = np.argwhere(data>np.percentile(data,95)).flatten()

        if xcentroid is None:
            xcentroid  = np.nanmean(x[argmaxes])
        if ycentroid is None:
            ycentroid  = np.nanmean(y[argmaxes])

        background = np.percentile(data,10)
        low_bounds = -np.percentile(data,0.01)
        self._guess = dict( amplitude_guess=ampl * 5,
                            amplitude_boundaries= [None, None],
                            # - background
                            bkgd_guess=background, bkgd_boundaries=[None, np.percentile(data,99.9)],

                            # centroid
                            xcentroid_guess=xcentroid, xcentroid_boundaries=[xcentroid-xcentroid_err, xcentroid+xcentroid_err],
                            ycentroid_guess=ycentroid, ycentroid_boundaries=[ycentroid-ycentroid_err, ycentroid+ycentroid_err],
                            # ------------------------ #
                            # SEDM DEFAULT VARIABLES   #
                            # ------------------------ #
                            # Ellipticity
                            ell_guess=1, ell_boundaries=[0.2,5],   ell_fixed=False,
                            xy_guess=0, xy_boundaries=[-0.6, 0.6], xy_fixed=False,
                            # Size
                            # moffat
                            alpha_guess=4.,
                            alpha_boundaries=[1., 8],
                            beta_guess=2.,
                            beta_boundaries=[0., None],
                            # Converges faster by allowing degenerated param...
                            # amplitude ratio
                           )
        return self._guess

    # ================== #
    #  Model             #
    # ================== #
    def get_logprior(self):
        """ If you need to return prior value. Do so here. """
        return 0

    def get_profile(self, x, y, **kwargs):
        """ """
        return moffat_profile(x, y,  **{**self.param_profile,**kwargs})
    
    def get_background(self,x,y):
        """ The background at the given positions """
        return self.param_background["bkgd"]
    
    def display_model(self, ax, rmodel, legend=True,
                          nobkgd=True,
                          cmodel = "C1",
                          cgaussian1 = "C0",
                          cbkgd="k", zorder=7, **kwargs):
        """ """
        # the decomposed binormal_profile
        
        n1 = _moffat_(rmodel, alpha=self.param_profile['alpha'], beta=self.param_profile['beta'])

        amplitude = self.param_profile['amplitude']
        # and its background
        background = 0 if nobkgd else self.param_background['bkgd']

        # - display background
        if not nobkgd:
            ax.axhline(background, ls=":",color=cbkgd, label="background",zorder=zorder)
        
        # - display details
        ax.plot(rmodel, background + n1*amplitude, ls="-.",color=cgaussian1, label="Moffat", zorder=zorder,
                    **kwargs)
        
        # - display full model
        #ax.plot(rmodel, background + (n2*coef2+n1*coef1)*amplitude, 
        #            ls="-",color=cmodel,zorder=zorder+1, lw=2, label="PSF Model",
        #            **kwargs)

        # - add the legend
        if legend:
            ax.legend(loc="best", ncol=1)
        
    # ============= #
    #  Properties   #
    # ============= #
    @property
    def centroid_guess(self):
        """ """
        return self._guess["xcentroid_guess"], self._guess["ycentroid_guess"]
    
    @property
    def centroid(self):
        """ """
        return self.fitvalues["xcentroid"], self.fitvalues["ycentroid"]
    
class MoffatTilted( MoffatFlat ):
    """ """
    NAME = "binormal-tilted"
    BACKGROUND_PARAMETERS = ["bkgd","bkgdx","bkgdy"]
    
    def get_background(self, x, y):
        """ The background at the given positions """
        return tilted_plane(x, y, [self.param_background[k] for k in self.BACKGROUND_PARAMETERS])
    
class MoffatCurved( MoffatFlat ):
    """ """
    NAME = "binormal-curved"
    BACKGROUND_PARAMETERS = ["bkgd","bkgdx","bkgdy","bkgdxy","bkgdxx","bkgdyy"]
    
    def get_background(self, x, y):
        """ The background at the given positions """
        return curved_plane(x, y, [self.param_background[k] for k in self.BACKGROUND_PARAMETERS])

# ======================================= #
#                                         #
#  NormalMoffat + Background  Models      #
#                                         #
# ======================================= #


class NormalMoffatFlat( _PSFSliceModel_ ):
    """ """
    NAME = "normal/moffat-flat"
    PROFILE_PARAMETERS = ["amplitude",
                          "alpha", "eta", "sigma", 
                          "xy", "ell",
                          "xcentroid", "ycentroid"]
    
    BACKGROUND_PARAMETERS = ["bkgd"]
    
    # ================== #
    #  Guess             #
    # ================== #
    def get_guesses(self, x, y, data,
                        xcentroid=None, xcentroid_err=2,
                        ycentroid=None, ycentroid_err=2):
        """ return a dictionary containing simple best guesses """
        flagok     = ~np.isnan(x*y*data)
        x          = x[flagok]
        y          = y[flagok]
        data       = data[flagok]
        
        ampl       = np.nanmax(data)
        if ycentroid is None or xcentroid is None:
            argmaxes   = np.argwhere(data>np.percentile(data,95)).flatten()

        if xcentroid is None:
            xcentroid  = np.nanmean(x[argmaxes])
        if ycentroid is None:
            ycentroid  = np.nanmean(y[argmaxes])

        background = np.percentile(data,10)
        low_bounds = -np.percentile(data,0.01)
        self._guess = dict( amplitude_guess=ampl * 5,
                            amplitude_boundaries= [None, None],
                            # - background
                            bkgd_guess=background, bkgd_boundaries=[0, np.percentile(data,99.9)],
                            # centroid
                            xcentroid_guess=xcentroid, xcentroid_boundaries=[xcentroid-xcentroid_err, xcentroid+xcentroid_err],
                            ycentroid_guess=ycentroid, ycentroid_boundaries=[ycentroid-ycentroid_err, ycentroid+ycentroid_err],
                            # ------------------------ #
                            # SEDM DEFAULT VARIABLES   #
                            # ------------------------ #
                            # Ellipticity
                            ell_guess=1, ell_boundaries=[0.2,5],   ell_fixed=False,
                            xy_guess=0, xy_boundaries=[-0.6, 0.6], xy_fixed=False,
                            # Size
                            sigma_guess = 1.3,
                            sigma_boundaries=[1., 2],
                            # moffat
                            alpha_guess=8.,
                            alpha_boundaries=[2., 15.],
                            #beta_guess=2.,
                            #beta_boundaries=[0., None],
                            # Converges faster by allowing degenerated param...
                            # amplitude ratio
                            eta_guess = 2,
                            eta_fixed = False,
                            eta_boundaries = [0.1,10],
                           )
        return self._guess

    # ================== #
    #  Model             #
    # ================== #
    def get_logprior(self):
        """ If you need to return prior value. Do so here. """
        return 0

    def get_profile(self, x, y, **kwargs):
        """ """
        return normalmoffat_profile(x, y, **{**self.param_profile,**kwargs})
    
    def get_background(self,x,y):
        """ The background at the given positions """
        return self.param_background["bkgd"]
        
    def display_model(self, ax, rmodel, legend=True,
                          nobkgd=True,
                          cmodel = "C1",
                          cgaussian1 = "C0",cgaussian2 = "C2",
                          cbkgd="k", zorder=7, **kwargs):
        """ """
        
        amplitude, normed_moffat, normed_normal = normalmoffat_profile(None, None, radius=rmodel, split=True, **self.param_profile)
        
        # and its background
        background = 0 if nobkgd else self.param_background['bkgd']

        # - display background
        if not nobkgd:
            ax.axhline(background, ls=":",color=cbkgd, label="background",zorder=zorder)
        
        # - display details
        ax.plot(rmodel, background + amplitude*normed_normal, ls="-.",color=cgaussian1, label="Gaussian",zorder=zorder,
                    **kwargs)
        ax.plot(rmodel, background + amplitude*normed_moffat, ls="-.",color=cgaussian2, label="Moffat",zorder=zorder,
                    **kwargs)
        # - display full model
        ax.plot(rmodel, (normed_normal+normed_moffat)*amplitude, 
                    ls="-",color=cmodel,zorder=zorder+1, lw=2, label="PSF Model",
                    **kwargs)

        # - add the legend
        if legend:
            ax.legend(loc="best", ncol=1)
        
    # ============= #
    #  Properties   #
    # ============= #
    @property
    def centroid_guess(self):
        """ """
        return self._guess["xcentroid_guess"], self._guess["ycentroid_guess"]
    
    @property
    def centroid(self):
        """ """
        return self.fitvalues["xcentroid"], self.fitvalues["ycentroid"]
    
class NormalMoffatTilted( NormalMoffatFlat ):
    """ """
    NAME = "normal/moffat-tilted"
    BACKGROUND_PARAMETERS = ["bkgd","bkgdx","bkgdy"]
    
    def get_background(self, x, y):
        """ The background at the given positions """
        return tilted_plane(x, y, [self.param_background[k] for k in self.BACKGROUND_PARAMETERS])
    
class NormalMoffatCurved( NormalMoffatFlat ):
    """ """
    NAME = "normal/moffat-curved"
    BACKGROUND_PARAMETERS = ["bkgd","bkgdx","bkgdy","bkgdxy","bkgdxx","bkgdyy"]
    
    def get_background(self, x, y):
        """ The background at the given positions """
        return curved_plane(x, y, [self.param_background[k] for k in self.BACKGROUND_PARAMETERS])
