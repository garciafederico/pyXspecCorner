import argparse
import numpy as np
import pandas as pd
import arviz
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons, TextBox
from astropy.io import fits
import corner


plt.rcParams["font.family"] = "DejaVu Serif"
plt.rcParams["mathtext.fontset"] = "dejavuserif"
plt.rc('text', usetex=False)


def UpdateCornerPlot(selectedTitles, contours, showTitles, showXYlabels, selectedAltNames):
    '''Create and Update the CornerPlot based on the selectedTitles,
       and plotting options like Contours, Titles and Labels'''
    figcorner.clear()
    if showXYlabels:
        corner.corner(df, var_names=selectedTitles.values, filter_vars="like", fig=figcorner,
                  labels=selectedAltNames, label_kwargs={"fontsize": fontSize},
                  titles=selectedAltNames, show_titles=showTitles, title_fmt=title_fmt, title_kwargs={"fontsize": fontSize},
                  plot_datapoints=False, plot_density=True, plot_contours=contours, smooth=True,
                  quantiles=(0.16, 0.50, 0.84), use_math_text=True, bins=bins, labelpad=labelpad)
    else:
        corner.corner(df, var_names=selectedTitles.values, filter_vars="like", fig=figcorner,
                  labels=[None for val in selectedTitles.values], label_kwargs={"fontsize": fontSize},
                  titles=selectedAltNames, show_titles=showTitles, title_fmt=title_fmt, title_kwargs={"fontsize": fontSize},
                  plot_datapoints=False, plot_density=True, plot_contours=contours, smooth=True,
                  quantiles=(0.16, 0.50, 0.84), use_math_text=True, bins=bins, labelpad=labelpad)

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
    parser.add_argument("--burn", help="Samples to Burn In", type=int, default=0, nargs='?')
    parser.add_argument("--samples",help="Samples used in CornerPlot (-1 to use all)", type=int, default=-1, nargs='?')
    parser.add_argument("--bins",help="Number of Bins used in CornerPlot", type=int, default=30, nargs='?')
    parser.add_argument("--format",help="Numeric format of Titles and XYlabels in CornerPlot", type=str, default='.2f', nargs='?')
    parser.add_argument("--labelpad",help="Fractional label padding for Titles and XYlabels", type=float, default=0.05, nargs='?')
    parser.add_argument("--fontSize",help="Font Size for Titles, XYTicks and XYlabels", type=str, default='xx-small', nargs='?')
    args = parser.parse_args()

    # Use the parsed arguments to get the selected data from the Chain FITS file
    chainName = args.chain
    BurnIn = int(args.burn)
    Samples = int(args.samples)
    bins = int(args.bins)
    title_fmt = args.format
    labelpad = args.labelpad
    fontSize = args.fontSize

    # Set fonts...
    plt.rc('xtick',labelsize=fontSize)
    plt.rc('ytick',labelsize=fontSize)

    chain = fits.open(chainName)
    nFields = int(chain[1].header['TFIELDS'])
    ChainLength = int(chain[1].header['NAXIS2'])

    if Samples<0:
        Samples = ChainLength
        idx = np.arange(min(BurnIn,0), ChainLength)
    else:
        idx = np.random.randint(low=min(BurnIn,0), high=ChainLength, size=Samples)

    print()
    print('===============================================')
    print(' Loading Chain: {}'.format(chainName))
    print(' Chain Length: {}'.format(ChainLength))
    print(' Number of Fields: {}'.format(nFields))
    print('===============================================')
    print(' Burning in {} samples'.format(BurnIn))
    print(' Using {} samples for plotting purposes'.format(Samples))
    print('===============================================')
    print()

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
            tt = ttype.split('__')
            if len(tt) == 3:
                tname, tmodel, tnum = tt
            elif len(tt) == 2:
                tname, tnum = tt
                tmodel = ''
            else:
                tnum = str(int(tnum)+1)
                tname = 'Chi-Squared'
                tunit = ''
                tmodel = ''
        except:
            tmodel = ''
            tunit = ''

        ttypes.append(ttype)
        if tunit and tmodel:
            title = '{} {}. {} [{}]'.format(tmodel,tnum,tname,tunit)
        elif tmodel:
            title = '{} {}. {}'.format(tmodel,tnum,tname)
        elif tunit:
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
