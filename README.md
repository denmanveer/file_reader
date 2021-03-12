## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info
This project is a simple reader script written in Python. This reads csv or json files and then prints analysis based on it.

## Technologies
Project is created with:
* Python: 3.7.6
* Pandas: 1.0.3

## Setup

First install following packages:
```
$ sudo apt update
$ sudo apt install python3.7
$ sudo pip3 install pandas

```

Things to change:
* Edit the shebang of the script to your interpreter path.

To run this project:
```
csv_json_reader.py --file <path of csv or json file>
```

Sample Output:
```
# ./csv_json_reader.py --file pop_sample.json
Average siblings: 2

Favourite foods:
- Pizza           60
- Ice Cream       58
- Meatballs       55

Births per Month:
- January     839
- February    2
- March       10
- April       16
- May         7
- June        19
- July        8
- August      12
- September   32
- October     0
- November    31
- December    24

```

******
