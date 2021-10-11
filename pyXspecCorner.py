import argparse
import numpy as np
import pandas as pd
import arviz
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
from astropy.io import fits
import corner


# Use very very small fonts...
plt.rc('xtick',labelsize='xx-small')
plt.rc('ytick',labelsize='xx-small')


def UpdateCornerPlot(selectedTitles, contours, showTitles, showXYlabels):
    '''Create and Update the CornerPlot based on the selectedTitles,
       and plotting options like Contours, Titles and Labels'''
    figcorner.clear()
    if showXYlabels:
        corner.corner(df, var_names=selectedTitles.values, filter_vars="like", fig=figcorner,
                  labels=[''.join(title.split('. ')[1:]) for title in selectedTitles.values], label_kwargs={"fontsize": 'xx-small'},
                  titles=selectedTitles.values, show_titles=showTitles, title_kwargs={"fontsize": 'xx-small'},
                  plot_datapoints=False, plot_density=True, plot_contours=contours, smooth=True,
                  quantiles=(0.14, 0.84), use_math_text=True)
    else:
        corner.corner(df, var_names=selectedTitles.values, filter_vars="like", fig=figcorner,
                  labels=[None for val in selectedTitles.values], label_kwargs={"fontsize": 'xx-small'},
                  titles=selectedTitles.values, show_titles=showTitles, title_kwargs={"fontsize": 'xx-small'},
                  plot_datapoints=False, plot_density=True, plot_contours=contours, smooth=True,
                  quantiles=(0.14, 0.84), use_math_text=True)
   
    figcorner.canvas.draw()
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

    UpdateCornerPlot(selectedTitles, contours, showTitles, showXYlabels)
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
    args = parser.parse_args()

    # Use the parsed arguments to get the selected data from the Chain FITS file
    chainName = args.chain
    BurnIn = int(args.burn)
    Samples = int(args.samples)

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
    selected = [False for Title in Titles]
    selected[-4] = True
    selected[-2] = True
    selectedTitles = Titles[selected]

    # Create the two interactive figures and fill them: Buttons and CornerPlot
    figcorner = plt.figure()
    figbuttons, ax = plt.subplots(1)

    chButtons = CheckButtons(ax, Titles, actives=selected)
    chButtons.on_clicked(chButtonsFunc)
    figbuttons.suptitle('Parameters /// Draw Contours')

    UpdateCornerPlot(selectedTitles, contours, showTitles, showXYlabels)

    plt.tight_layout()
    plt.show()


