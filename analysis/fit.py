# *****************************************************************************
#   Description: A set of utilities to ease SIPHRA spectra analysis.
#   Implements PyROOT dependencies.
#   Written by: Oscar Rosero (KTH)
#....
#   Date: 02/2026

import ROOT

def gauspeak(n_init: int):
    return f"[{n_init}]*TMath::Gaus(x, [{n_init+1}], [{n_init+2}])"

def bg_exp(n_init: int):
    return f"[{n_init}]*TMath::Exp(-x/[{n_init+1}])"

def peak_and_bg():
    return f"{bg_exp(0)}+{gauspeak(2)}"

def fit_peak_expbg(hist: ROOT.TF1,
                   name: str,
                   xl: float, xr: float,
                   norm: float, mean: float, sigma: float =70,
                   const: float=200, denom=200,
                   showFit: bool =False, keep_prev_fncs: bool =True):
    '''
    Fits a gaussian peak in a part of a spectrum assuming exponentially decaying background.
    Parameters
    ----------
    hist : ROOT.TH1F
        Histogram of spectrum
    name : str
        Name for the fit function
    xl, xr : float
        Lower and upper limits of the section of the spectrum to be fitted
    norm, mean, sigma : float
        Parameters of the gaussian [norm]*TMmath::Gauss(x, [mean], [sigma])
    const, denom : float
        Parameters of the exponentially decaying background [const]*TMmath::Exp(-x/[denom])
    showFit : bool
        If false the fit will be executed in silent mode, so the fit function is not displayed
    keep_prev_fncs : bool
        If true the new fit function is added to the list of functions, otherwise it overwrites previous ones.
    '''
    fit_fn = ROOT.TF1(name, peak_and_bg(), xl, xr, 5)
    fit_fn.SetParNames("Const", "Denom", "Norm", "Mean", "Sigma")
    fit_fn.SetParameters(const, denom, norm, mean, sigma)
    options = "L S" if showFit else "0 S"
    options += " +" if keep_prev_fncs else ""
    fit_result = hist.Fit(fit_fn, options, "", xl, xr)
    return fit_fn, fit_result