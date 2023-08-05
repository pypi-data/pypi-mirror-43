# tablat
---

[![PyPI version](https://badge.fury.io/py/tablat.svg)](https://badge.fury.io/py/tablat)
[![PyPI version](https://img.shields.io/github/license/salpreh/tablat.svg)](https://img.shields.io/github/license/salpreh/tablat.svg)

**A simple way to print output in a table**

### Basic usage
Just create a `Table` object and give it a headers list and the data. The number of columns will be calculated from the number of headers.

#### Code sample
```py
from pathlib import Path
from tablat import Table

folder_path = Path('./')
header = ['FILE_NAME', 'FOLDER', 'FILES_IN']
data = []

for file_path in folder_path.iterdir():
    data.append(file_path.name)
    if file_path.is_dir():
        data.extend(['YES', len([f for f in file_path.iterdir()])])

    else:
        data.extend(['NO', 0])

my_table = Table(data, header)
my_table.print_table()
```
*Note: `print(my_table)` is also valid*

#### Output
<img src="https://raw.githubusercontent.com/salpreh/tablat/master/assets/tablat_output.png" alt="table_output">


### Installation
You can intall the package using [pip](https://pip.pypa.io/en/stable/) (Python Package Installer)
```sh
pip install tablat
```
or
```sh
python -m pip install tablat
```

### Usage

#### Creating and modifying `Table`

`Table` object can be initialized with the data or empty:
```py
my_table = Table(data=my_data, headers=my_headers)
```
If it is initialized empty it can be modified or updated later:
```py
my_table = Table()
my_table.headers = ['FILE_NAME', 'IS_DIR']
my_table.table_data = ['My docs', True, 'profile_pic.png', False]
```
Table data can be expanded anytime:
```py
for file_path in Path('./').iterdir():
  my_table.add_data([file_path.name, file_path.is_dir()])
```

#### Syling the table with `TabStyle`

`TabStyle` class is used to encapsulate style options for the table. Current values are:

- Table borders
- Row separators
- Column separators

*Note: default style is **with borders** and **no separators** for rows and columns*

Using `TabStyle` to configure the style:
```py
form tablat import Table, TabStyle


# Style object with no borders and row separators
pref_style = TabStyle(borders=False, row_sep=True)
.
.
.
# Initializing Table with our prefered style
some_tab = Table(data, headers, pref_style)
.
.
.
# Restoring Table default style
some_tab.style = TabStyle()
```

`Table` objects are initialized with a default `TabStyle` that can be modified
```py
my_table = Table()

# Disabling borders
my_table.syle.borders = False

# Modifying style properties at once
my_table.style.update(col_sep=True, row_sep=True)
```

#### Sample table with style modifications
<img src="https://raw.githubusercontent.com/salpreh/tablat/master/assets/full_tab.png" alt="table with borders and separators">
<img src="https://raw.githubusercontent.com/salpreh/tablat/master/assets/col_sep.png" alt="table with row separators">

<img src="https://raw.githubusercontent.com/salpreh/tablat/master/assets/borders_cols.png" alt="table with borders and column separator">
<img src="https://raw.githubusercontent.com/salpreh/tablat/master/assets/clean_tab.png" alt="table with no borders nor separators">


#### Additional Notes
You can retrieve data form the table using indices

```py
# Get first row data
my_table[0]

# Get third row, second column
my_table[2][1]
```
