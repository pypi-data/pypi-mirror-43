
""" Generic simple tools. """

import numpy as np

__all__ = ["kwargs_update"]


def kwargs_update(default,**kwargs):
    """
    """
    k = default.copy()
    for key,val in kwargs.items():
        k[key] = val
        
    return k



def fit_intrinsic(data, model, errors, dof, intrinsic_guess=None):
    """ Get the most optimal intrinsic dispersion given the current fitted standardization parameters. 
    
    The optimal intrinsic magnitude dispersion is the value that has to be added in quadrature to 
    the errors such that the chi2/dof is 1.
    Returns
    -------
    float (intrinsic dispersion)
    """
    from scipy.optimize import fmin
    def get_intrinsic_chi2dof(intrinsic):
        return np.abs( np.nansum((data-model)**2/(errors**2+intrinsic**2)) / dof - 1)
    
    if intrinsic_guess is None:
        intrinsic_guess = np.nanmedian(errors)
        
    return fmin(get_intrinsic_chi2dof, intrinsic_guess, disp=0)[0]
