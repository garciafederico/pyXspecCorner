## pyXspecCorner by Federico Garcia

A Python tool to make interactive [Corner Plots](https://corner.readthedocs.io/) based on XSPEC MCMC chains saved to FITS files.

### Usage:

**Basic:** The user must provide the path/name to the MCMC XSPEC chain FITS file.
```
   python pyXspecCorner.py 'MCMC_chain.fits'
```

or alternatively
```
   python tkXspecCorner.py 'MCMC_chain.fits'
```
to get a faster version based on `tkinter`.

**Optional:** The user can also provide the burn in and/or number of samples to use for plotting purposes, and plotting parameters like the number of bins and number format.

```
   python pyXspecCorner.py 'MCMC_chain.fits' --burn 300 --samples 1000 --bins 50 --format .3f
```

**Usage help:** The user can get additional description/help using the argparse helper.
```
   python pyXspecCorner.py -h
```

### Description:

The program will open two matplotlib windows, one with a corner plot and another one with a list of CheckButtons to interactively select the parameters to be plotted in the corner plot, and edit the individual titles/labels shown in the plot.

The three last CheckButtons in the list allows to turn on and off the smoothed 2D contours in the [Corner Plot](https://corner.readthedocs.io/), and to play with Titles and XYlabels in the plot.

In the `tkinter` version, a `tk` window is opened with buttons and textboxes for every parameter, a `matplotlib` plot embedded, and a button to Update the plot when needed.
