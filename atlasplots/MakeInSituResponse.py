import ROOT
from ROOT import TH1F, TCanvas, TF1, TPad
import atlasplots.atlasstyle as atlasstyle

def extract_number_from_string(s):
    # This function extracts a number from a string.
    import re
    match = re.search(r'\d+\.\d+', s)
    if match:
        return float(match.group())
    else:
        return None

# Set up the ATLAS plot style
atlasstyle.SetAtlasStyle()

# Open the ROOT file
root_file = ROOT.TFile.Open("your_input_file.root")

# Define the binning for the final histogram
pT_binning = [100, 200, 300, 400, 500, 600, 700]

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

    # Check if the histogram name matches your criteria
    if "data_17" in hist_name:
        # Extract a number from the histogram name
        number_from_name = extract_number_from_string(hist_name)

        if number_from_name is not None:
            # Get the histogram
            hist = root_file.Get(hist_name)
            data_histogram.Fill(number_from_name, hist.GetMean())

    elif "Py8_2017" in hist_name:
        # Extract a number from the histogram name
        number_from_name = extract_number_from_string(hist_name)

        if number_from_name is not None:
            # Get the histogram
            hist = root_file.Get(hist_name)
            mc_histogram.Fill(number_from_name, hist.GetMean())

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
