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
A7 00 00 00 03 00

64 00 03 00 1C 00
		
65 00 1F 00 05 00

66 00 24 00 01 00

69 00 25 00 3C 00 

69 00 61 00 1E 00

69 00 7F 00 17 00

6E 00 96 00 1A 00

73 00 B0 00 0A 00

A6 00 00 05 09 00

F4 01 09 05 17 00

F5 01 20 05 19 00
```
### What is that?
This table represents how the data are stored in memory. The Winisis uses two bytes for storing the Field Tag, where the information starts and the size of the information.

Here is a brief description:
- The first and second bytes (first and second columns) represents the tag id.
- The third and fourth bytes represents where the text starts.
- The fifth and sixth bytes represents the size of the

### Examples
On the first row we have `A7 00 00 00 03 00`.
- To get the Field Tag, first we get the two first bytes, switch it (`00 A7`), then we convert it to decimal (00A7 = 167).
- To get the initial text position, we get the bytes positions 03 and 04, invert then and convert it to decimal (in this case, `0000` = 0).
- To get the size of the text, we get the two last bytes (`03 00`), then we invert and convert it to decimal (`0003` = 3).

On the last row we have `F5 01 20 05 19 00`.
Repeating the process we did in the previous example, we have:
- `F5 01`, inverting to `01 F5`, converting it to decimal is equals to 501 (the Field Tag).
- `20 05`, inverting to `05 20`, converting it to decimal is equals to 1312 (where the data starts)
- `19 00`, inverting to `00 19`, converting it to decimal is equals to 25 (the size of the data).

This "inversion" is necessary due to the format the bytes are stored in memory (Little Endian).

It is important to convert to decimal for using with the `.fdt` file.