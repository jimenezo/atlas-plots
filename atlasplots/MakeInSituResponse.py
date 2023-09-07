import ROOT
from ROOT import TH1F, TCanvas, TF1, TPad
import atlasplots.atlasstyle as atlasstyle
import re

def extract_number_from_string(s):
    # This function extracts a number from a string.
    match = re.search(r'\d+\.\d+', s)
    if match:
        return float(match.group())
    else:
        return None

# Set up the ATLAS plot style
atlasstyle.atlas_style()

# Open the ROOT file
root_file = ROOT.TFile.Open("../Results/InSituResponsePlots/largejet/2015_2016/InsituRespHistos_15-01-J2_jvt09_Py8_2016.root")

# Open the settings file
settings_file = open("config/HistosGammajet.data")

# Initialize the pT_bins list
pT_binning = []

# Read and parse the pT bins from the settings file
for line in settings_file:
    # Remove leading and trailing whitespaces and split the line by spaces
    parts = line.strip().split()
    
    # Skip empty lines and lines starting with '#'
    if not parts or parts[0].startswith("#"):
        continue
    
    # Check if the line starts with "pT_ref.Bins:"
    if parts[0] == "pT_ref.Bins:":
        # Append the pT bins to the list
        pT_binning.extend(map(int, parts[1:]))

# Close the settings file
settings_file.close()

# Create a canvas with two pads
canvas = TCanvas("canvas", "Data vs. MC", 800, 600)
main_pad = TPad("main_pad", "Main Plot", 0.0, 0.3, 1.0, 1.0)
ratio_pad = TPad("ratio_pad", "Ratio", 0.0, 0.0, 1.0, 0.3)
main_pad.Draw()
ratio_pad.Draw()
main_pad.cd()

# Create empty histograms for data and MC
data_histogram = TH1F("data_histogram", "Data", len(pT_binning) - 1, array('d', pT_binning))
mc_histogram = TH1F("mc_histogram", "MC", len(pT_binning) - 1, array('d', pT_binning))

# Loop over histograms in the ROOT file
for key in root_file.GetListOfKeys():
    hist_name = key.GetName()

    # Extract a number from the histogram name
    number_from_name = extract_number_from_string(hist_name)

    if number_from_name is not None:
        # Check if the histogram name contains "data" or "Py8"
        if re.search(r'(data|Py8)', hist_name):
            # Extract pT_ref values from the histogram name
            pT_ref_values = re.findall(r'pTref(\d+)_(\d+)', hist_name)
            
            if pT_ref_values:
                # pT_ref values are in the form (400, 600)
                # Extract the values from the tuple
                pT_ref_min, pT_ref_max = map(int, pT_ref_values[0])
                
                # Set the fit range based on pT_ref values
                sigma = hist.GetStdDev()
                fit_range_min = pT_ref_min - 2 * sigma
                fit_range_max = pT_ref_max + 2 * sigma
                
                # Perform a Gaussian fit within the specified range
                fit_func = TF1("fit_func", "gaus", fit_range_min, fit_range_max)
                hist.Fit(fit_func, "R")
                
                # Fill the appropriate histogram (data or MC)
                if "data" in hist_name:
                    data_histogram.Fill(number_from_name, fit_func.GetParameter(1))
                else:
                    mc_histogram.Fill(number_from_name, fit_func.GetParameter(1))

# Plot data and MC histograms on the main pad
data_histogram.SetMarkerStyle(20)
data_histogram.SetMarkerColor(ROOT.kBlack)
mc_histogram.SetLineColor(ROOT.kRed)
mc_histogram.SetFillColor(ROOT.kRed)
mc_histogram.SetFillStyle(3004)

data_histogram.Draw("E1")
mc_histogram.Draw("HIST SAME")

# Create the legend
legend = ROOT.TLegend(0.7, 0.7, 0.9, 0.9)
legend.AddEntry(data_histogram, "Data", "lep")
legend.AddEntry(mc_histogram, "MC", "f")
legend.Draw()

# Create the ratio histogram
ratio_histogram = mc_histogram.Clone("ratio_histogram")
ratio_histogram.Divide(data_histogram)

# Switch to the ratio pad
ratio_pad.cd()

# Draw the ratio histogram
ratio_histogram.SetMarkerStyle(20)
ratio_histogram.SetMarkerColor(ROOT.kBlack)
ratio_histogram.Draw("E1")

# Save the canvas
canvas.SaveAs("data_vs_mc.png")

# Close the ROOT file
root_file.Close()
