## pyXspecCorner by Federico Garcia

A Python tool to make interactive [Corner Plots](https://corner.readthedocs.io/) based on XSPEC MCMC chains saved to FITS files.

### Usage:

**Basic:** The user must provide the path/name to the MCMC XSPEC chain FITS file.
```
   python pyXspecCorner.py 'MCMC_chain.fits'
```

**Optional:** The user can also provide the burn in and/or number of samples to use for plotting purposes.

```
   python pyXspecCorner.py 'MCMC_chain.fits' burn 300 samples 1000
```

**Usage help:** The user can get additional description/help using the argparse helper.
```
   python pyXspecCorner.py -h
```

### Description:

The program will open two matplotlib windows, one with a corner plot and another one with a list of CheckButtons to interactively select the parameters to be plotted in the corner plot. 

The lasts CheckButtons in the list allows to turn on and off the smoothed 2D contours in the [Corner Plot](https://corner.readthedocs.io/), and to play with Titles and XYlabels in the plot.


