#! /usr/bin/env python
# -*- coding: utf-8 -*-

""" Slice Based Modelisation """


import pyifu
import numpy as np

# PSF Model based on psfimg
from psfimg import psffitter


def get_slice_psf(slice, model="MoffatGaussianTilted"):
    slpsf = SlicePSF2D(slice)
    if type(model) == str:
        slpsf.set_model( eval(model+("()" if not model.endswith(")") else "")) )
    else:
        slpsf.set_model(model)

    return slpsf

# ==================== #
#                      #
#    FITTER            #
#                      #
# ==================== #

class SlicePSF2D( psffitter.FitPSF2D ):
    PROPERTIES = ["slice"]
    SIDE_PROPERTIES = ["centroid","centroid_error"]
    
    def __init__(self, slice_):
        """ """
        self.set_slice(slice_)
        
    def set_slice(self, slice_):
        """ """
        self._properties["slice_"] = slice_
        self.set_image(self.slice.data, self.slice.variance, pixels=np.asarray(self.slice.index_to_xy(self.slice.indexes)) )

    def set_centroid_guess(self, centroid, centroid_err=[2,2]):
        """ """
        self._side_properties["centroid"] = np.asarray(centroid)
        self._side_properties["centroid_err"] = np.asarray(centroid_err)
        
    # -------- #
    # Fitting  #
    # -------- #
    def get_model(self,  parameter=None, oversampling=False, as_slice=True):
        """ """
        if parameter is not None:
            self.model.setup(parameter)
        model_data = self.model.get_model(self._xfitted, self._yfitted, oversampling=oversampling)
        if not as_slice:
            return model_data
        return pyifu.get_slice(model_data, self.pixels, spaxel_vertices=self.slice.spaxel_vertices, 
                               indexes=self.slice.indexes, lbda=self.slice.lbda)
    
    def get_residual(self, as_slice=True, scale=None, **kwargs):
        """ """
        model = self.get_model(as_slice=False, **kwargs)
        
        if scale is None:
            scale_ = 1
        elif scale in ["error"]:
            err_tot = np.sqrt(self.model.get_fit_variance(model, self.variance))
            scale_ = err_tot
        elif scale_ in ["model"]:
            scale_ = model/100
        else:
            raise ValueError("cannot parse scale (%s). Available [None / error / model]"%scale)
        
        res_data = (self.image-model)/scale_
        if not as_slice:
            return res_data
        
        return pyifu.get_slice( res_data,
                                       self.pixels, spaxel_vertices=self.slice.spaxel_vertices, 
                                       indexes=self.slice.indexes, lbda=self.slice.lbda)
        
    def get_expected_centroid(self):
        """ """
        if self._side_properties["centroid"] is None:
            x, y = self.pixels.T
            argmaxes = np.argwhere(self.image>np.percentile(self.image, 99.5)).flatten() # brightest points
            self._side_properties["centroid"] =  np.nanmedian(x[argmaxes]),np.nanmedian(y[argmaxes]) # centroid
            
        return self._side_properties["centroid"]
    
    # -------- #
    # PLOTTER  #
    # -------- #    
    def _display_datamodel_(self, axes, show_res_as_pull=True, show_guess_position=True, 
                            resprop={}, **kwargs):
        """ """
        axdata, axmodel,axres = axes
        prop = {**{},**kwargs}
        
        # Data
        self.slice.show(ax= axdata, show_colorbar=False, **prop)
        # Model
        model = self.get_model(as_slice=True)
        model.show(ax=axmodel, show_colorbar=False, **prop)
        # Model
        residuals_ = self.get_residual(scale="error")
        residuals_.show(ax=axres,show_colorbar=False, **{**prop,**resprop})

        axdata.set_title("data")
        axmodel.set_title("Model (%s)"%self.model.NAME)
        axres.set_title("Residual")
        
        if show_guess_position:
            x_guess,y_guess = self.get_expected_centroid()
            [ax_.scatter(x_guess, y_guess, s=50, color="C1", marker="x") for ax_ in [axdata,axmodel,axres] ]
        return residuals_.data
    
    # ============= #
    #  Properties   #
    # ============= #
    @property
    def slice(self):
        """ """
        return self._properties["slice_"]
    
    @property
    def position_bounds(self):
        """ """
        return (np.asarray(self._centroid_error*[-1,1]).reshape(2,1) + self.get_expected_centroid()).T

    @property
    def _centroid_error(self):
        """ """
        if self._side_properties["centroid_error"] is None:
            self._side_properties["centroid_error"] = np.asarray([2,2])
        return self._side_properties["centroid_error"]
# ==================== #
#                      #
#    MODEL             #
#                      #
# ==================== #
#
# Flat Background
#
class MoffatGaussianFlat( psffitter.MoffatGaussian2DPSF ):
    """ """
    NAME = "mg-flat"
    BACKGROUND_PARAMETERS = ["bkgd"]
#
# Tilted Plane
#
def tilted_plane(x, y,
                three_coefs):
    """ """
    return np.dot(np.asarray([np.ones(x.shape[0]), x, y]).T, three_coefs)

class MoffatGaussianTilted( psffitter.MoffatGaussian2DPSF ):
    """ """
    NAME = "mg-tilted"
    BACKGROUND_PARAMETERS = ["bkgd","bkgdx","bkgdy"]
    
    def get_background(self, x, y):
        """ The background at the given positions """
        return tilted_plane(x, y, [self.param_background[k] for k in self.BACKGROUND_PARAMETERS])
#
# Curved Plane
#
def curved_plane(x, y,
                five_coefs):
    """ """
    return np.dot(np.asarray([np.ones(x.shape[0]), x, y, x*y, x*x, y*y]).T, five_coefs)

class MoffatGaussianCurved( psffitter.MoffatGaussian2DPSF ):
    """ """
    NAME = "mg-curved"
    BACKGROUND_PARAMETERS = ["bkgd","bkgdx","bkgdy","bkgdxy","bkgdxx","bkgdyy"]
    
    def get_background(self, x, y):
        """ The background at the given positions """
        return curved_plane(x, y, [self.param_background[k] for k in self.BACKGROUND_PARAMETERS])
