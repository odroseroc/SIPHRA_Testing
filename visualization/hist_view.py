import ROOT

# COLORS = [ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kAzure, ROOT.kSpring, ROOT.kPink, ROOT.kMagenta, ROOT.kTeal, ROOT.kYellow, ROOT.kViolet, ROOT.kCyan]

COLORS = [ROOT.kAzure-7, ROOT.kOrange+1, ROOT.kRed-7, ROOT.kCyan-5, ROOT.kGreen-5, ROOT.kOrange-4, ROOT.kMagenta-5, ROOT.kRed-9, ROOT.kOrange-7, ROOT.kGray+1]

def hist_quickShow(hists, color_offset=0, tone_offset=0):
    l_colors = len(COLORS)
    if ROOT.gROOT.FindObject('cv'):
        ROOT.gROOT.FindObject('cv').Close()

    cv = ROOT.TCanvas('cv', 'cv', 800, 600)

    ROOT.gStyle.SetOptStat(11)
    ROOT.gStyle.SetStatFontSize(0.03)
    ROOT.gStyle.SetStatW(0.16)

    list(hists)
    counter = 0

    for hist in hists:
        hist.SetLineColor(COLORS[counter % l_colors + color_offset] + counter // l_colors + tone_offset)
        if counter == 0:
            hist.Draw('hist')
        else:
            hist.Draw('hist sames')
        counter += 1
    cv.SetLogy()
    cv.Draw()
    return cv