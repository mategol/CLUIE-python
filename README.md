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

> Next, you can start adding columns to your menu (in this case, we will make menu for file selection):
```python
gui.add_column('Name:', 'auto')
gui.add_column('Size:', 6)
```
`1st argument` sets label of created column.<br />
`2nd argument` sets column width.<br />

or multiple columns declared in one line:

```python
gui.add_column([['Name:', 'auto'], ['Size:', 8]])
# or
gui.add_column([
    ['Name:', 'auto'],
    ['Size:', 8]
])
```
`1st argument` is list with desired columns in following syntax -> `[[LABEL, WIDTH], [LABEL, WIDTH] ... ]`<br /><br />

> Now, you can fill the menu with rows:
```python
gui.add_row(['requirements.txt', '1KB'], '#requirements')
gui.add_row(['main.py', '56KB'], '#main')
gui.add_row(['funnymeme.png', '2MB'], '#meme')
```
`1st argument` contains full row as list with single cells. Whole list is whole row, and single list-element is single cell.<br />
`2nd argument` is declared row-ID that will be useful later. Left empty sets ID to *None*<br /><br />

> There are several configurable settings that allow you to customize the menu as you want:
```yaml
margin_left: Sets blank space on the left of menu
margin_right: Sets blank space on the right of menu
margin_top: Sets blank space above the menu (you can also add content there)
margin_bottom: Sets blank space under the menu (you can also add content there)
top_header: Sets content of the blank space above the menu
bottom_footer: Sets content of the blank space under the menu
pointer: Character pointing selected item
column_label_margin: Sets column label offset
row_entry_margin: Sets row entry offset
list_scroll_margin: Hard to explain, shown below
```
<br />

> How do you configure settings?
```python
gui.configure('margin_left', 1)
```
`1st argument` is setting that you want to change<br />
`2nd argument` is new value of specified setting<br />

or multiple settings in one line:
```python
gui.configure([['margin_left', 1], ['margin_right', 1]])
# or
gui.configure([
    ['margin_left', 1],
    ['margin_right', 1]
])
```
`1st argument` is setting that you want to change<br />
`2nd argument` is new value of specified setting<br />











