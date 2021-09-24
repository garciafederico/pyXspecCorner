## pyXspecCorner by Federico Garcia

A Python tool to make interactive [Corner Plots](https://corner.readthedocs.io/) based on XSPEC MCMC chains saved to FITS files.

### Usage:
```
   python pyXspecCorner.py 'MCMC_chain.fits'
```

### Description:

The program will open two matplotlib windows, one with a corner plot and another one with a list of CheckButtons to interactively select the parameters to be plotted in the corner plot. 

The last CheckButton in the list allows to turn on and off the smoothed 2D contours in the [Corner Plot](https://corner.readthedocs.io/).


