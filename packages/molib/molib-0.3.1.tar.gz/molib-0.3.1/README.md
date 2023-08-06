# molib
This package contains functions that I keep re-using in different packages, so I decided to publish them, in case it helps other too.

# Installation
To install molib, use pip (or similar):
```{.sourceCode .bash}
pip install molib
```

# Documentation

## Figures

### Add letter labels to all subplots in a figure.
```python
label_subplots(fig, size=14)
```

* Adjusts figure padding and left margin to make labels fit.
* Uses ```add_subfig_label``` and ```gen_sub_label```.


### Add a subplot label to an axis.
```python
add_subfig_label(ax, label, size=14)
```


### Generate the next figure label.
```python
gen_sub_label(lower=False, paren=False)
```

* Produces the next letter in the alphabet as a subfig label.
* Label can be uppercase or lowercase, with optional parentheses.


### Save plots in a directory
```python
save_plot(output_filename, proj_dir=Path.cwd(), subdir=None, fig=None)
```

* Function for saving plots (active plot or given figure) and printing a console message.
* Saves as a 300dpi png file.
* Makes plots directory if it does not
exist.
* Directory name is customizable.


## Colors
### Rescale RGB to values between 0 and 1
```python
rescale_colors(color_list)
```

### Tableau 10 Colors
```python
tableau10(index)
```

### Tableau 20 Colors
```python
tableau20(index)
```

### Tableau Color Blind 10
```python
tableau10blind(index)
```

## Logging
### Custom console logger
```python
import logging
console_logger(logging.DEBUG)
```
