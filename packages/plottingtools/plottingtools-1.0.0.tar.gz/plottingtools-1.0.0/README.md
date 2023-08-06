# plottingtools
A collection of tools that I use for plotting often enough (or with enough
complexity) to necessitate creating a useful API.


## Overview
---
This package is intended to make plotting as easy as possible for simple data
science visualizations. It's essentially a wrapper around matplotlib and is
designed to simplify the process of creating quick plots. While it's certainly
not as powerful as using matplotlib directly, it hopefully makes it a lot
easier to display information quickly.

This package does not rely on (or currently support) pandas `DataFrames`, and
expects data to be in vector form (ideally a numpy `ndarray`). 


## Functionality
---
Currently, this package does the following:
- Display data as bars on a single plot
    - Single/multi color
    - Scaled by a scalar or broadcastable array-like object
    - Shown as percentages
    - Text:
        - Titles
        - legends
        - X-axis labels
        - over-bar labels
    - Examples:
        located in plottingtools/examples/bars
- Display line plots
    - Single or multiple lines
    - Formatting options for each line
    - Labeling
    - Titles
    - Simple formatting of the figure


## Installation
` pip install plottingtools `


## Updates and contribution
Keep your eyes here to see updates. Please submit issues or PRs as you see fit.

