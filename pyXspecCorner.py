import argparse
import numpy as np
import pandas as pd
import arviz
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons, TextBox
from astropy.io import fits
import corner


# Use very very small fonts...
plt.rc('xtick',labelsize='xx-small')
plt.rc('ytick',labelsize='xx-small')

plt.rcParams["font.family"] = "DejaVu Serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rc('text', usetex=False)

def UpdateCornerPlot(selectedTitles, contours, showTitles, showXYlabels, selectedAltNames):
    '''Create and Update the CornerPlot based on the selectedTitles,
       and plotting options like Contours, Titles and Labels'''
    figcorner.clear()
    if showXYlabels:
        corner.corner(df, var_names=selectedTitles.values, filter_vars="like", fig=figcorner,
                  labels=selectedAltNames, label_kwargs={"fontsize": 'xx-small'},
                  titles=selectedAltNames, show_titles=showTitles, title_fmt=title_fmt, title_kwargs={"fontsize": 'xx-small'},
                  plot_datapoints=False, plot_density=True, plot_contours=contours, smooth=True,
                  quantiles=(0.14, 0.84), use_math_text=True, bins=bins, labelpad=labelpad)
    else:
        corner.corner(df, var_names=selectedTitles.values, filter_vars="like", fig=figcorner,
                  labels=[None for val in selectedTitles.values], label_kwargs={"fontsize": 'xx-small'},
                  titles=selectedAltNames, show_titles=showTitles, title_fmt=title_fmt, title_kwargs={"fontsize": 'xx-small'},
                  plot_datapoints=False, plot_density=True, plot_contours=contours, smooth=True,
                  quantiles=(0.14, 0.84), use_math_text=True, bins=bins, labelpad=labelpad)

    figcorner.canvas.draw()
    return



def chTextBoxesFunc(a):
    '''Read Selected Buttons and seamingly call
       UpdateCornerPlot to update the corner plot'''
    for i, chTextBox in enumerate(chTextBoxes):
        AltNames[i] = chTextBox.text
    contours = selected[-3]
    showTitles = selected[-2]
    showXYlabels = selected[-1]
    selectedTitles = Titles[selected]
    selectedAltNames = AltNames[selected]

    UpdateCornerPlot(selectedTitles, contours, showTitles, showXYlabels, selectedAltNames)
    return


def chButtonsFunc(a):
    '''Read Selected Buttons and seamingly call
       UpdateCornerPlot to update the corner plot'''
    for i, Title in enumerate(Titles):
        if a == Title:
            selected[i] = not selected[i]
            break
    contours = selected[-3]
    showTitles = selected[-2]
    showXYlabels = selected[-1]
    selectedTitles = Titles[selected]
    selectedAltNames = AltNames[selected]

    UpdateCornerPlot(selectedTitles, contours, showTitles, showXYlabels, selectedAltNames)
    return


if __name__ == '__main__':
    '''pyXspecCorner is a CornerPlotter for XSPEC MCMC Chains saved to FITS files'''

    # Organize the Parser to get Chain file, burn-in and samples to be used.
    parser = argparse.ArgumentParser(prog='pyXspecCorner',
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                    description='Make interactive CornerPlots based on XSPEC MCMC Chain FITS files.')

    parser.add_argument("chain", help="Path to XSPEC Chain FITS file", type=str, default='chain.fits')
    parser.add_argument("--burn", help="Samples to Burn In", type=int, default=100, nargs='?')
    parser.add_argument("--samples",help="Samples used in CornerPlot", type=int, default=1000, nargs='?')
    parser.add_argument("--bins",help="Number of Bins used in CornerPlot", type=int, default=30, nargs='?')
    parser.add_argument("--format",help="Numeric format of Titles and XYlabels in CornerPlot", type=str, default='.2f', nargs='?')
    parser.add_argument("--labelpad",help="Fractional label padding for Titles and XYlabels", type=float, default=0.05, nargs='?')
    args = parser.parse_args()

    # Use the parsed arguments to get the selected data from the Chain FITS file
    chainName = args.chain
    BurnIn = int(args.burn)
    Samples = int(args.samples)
    bins = int(args.bins)
    title_fmt = args.format
    labelpad = args.labelpad

    chain = fits.open(chainName)
    nFields = chain[1].header['TFIELDS']
    ChainLength = chain[1].header['NAXIS2']

    idx = np.random.randint(low=int(min(BurnIn,ChainLength//2)), high=ChainLength, size=int(min(Samples,ChainLength)))

    # Create the DataFrame for the CornerPlot and fill it with the Data and Titles.
    df = pd.DataFrame()
    titles, ttypes = [], []

    for i in range(nFields):
        ttype = chain[1].header['TTYPE{}'.format(i+1)]
        tform = chain[1].header['TFORM{}'.format(i+1)]
        try:
            tunit = chain[1].header['TUNIT{}'.format(i+1)]
        except:
            tunit = ''

        try:
            tname, tnum = ttype.split('__')
        except:
            tnum = str(int(tnum)+1)
            tname = 'Chi-Squared'
            tunit = ''

        ttypes.append(ttype)
        if tunit:
            title = '{}. {} [{}]'.format(tnum,tname,tunit)
        else:
            title = '{}. {}'.format(tnum,tname)

        titles.append(title)
        df[title] = chain[1].data[ttype][idx]

    # Add some Plotting abilities
    titles.append('Draw Contours')
    contours = False
    titles.append('Show Titles')
    showTitles = True
    titles.append('Show XY Labels')
    showXYlabels = False

    # Make the Titles and Pre-select Chi-square and Titles
    Titles = pd.Series(titles)
    AltNames = np.array(Titles)
    selected = [False for Title in Titles]
    selected[-4] = True
    selected[-2] = True
    selectedTitles = Titles[selected]
    selectedAltNames = AltNames[selected]

    # Create the two interactive figures and fill them: Buttons and CornerPlot
    figcorner = plt.figure()
    figbuttons = plt.figure() #subplots(1,2)

    axbuttons = plt.axes([0.01, 0.01, 0.4, 0.92])

    chButtons = CheckButtons(axbuttons, Titles, actives=selected)
    chButtons.on_clicked(chButtonsFunc)
    figbuttons.suptitle('Parameters')

    w = 0.9/len(titles)
    chTextBoxes = []
    for i, AltName in enumerate(AltNames):
        if '.' in AltName:
            axbox = plt.axes([0.55, 0.89-w*i, 0.4, 0.95*w])
            text_box = TextBox(axbox, AltName.split('. ')[0]+'. ', initial=AltName)
            text_box.on_submit(chTextBoxesFunc)
            chTextBoxes.append(text_box)

    UpdateCornerPlot(selectedTitles, contours, showTitles, showXYlabels, selectedAltNames)

    plt.show()
