import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
import core.engine as engine
import core.variables as variables
import core.stats as statistiques

#Clé= nom de la stat , valeur en valeur
data = {'longueur minimum' : 5,
        'longueur maximum': 9,
        'longueur moyenne': 6.916666666666667}

tab2_layout = [
    [sg.Table(values=data.items(),
              headings=['Statistique', 'Valeur'],
              auto_size_columns=True,
              justification='center',
              alternating_row_color='green',
              num_rows=len(data))]
         ]
# show plot
windowtbl = sg.Window('Histogram and Table', tab2_layout)
while True:
    event, values = windowtbl.read()
    if event == sg.WIN_CLOSED:
        break
windowtbl.close()

stat2={'nb minuscules':  192,
       'nb majuscules':  0,
       'nb numeriques':  57,
       'nb symboles':  0}

plt.pie(stat2.values(), labels=stat2.keys())
pielayout = [[sg.Canvas(size=(400, 400), key='-CANVAS-')]]
window = sg.Window('Répartition', pielayout)
canvas = window['-CANVAS-'].TKCanvas
canvas.figure = plt.gcf()
canvas.draw()
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break

# Close the window and destroy the pie chart
window.close()
plt.close('all')
