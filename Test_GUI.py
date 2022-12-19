import random
import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import core.engine as engine
import core.variables as variables
import core.stats as statistiques


#Données de test
NStat=3
data = {'longueur minimum' : 5,
        'longueur maximum': 9,
        'longueur moyenne': 6.916666666666667}

stat2={'nb minuscules':  192,
       'nb majuscules':  1,
       'nb numeriques':  57,
       'nb symboles':  1}
explode=[0.1]
tabs=[]

stat3={}
for i in range(255):
    c=chr(i)
    stat3[c]=random.random()*50
bin_edges=1

#Fenetre principale
window=sg.Window('Analyseur de mots de passe')

# Simple example of TabGroup element and the options available to it
sg.theme('Light Green')     # Please always add color to your window
# The tab 1, 2, 3 layouts - what goes inside the tab

File_layout = [[sg.T("")], [sg.Text("Veuillez choisir un fichier: "), sg.Input(key="-IN2-",  change_submits=True),
        sg.FileBrowse("Ouvrir", key="-IN-TAB1")], [sg.Button("Lancer le calcul")]
               ]

table_layout = [
            [sg.Table(values=contact_information_array, headings=headings, max_col_width=35,
                    auto_size_columns=True,
                    display_row_numbers=True,
                    justification='right',
                    num_rows=10,
                    key='-TABLE-',
                    row_height=35,
                    tooltip='Contacts Table')]
]

tab3_layout = [[sg.Text('Tab 3')]]
tab4_layout = [[sg.Text('Tab 4')]]



window.show()
