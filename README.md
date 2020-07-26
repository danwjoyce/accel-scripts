# Using cwa2svm v0.1
These scripts are intended to be used to batch process AX3 data with minimal user input to a format suitable for activity monitoring (in contrast to fine-grained movement studies).  

Note: they do not replace the full-featured toolsets designed by the [openmovement](https://github.com/digitalinteraction/openmovement) group.  

The basic processing pipeline implemented in `cwa2svm` is:

1. Take a CSV representation of AX3 CWA data
2. Apply Butterworth bandpass filters to the (x,y,z) accelerometer data
3. Compute the 1g-corrected SVM (Signal Vector Magnitude)
4. Downsample to windows of e.g. 30 seconds and report the mean SVM in these windows
5. Output a relatively small CSV ready for importing to your analysis tool

Of course, this can all be done with the tools in the OpenMovement [AX3-GUI](https://github.com/digitalinteraction/openmovement/wiki/AX3-GUI)

The use-case for these scripts is when for a given analysis task and a bunch of participant's `CWA` data, you want to batch process all participant's data to produce a CSV representing each participant at sample intervals and with filter parameters suitable for the analysis.  Because of this, it is not anticipated that the CSV version of the raw `CWA` data will be kept.

These scripts need testing on real-life data and this current version is experimental.

# 0 : Installation and Requirements
You'll need a working Python 3 installation and the cwa-convert tool (see below)

Download and extract this repo.  Inside you'll find:

* `Code` -- this is the location for the scripts
* `SourceData` -- place your data here for processing; it contains example ~ 24 hour recordings from an AX3 to try out the scripts
    
The first step (below) is to convert the native AX3 `.CWA` file to CSV.  To do this, you'll need to install the [cwa-convert](https://github.com/digitalinteraction/openmovement/tree/master/Software/AX3/cwa-convert/c) tool (which needs compilation on Linux and Mac).

To make life simpler, put the executable `cwa-convert` utility in the `Code` directory.

# 1 : Outline Steps

Assuming the installation above:

1. Plug the AX3 into a USB port, and copy the `.CWA` file to somewhere convenient, e.g. the `SourceData` directory
2. Convert the `CWA` file to CSV (which results in a huge file, but there's no need to keep this file after the following steps)

You can try this out on the sample data provided.  Assuming `cwa-convert` is located in the `Code` directory:
        
    ./cwa-convert ../SourceData/ex-raw.CWA -out ../SourceData/ex-raw.csv

3. Now you have a CSV version of the raw `CWA` data in `SourceData`.  
4. Run the `cwa2svm` script;  

The command line options are given by running

    python cwa2svm --h

To process the example data above, try this example:

    python cwa2svm.py ../SourceData/ex-raw.csv ../SourceData/ex-svm.csv -samplerate 100 -binsize 30T -filter yes -low 0.5 -high 20

This takes `ex-raw.csv`, saves the resulting file as `ex-svm.csv`. It assumes the samplerate was 100 Hz, sets the window to 30 minutes and applies a 4th order Butterworth filter with low / high cutoff frequencies of 0.5 and 20 Hz respectively.

You can quickly check the result with:

    python svm2pdf.py ../SourceData/ex-svm.csv ../SourceData/ex-30-mins.pdf

Which saves a rough PDF of the data to view.

# 2 : Output Format

`cva2swm` delivers data in a CSV file with columns:

    Time, Ax, Ay, Az, SVM

Where `Ax`, `Ay`, and `Az` are the filtered accelerometer axes and `SVM` the signal vector magnitude






