# Design and Analysis of Algorithms report template

This repository is a very specific template for a report on the design and
analysis of algorithms class in the Western Parana State University (UNIOESTE).

## Juptyer Notebook

The report is written in a Jupyter Notebook, which can be found in the
`./daa_template.ipynb` file.

You can run it locally, or in online services like
[Google Colab](https://colab.research.google.com/).

## Picods library

The `picods` library is a small library that provides some useful functions for
creating plots and tables. It is used in the report for generating
visualizations.

You can use them as follows:

```python
from picods import (picoplot, picotable)

# Plotting one or more lines inside a single plot
picoplot(
    "Title", # Title of the plot
    [[x1_0, ..., x1_n],..., [xn_0, ..., xn_n]], # List of lists of x values
    [[y1_0, ..., y1_n],..., [yn_0, ..., yn_n]], # List of lists of y values
    ["label1", ..., "labeln"], # List of labels for each line
    ["red"", ..., "blue"], # List of colors for each line
    "x label", # Label for the x axis
    "y label", # Label for the y axis
)

# Plotting a table
picotable(
    "Title", # Title of the table
    [["a", "b", "c"], [1, 2, 3], [4, 5, 6]], # List of lists of values
    ["column 1", "column 2", "column 3"], # List of column labels
    ["row 1", "row 2", "row 3"], # List of row labels'
    round_digits=2, # Number of digits to round the values to
    color="blue", # Color of the table
)
```

## Pyaon library

Library for reading input files for using in the algorithms and in the report.

Each type of input file has a specific function for reading it. The functions
are separated in modules, each module for a specific type of input file.

You can use them as follows:

```python
from pyaon.hashing import (dump, load)

# read file1.txt, which  is a file with a list of integers
my_list_of_integers = load("file1.txt")

# write my_list_of_integers to file2.txt
dump(my_list_of_integers, "file2.txt")
```

## Pydaa library

Library that implements the algorithms being analyzed in the report.

Each algorithm is implemented in a specific module and is unique to that
specific use case.

some examples are:

```python
from pydaa.hashing import (open_addressing_hash_table, separate_chaining_hash_table)

# create a hash table with open addressing
my_hash_table = open_addressing_hash_table(10, lambda x: x % 10)

# create a hash table with separate chaining
my_hash_table = separate_chaining_hash_table(10, lambda x: x % 10)

# insert a value in the hash table
my_hash_table.insert(1)
```

## Conclusion

You can use these libraries and frameworks to write your own report, For
example, the pipeline that I use is:

1. Write the algorithms in the `pydaa` library
1. Read the input files with the `pyaon` library
1. Run the algorithms, and get the output (usually time usage)
1. With the output, create the plots and tables with the `picods` library
1. Write the report in the `daa_template.ipynb` notebook
1. Use some tool to export the notebook to PDF

You can find an example of this pipeline in the `./analysis.py` file.
