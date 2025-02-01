# Winisis Dump

## Files Description
| Extension | Description |
|-|-|
| `.fdt` | Contains table information (tag id, input type etc) |
| `.mst` | Contains all data |
| `.val` | Contains all pick list data |

## File Encoding
The file enconding used in Winisis is CP 437.

## The `.mst` File
The `.mst` contains all records saved on Winisis.
It has a header with the following format

```Hex
A7 00 00 00 03 00 = SZ 03

64 00 03 00 1C 00 = SZ 28
		
65 00 1F 00 05 00 = SZ 05

66 00 24 00 01 00 = SZ 01

69 00 25 00 3C 00 

69 00 61 00 1E 00

69 00 7F 00 17 00

6E 00 96 00 1A 00

73 00 B0 00 0A 00

A6 00 00 05 09 00

F4 01 09 05 17 00

F5 01 20 05 19 00
```

The first and second bytes (first and second columns) represents the tag id.

### Examples
On the first row we have `A7 00`.
To convert it to decimal, first we switch these two bytes to `00 A7`, then we convert it to decimal (00A7 = 167).

The last row you will find the hex value `F5 01`. To convert it into a decimal value, we first switch these two bytes to `01 F5`, then we convert it to decimal (01F5 = 501).

This "inversion" is necessary due to the format the bytes are stored in memory (Little Endian).

It is important to convert to decimal for using with the `.fdt` file.