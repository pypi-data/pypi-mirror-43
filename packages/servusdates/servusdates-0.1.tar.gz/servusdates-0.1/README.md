# servusdates
*Python3 module to check date and hour format.*

## Installation
### Install with pip
```
pip3 install -U servusdates
```

## Usage
```
In [1]: import servusdates

In [2]: servusdates.is_complete_hour("16:20:00")

Out[2]: True

In [3]: servusdates.is_date("08/10/1997")

Out[3]: (True, 'DD-MM-YYYY')
```
