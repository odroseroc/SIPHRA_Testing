import ROOT
import numpy as np

def calibration_fit(histogram, energy_ranges, energies):
    """Function to create a linear calibration fit based on a histogram. Returns slope and constant of linear fit. 
    Inputs: Histogram to base calibration on.
    Ranges within which the peaks of the histogram are located.
    Known energies of these peaks, in MeV."""
    
    channels = []
    for i in range(len(energy_ranges)):
        cal_fit=ROOT.TF1("cal_fit_" + str(i), "gaus", energy_ranges[i][0], energy_ranges[i][1])
        hist.Fit(cal_fit, "R+S")
        channels.append(cal_fit.GetParameter('Mean'))

    channels = np.array(channels, dtype='float64')
    energies = np.array(energies, dtype='float64')

    graph = ROOT.TGraph(len(channels), channels, energies)
    fit = ROOT.TF1("calib", "pol1", min(channels), max(channels))
    graph.Fit(f)
    
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
    print(a, b)
    data_cal = a * (acquisition['s']/len(acquisition.active_chs)) + b

    emax = a * n_of_bins + b
    emin = b

    return(data_cal, emin, emax)