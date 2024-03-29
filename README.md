## py(tk)XspecCorner by Federico Garcia

A Python tool to make interactive [Corner Plots](https://corner.readthedocs.io/) based on XSPEC MCMC chains saved to FITS files.

![screenshot tkXspecCorner.py](screenshot_tk.png)

and/or

![screenshot pyXspecCorner.py](screenshot.png)

### Description:

The program will open two `matplotlib` windows, one with a corner plot and another one with a list of `CheckButtons` and `TextBoxes` to interactively select the parameters to be plotted in the corner plot, and edit the individual titles/labels shown.

The three last `CheckButtons` in the list allow to turn on and off the smoothed 2D `contours` in the [Corner Plot](https://corner.readthedocs.io/), and to play with `Titles` and `XYlabels` in the plot.

The program also displays a summary with the main statistics of the available parameters in the chain file using the samples selected by the user.

In the `tkinter` version, a `tk` window is opened with `buttons` and `textboxes` for every parameter, a `matplotlib` plot embedded, and a button to Update the plot when needed.

### Usage:

**Basic:** The user must provide the `path/name` to the MCMC XSPEC chain FITS file.
```
   python pyXspecCorner.py 'MCMC_chain.fits'
```

or alternatively
```
   python tkXspecCorner.py 'MCMC_chain.fits'
```
to get a faster version based on `tkinter`.

**Optional:** The user can also provide the burn in and/or number of samples to use for plotting purposes, and plotting parameters like the number of bins, number format, and label padding

```
   python pyXspecCorner.py 'MCMC_chain.fits' --burn 300 --samples 1000 --bins 50 --format .3f --labelpad 0.1
```

**Usage help:** The user can get additional `description/help` using the argparse helper.
```
   python pyXspecCorner.py -h
```

