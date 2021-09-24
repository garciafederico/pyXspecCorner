import sys
import numpy as np
import pandas as pd
import arviz
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
from astropy.io import fits
import corner

plt.rc('xtick',labelsize='xx-small')
plt.rc('ytick',labelsize='xx-small')

chainName = sys.argv[-1]
maxSamples = int(1e4)

chain = fits.open(chainName)
nFields = chain[1].header['TFIELDS']
ChainLength = chain[1].header['NAXIS2']
idx = np.random.choice(ChainLength,int(min(maxSamples,ChainLength)))

def chButtonsFunc(a):
    for i, Title in enumerate(Titles):
        if a == Title:
            selected[i] = not selected[i]
            break
    contours = selected[-1]
    selectedTitles = Titles[selected]

    figcorner.clear()
    if contours:
        corner.corner(df.loc[idx], var_names=selectedTitles.values, filter_vars="like", fig=figcorner,
                  labels=[None for val in selectedTitles.values], label_kwargs={"fontsize": 'xx-small'},
                  titles=selectedTitles.values, show_titles=True, title_kwargs={"fontsize": 'xx-small'},
                  plot_datapoints=False, plot_density=True, plot_contours=True, smooth=True)
    else:    
        corner.corner(df.loc[idx], var_names=selectedTitles.values, filter_vars="like", fig=figcorner,
                  labels=[None for val in selectedTitles.values], label_kwargs={"fontsize": 'xx-small'},
                  titles=selectedTitles.values, show_titles=True, title_kwargs={"fontsize": 'xx-small'},
                  plot_datapoints=False, plot_density=True, plot_contours=False, no_fill_contours=True)

    figcorner.canvas.draw()

    return 


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
    df[title] = chain[1].data[ttype]

titles.append('Draw Contours')
contours = False

figcorner = plt.figure()
figbuttons, ax = plt.subplots(1)

Titles = pd.Series(titles)
selected = [False for Title in Titles]
selected[-2] = True
selectedTitles = Titles[selected]

chButtons = CheckButtons(ax, Titles, actives=selected)
chButtons.on_clicked(chButtonsFunc)
figbuttons.suptitle('Parameters /// Draw Contours')

if contours:
    corner.corner(df.loc[idx], var_names=selectedTitles.values, filter_vars="like", fig=figcorner,
              labels=[None for val in selectedTitles.values], label_kwargs={"fontsize": 'xx-small'},
              titles=selectedTitles.values, show_titles=True, title_kwargs={"fontsize": 'xx-small'},
              plot_datapoints=False, plot_density=True, plot_contours=True, smooth=True)
else:    
    corner.corner(df.loc[idx], var_names=selectedTitles.values, filter_vars="like", fig=figcorner,
              labels=[None for val in selectedTitles.values], label_kwargs={"fontsize": 'xx-small'},
              titles=selectedTitles.values, show_titles=True, title_kwargs={"fontsize": 'xx-small'},
              plot_datapoints=False, plot_density=True, plot_contours=False, no_fill_contours=True)
figcorner.canvas.draw()

plt.tight_layout()
plt.show()


