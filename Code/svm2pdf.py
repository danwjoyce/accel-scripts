# quick PDF plot of cv2svm .CSV output
import argparse
import sys
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,
                               AutoMinorLocator)
import pandas as pd
import math

parser = argparse.ArgumentParser(description='Takes CSV output from cwa2svm \
                                                and produces a rough plot of the time series as PDF for quickly checking conversion')
parser.add_argument("source", type=str, help = "Full path to source CSV file")
parser.add_argument("out", type=str, help = "Full path to output")

args = parser.parse_args()

source_file = args.source
out_file = args.out

df = pd.read_csv(source_file)

r,c = df.shape

O_r = math.floor(math.log10(r))

if O_r <= 2:
    locx = 10
else:
    locx = 100

fig, ax = plt.subplots()
ax.plot(df['Time'], df['SVM'], 'b-')
ax.xaxis.set_major_locator(MultipleLocator(locx))
plt.xticks(rotation=90)
fig.savefig(out_file, bbox_inches='tight')
