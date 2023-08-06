#! /usr/bin/env python
# -*- coding: utf-8 -*-

""" Handle Slice Collections """

import numpy as np
import pandas
from propobject import BaseObject

# Internal
from . import psfslice

def get_slices_collection(cube, lbdaranges=[4000,8000], bins=6):
    """ """
    step_lbda_  = np.linspace(lbdaranges[0],lbdaranges[1], bins+1)
    lbda_slices =  np.asarray([step_lbda_[:-1], step_lbda_[1:]]).T
    return SlicePSFCollection([cube.get_slice(lbda_min=lmin, lbda_max=lmax, slice_object=True)
                                   for lmin, lmax in lbda_slices])



class SlicePSFCollection( BaseObject ):
    """ """
    PROPERTIES = ["slices", "model"]
    DERIVED_PROPERTIES = ["psfslices","fitvalues"]
    def __init__(self, slices, indexes=None):
        """ """
        self.set_slices(slices, indexes)

    def set_slices(self, slices, indexes=None):
        """ """
        if type(slices) is dict:
            self._properties["slices"] = slices
        else:
            if indexes is None:
                indexes = np.arange(len(slices))
            self._properties["slices"] = {i:s_ for i,s_ in zip(indexes, slices)}

        
    def set_model(self, model):
        """ """
        self._properties["model"] = model
        
    def set_psf_values(self, psf_values_, indexes=None):
        """ """
        if type(psf_values_) is dict:
            self._derived_properties["psf_values"] = pandas.DataFrame(psf_values_)
        elif type(psf_values_) is pandas.DataFrame:
            self._derived_properties["psf_values"] = psf_values_
        else:
            if indexes is None:
                indexes = np.arange(len(fitvalues))
            self._derived_properties["psf_values"] = pandas.DataFrame({i:f_ for i,f_ in zip(indexes, psf_values_)})
            
    # ------- #
    #  Fitter #
    # ------- #
    def fit_slices(self, **kwargs):
        """ """

        fitvalues = {}
        for i,s_ in self.slices.items():
            s_to_fit = s_.copy()
            norm = np.nanmean(s_.data)
            s_to_fit.scale_by(norm)
            self.psfslices[i] = psfslice.get_slice_psf(s_to_fit, self.model)
            self.psfslices[i].fit()
            fitvalues[i] = self.psfslices[i].fitvalues
            fitvalues[i]["norm"] = norm
            
        self.set_psf_values(fitvalues)

    # ================= #
    #   Properties      #
    # ================= #
    @property
    def slices(self):
        """ dict containing the slices """
        if self._properties["slices"] is None:
            self._properties["slices"] = {}
        return self._properties["slices"]

    @property
    def model(self):
        """ """
        if self._properties["model"] is None:
            self._properties["model"] = "MoffatGaussianTilted"
        return self._properties["model"]

    @property
    def model_params(self):
        """ What parameters does the model have? """
        if self.model is None:
            return None
        return eval("psfslice.%s.get_model_param()"%self.model)
    
    @property
    def psfslices(self):
        """ """
        if self._derived_properties["psfslices"] is None:
            self._derived_properties["psfslices"] = {}
        return self._derived_properties["psfslices"]
        
    @property
    def psf_values(self):
        """ """
        if self._derived_properties["psf_values"] is None:
            self._derived_properties["psf_values"] = {}
        return self._derived_properties["psf_values"]
