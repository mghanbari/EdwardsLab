"""
Plot the SRA data from PARTIE. Espeically plot the percent phage + prok against percent 16S
"""

import os
import random
import sys

import matplotlib.lines
import argparse
import matplotlib.colors
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Plot the SRA data from PARTIE")
    parser.add_argument('-p', help='partie output file', required=True)
    parser.add_argument('-e', help='Experiment library file (run id\texperiment library', required=True)
    args = parser.parse_args()

    explib = {}
    with open(args.e, 'r') as f:
        for l in f:
            p = l.strip().split("\t")
            if len(p) == 1:
                p.append('OTHER')
            explib[p[0]] = p[1]

    data = {}
    experimentlibraries = {}
    with open(args.p, 'r') as f:
        for l in f:
            p = l.strip().split("\t")
            # data is unique kmers, percent 16S, percent phage, percent prok, percent prok + phage
            p[0] = p[0].replace('.sra', '')
            data[p[0]] = [float(p[2]), float(p[4]), float(p[6]), float(p[8]), float(p[6]) + float(p[8])]
            if p[0] in explib:
                if explib[p[0]] in experimentlibraries:
                    experimentlibraries[explib[p[0]]].append(p[0])
                else:
                    experimentlibraries[explib[p[0]]] = [p[0]]
            else:
                sys.stderr.write("No " + p[0] + " in exp\n")

    sra_ids = data.keys()

    # allcolors = matplotlib.colors.cnames.keys()
    allcolors = ['indigo', 'gold', 'hotpink', 'firebrick', 'indianred', 'yellow',
                 'mistyrose', 'olive', 'pink', 'tomato', 'orangered', 'navajowhite', 'lime', 'palegreen', 'greenyellow',
                 'burlywood', 'seashell', 'mediumspringgreen', 'fuchsia', 'papayawhip', 'blanchedalmond', 'chartreuse',
                 'dimgray', 'black', 'peachpuff', 'springgreen', 'aquamarine', 'white', 'orange', 'brown', 'ivory',
                 'dodgerblue', 'peru', 'lawngreen', 'chocolate', 'crimson', 'forestgreen', 'slateblue', 'cyan',
                 'mintcream', 'silver', 'antiquewhite', 'mediumorchid', 'skyblue', 'gray', 'goldenrod', 'floralwhite',
                 'moccasin', 'saddlebrown', 'grey', 'mediumvioletred', 'slategrey', 'red', 'deeppink', 'limegreen',
                 'palegoldenrod', 'plum', 'turquoise', 'lavender', 'maroon', 'yellowgreen', 'sandybrown', 'thistle',
                 'violet', 'navy', 'magenta', 'dimgrey', 'tan', 'rosybrown', 'olivedrab', 'blue', 'ghostwhite',
                 'honeydew', 'cornflowerblue', 'linen', 'powderblue', 'seagreen', 'snow', 'sienna', 'mediumblue',
                 'royalblue', 'green', 'mediumpurple', 'midnightblue', 'cornsilk', 'paleturquoise', 'bisque',
                 'slategray', 'khaki', 'wheat', 'teal', 'deepskyblue', 'salmon', 'steelblue', 'palevioletred',
                 'aliceblue', 'orchid', 'gainsboro', 'mediumseagreen', 'mediumturquoise', 'lemonchiffon', 'cadetblue',
                 'lavenderblush', 'coral', 'purple', 'aqua', 'whitesmoke', 'mediumslateblue', 'mediumaquamarine',
                 'beige', 'blueviolet', 'azure', 'oldlace']

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    labels = {}

    #for e in experimentlibraries:
    for e in ['WGS', 'AMPLICON', 'CLONE', 'OTHER', 'RNA-Seq', 'WGA']:
        col = allcolors.pop(0)
        print(e + "\t" + str(len(experimentlibraries[e])))

        phageprok = []
        sixs = []
        kms = []
        labels[col] = e

        for i in range(1000):
            r = random.randint(0, len(experimentlibraries[e]) - 1)
            phageprok.append(data[experimentlibraries[e][r]][3])
            sixs.append(data[experimentlibraries[e][r]][1])
            kms.append(data[experimentlibraries[e][r]][0])

        ax.scatter(phageprok, sixs, kms, label=e, c=col)
        ax.legend()

    # this is to get the legend on a 3D plot
    scatterproxy = []
    labeltexts = []
    for color in labels:
        scatterproxy.append(matplotlib.lines.Line2D([0], [0], linestyle="none", c=color, marker='o'))
        labeltexts.append(labels[color])

    ax.legend(scatterproxy, labeltexts, numpoints=1)

    ax.set_xlabel('Percent prokaryote')
    ax.set_ylabel('Percent 16S')
    ax.set_zlabel('Kmers')
    plt.show()
