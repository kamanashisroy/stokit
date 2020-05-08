Learning yfinance ap

Requirements
==============

- yfinance
- matplotlib
- mplfinance
- panda
- numpy
- colorama

Demo
=====

#### stokit port

We can select a portfolio like the following,

```
stokit port portfolio.csv
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
stokit compare --chart table
```

#### stokit quote

```
stokit quote m
```
