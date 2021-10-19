import argparse
import numpy as np
import pandas as pd
import arviz
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons, TextBox
from astropy.io import fits
import corner
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


# Use very very small fonts...
plt.rc('xtick',labelsize='xx-small')
plt.rc('ytick',labelsize='xx-small')


def UpdateCornerPlot(selectedTitles, contours, showTitles, showXYlabels, selectedAltNames):
    '''Create and Update the CornerPlot based on the selectedTitles,
       and plotting options like Contours, Titles and Labels'''
    figcorner.clear()
    if showXYlabels:
        corner.corner(df, var_names=selectedTitles.values, filter_vars="like", fig=figcorner,
                  labels=selectedAltNames, label_kwargs={"fontsize": 'xx-small'},
                  titles=selectedAltNames, show_titles=showTitles, title_fmt=title_fmt, title_kwargs={"fontsize": 'xx-small'},
                  plot_datapoints=False, plot_density=True, plot_contours=contours, smooth=True,
                  quantiles=(0.14, 0.84), use_math_text=True, bins=bins)
    else:
        corner.corner(df, var_names=selectedTitles.values, filter_vars="like", fig=figcorner,
                  labels=[None for val in selectedTitles.values], label_kwargs={"fontsize": 'xx-small'},
                  titles=selectedAltNames, show_titles=showTitles, title_fmt=title_fmt, title_kwargs={"fontsize": 'xx-small'},
                  plot_datapoints=False, plot_density=True, plot_contours=contours, smooth=True,
                  quantiles=(0.14, 0.84), use_math_text=True, bins=bins)
   
    figcorner.canvas.draw()
    return


def UpdateAll():
    for i, selVar in enumerate(selVariables):
        selected[i] = selVar.get()
    for i, textVar in enumerate(textVariables):
        AltNames[i] = textVar.get()
    selectedTitles = Titles[selected]
    selectedAltNames = AltNames[selected]
    contours = selected[-3]
    showTitles = selected[-2]
    showXYlabels = selected[-1]

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
    args = parser.parse_args()

    # Use the parsed arguments to get the selected data from the Chain FITS file
    chainName = args.chain
    BurnIn = int(args.burn)
    Samples = int(args.samples)
    bins = int(args.bins)
    title_fmt = args.format

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
    figcorner = plt.Figure(figsize=(6,6), dpi=120)

    app = tk.Tk() 
#    app.geometry('1350x950')
    app.title('tkXspecCorner    by Federico Garcia')

    ParamTitle = tk.Label(app, text='Parameters', font="sans 12 bold")
    ParamTitle.grid(row=0, column=1, columnspan=2, rowspan=1)

    selVariables, chkButtons, textVariables, txtButtons = [], [], [], []
    for i, Title in enumerate(Titles):            
        selVariables.append(tk.BooleanVar())
        chkButton = tk.Checkbutton(app, text=Titles[i], var=selVariables[i])
        chkButtons.append(chkButton) 
        chkButton.grid(row=i+1, column=1)
        
        textVariables.append(tk.StringVar())
        textVariables[i].set(Titles[i])
        txtButton = tk.Entry(app, text=Titles[i], textvariable=textVariables[i])
        txtButtons.append(txtButton)
        txtButton.grid(row=i+1, column=2)
 
    updateButton = tk.Button(app, text='Update Corner Plot', font="sans 10 bold", command=UpdateAll)
    updateButton.grid(row=len(Titles)+1, column=1, columnspan=2, rowspan=1)
    
    canvas = FigureCanvasTkAgg(figcorner, app)
    canvas.get_tk_widget().grid(row=0,column=4,columnspan=10,rowspan=len(Titles)+1)
    toolbar = NavigationToolbar2Tk(canvas, app, pack_toolbar=False)
    toolbar.grid(row=len(Titles)+1,column=4,columnspan=10,rowspan=1)

    UpdateCornerPlot(selectedTitles, contours, showTitles, showXYlabels, selectedAltNames)
    app.mainloop()



