# CLUIE-python
Python Command-Line User-Interface Engine made to give you an option to create Graphical-Interface in console application.<br /><br />

# Installation
`pip install cluie` - remember that this package <b>supports only Windows OS</b> currently.<br /><br />

# Quick start
> First of all, you need to initialize the engine with:
```python
import CLUIE
gui = CLUIE.engine('FramedList', '50x20', 'ARROWSE')
```
`1st argument` specifies GUI model. All models are listed and described further below.<br />
`2nd argument` sets resolution in console-characters "units" (50 characters wide and 20 characters tall in this case).<br />
`3rd argument` sets controlling key-setup. 'ARROWSE' means that you navigate by arrows and submit with ENTER.<br /><br />

> Next, you can start adding columns to your menu:
```python
gui.add_column('Name:', 'auto')
gui.add_column('Size:', 6)
```
`1st argument` sets label of created column.<br />
`2nd argument` sets column width.<br /><br />

> Now, you can fill the menu with rows:
```python
gui.add_row(['requirements.txt', '1KB'])
gui.add_row(['main.py', '56KB'])
gui.add_row(['funnymeme.png', '2MB'])
```
`1st argument` contains full row as list with single cells. Whole list is whole row, and single list-element is single cell.<br />

