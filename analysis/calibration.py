import ROOT
import numpy as np

def calibration_fit(histogram, energy_ranges, energies):
    """Function to create a linear calibration fit based on a histogram. Returns slope and constant of linear fit. 
    Inputs: Histogram to base calibration on.
    Ranges within which the peaks of the histogram are located, input as a list if tuples. AT LEAST 2 points.
    Known energies of these peaks, in MeV."""
    
    channels = []
    for i in range(len(energy_ranges)):
        cal_fit=ROOT.TF1("cal_fit_" + str(i), "gaus", energy_ranges[i][0], energy_ranges[i][1])
        histogram.Fit(cal_fit, "R+S")
        channels.append(cal_fit.GetParameter('Mean'))

    channels = np.array(channels, dtype='float64')
    energies = np.array(energies, dtype='float64')

    graph = ROOT.TGraph(len(channels), channels, energies)
    fit = ROOT.TF1("calib", "pol1", min(channels), max(channels))
    graph.Fit(fit)
    
    a = fit.GetParameter(1)
    b = fit.GetParameter(0)

    return [a, b]


def calibrated_histogram(linear_fit, acquisition, n_of_bins):
    a = linear_fit[0]
    b = linear_fit[1]
    data_cal = a * (acquisition['s']/len(acquisition.active_chs)) + b

    emax = a * n_of_bins + b
    emin = b

    hist_cal = ROOT.TH1F("h_cal", "Calibrated Spectrum", n_of_bins, emin, emax)
    hist_cal.Fill(data_cal)

    return(hist_cal)
    

def calibrated_acquisition(linear_fit, acquisition, n_of_bins):
    a = linear_fit[0]
    b = linear_fit[1]
    data_cal = a * (acquisition['s']/len(acquisition.active_chs)) + b

    emax = a * n_of_bins + b
    emin = b

    return(data_cal, emin, emax)
    

def energy_resolution(hist, peak_ranges, peak_energies):
    """Calculates energy resolution. Input peak_ranges as a list of tuples. 
    Outputs a list of resolutions for the different energies."""
    resolutions = []
    for i in range (len(peak_ranges)):
        resolution_fit = ROOT.TF1("res_fit_" + str(i), "gaus", peak_ranges[i][0], peak_ranges[i][1])
        hist.Fit(resolution_fit, "R+S")

        std_dev = resolution_fit.GetParameter('Sigma')
        resolution = (2.355 * std_dev)/peak_energies[i]
        resolutions.append(resolution)

    return resolutions