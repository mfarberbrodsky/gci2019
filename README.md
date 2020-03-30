# UnitPy
Unit converter created in Python for CCExtractor, Google Code-In 2019.

## Basic usage and configuration
To use the converter, simply execute it using "python UnitConverter.py value src_unit dst_unit".  
For example, "python UnitConverter 3 cm m" will convert 3 centimeters to meters.

To configure the converter, use the file conversion_table.txt. Each line in the file is in the format "src_unit dst_unit ratio", when ratio is the number a value in src_unit has to be multiplied by to be converted into dst_unit.  
For example, "h min 60" represents that converting hours to minutes requires a multiplication by 60.  
You can also configure a different path for the conversion table using the optional parameter "--table".

Here is an example showing all the features:
[![asciicast](https://asciinema.org/a/PEDeBNuH1lLjPOmCAkZmIau22.svg)](https://asciinema.org/a/PEDeBNuH1lLjPOmCAkZmIau22)

## How does it work?
First, the converter reads and parses the given conversion table and creates an undirected graph from it.  
Then, given two units, the converter tries to find a "path" between them using breadth-first-search.  
If a path is found, the ratio between the two units is computed and the converted value is printed. Otherwise, an error message is printed.
