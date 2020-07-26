import argparse
import sys
import pandas as pd
import math
import numpy
import butterfilter as filt

parser = argparse.ArgumentParser(description='Takes raw CSV version of an AX3 CWA file and computes signal vector magnitude (SVM) \
                                                and downsamples to bins providing a mean SVM for each bin')
parser.add_argument("source", type=str, help = "Full path to source CSV file")
parser.add_argument("out", type=str, help = "Full path to output")
parser.add_argument("-samplerate", type=float, default = 100, 
                    help = "Sample rate (in Hz) of source data (default = 100Hz)")
parser.add_argument("-binsize", type=str, required = True, help = "Downsampling window -- specification from \
                            https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.resample.html. \
                            For example, -binsize 3T results in 3 minute, 30S gives 30 seconds")
parser.add_argument("-filter", type=str, required = True, choices = ['yes','no'],
                    help = "Apply 4th Order Butterworth Bandpass Filter")
parser.add_argument("-low", type=float, required = False, default = 0.5, help = "Bandpass low cutoff in Hz (default = 0.5)")
parser.add_argument("-high", type=float, required = False, default = 20, help = "Bandpass high cutoff in Hz (default = 20)")


args = parser.parse_args()

try:
    print(" ** Loading source CSV file (may take some time)")
    raw_data = pd.read_csv(args.source, names = ["Time","Ax","Ay","Az"])
except FileNotFoundError:
    print("Source file: " + args.source + " does not exist")
    sys.exit(1)

    
if args.filter == "yes":
    try:
        print(" ** Apply Butterworth Filter")
        print(" --- Low = " + str(args.low) + " Hz")
        print(" --- High = " + str(args.high) + " Hz")
        
        # Filter requirements : from https://github.com/digitalinteraction/openmovement/wiki/AX3-GUI
        raw_data['Ax'] = filt.butter_bandpass_filter(raw_data['Ax'], args.low, args.high, args.samplerate, order=4)
        raw_data['Ay'] = filt.butter_bandpass_filter(raw_data['Ay'], args.low, args.high, args.samplerate, order=4)
        raw_data['Az'] = filt.butter_bandpass_filter(raw_data['Az'], args.low, args.high, args.samplerate, order=4)
        
    except:
        print("Error Bandpass Filtering: check CSV file for compatibility, correct columns and ordering: Time, Ax, Ay, Az")
        raise
        sys.exit(1)
    
try:
    print(" ** Computing Signal Vector Magnitude")
    # derived measure of activity
    raw_data['Time'] = pd.to_datetime(raw_data['Time'])
    raw_data = raw_data.set_index('Time')
    raw_data['SVM'] = numpy.maximum(0, numpy.sqrt( raw_data['Ax']**2 + 
                                                   raw_data['Ay']**2 + 
                                                   raw_data['Az']**2 ) - 1 )
except:
    print("Error computing SVM, check CSV file for compatibility and correct columns and ordering: Time, Ax, Ay, Az")
    sys.exit(1)
 
try:
    print(" ** Downsampling")
    sub_sampled = raw_data.resample(args.binsize).mean()
except:
    print("Error dowmsampling data: check that --binsize value makes sense")
    sys.exit(1)

try:
    print(" ** Saving results as CSV")
    sub_sampled.to_csv(args.out, index = True)
except FileNotFoundError:
    print("Output file: " + args.source + " cannot be written -- check path exists")
    sys.exit(1)
    