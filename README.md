Learning yfinance ap

Requirements
==============

- yfinance
- matplotlib
- mplfinance
- panda
- numpy
- colorama
- sklearn
- scikit

Demo
=====

#### stokit port

We can select a portfolio like the following,

```
stokit port watchlist.csv
```

or

```
stokit port cruiselines.csv
```

#### stokit import

It is possible import exported csv file from broker(currently chase is supported).

```
stokit import chase_positions.csv
```

#### stokit pull

Download all the data from yahoo-finance.

```
stokit pull
```

#### stokit status

```
stokit status
```

It is also possible to visualize as pie or bar or doughnut .

```
stokit status --chart bar
```

or 

```
stokit status --chart bar doughnut
```

#### stokit compare

This tool is useful to compare multiple stocks before we buy or sell.

```
stokit compare
```

Or we can check it visually,

```
stokit compare --chart heat
```

#### stokit quote

```
stokit quote m
```
