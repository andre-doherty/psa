
# pip3 install pysimplegui

import PySimpleGUI as sg
import numpy as np
import matplotlib.pyplot as plt
import core.engine as engine
import core.variables as variables
import core.stats as statistiques

import sys


def display_results():
    layout = [[sg.Text("Stats Info", key="new")]]
    window = sg.Window("Second Window", layout, modal=True)
    choice = None
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

    window.close()

sg.theme('Green')  # Add a touch of color
# All the stuff inside your window.
#default text used to get a default file , to be removed before prod default_text='C:\code\smallRYou.txt',

layoutInputFile = [[sg.T("")], [sg.Text("Veuillez choisir un fichier: "), sg.Input(key="-IN2-",  change_submits=True),
        sg.FileBrowse("Ouvrir", key="-IN-")], [sg.Button("Lancer le calcul")]]
layoutOutputFile = [[sg.T("")], [sg.Text("Résultats: ")]]
    # Create the Window
window = sg.Window('Input Info', layoutInputFile)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == "Exit":
            break
        elif event == "Lancer le calcul":
            window.close()
            #sg.popup(values["-IN2-"], "submitted")
            inputfile=values["-IN2-"]
            count_lines = sum(1 for line in open(inputfile, encoding="iso8859-1"))
            #display_results()
            dict_output=engine.analyze(inputfile, count_lines)

            for x in dict_output:
                statistique = dict_output[x]
                data=statistique.restituer_statistiques()
                sg.popup(type(data))
                #sg.popup("stat", x, dir(dict_output[x]), sys.getsizeof(dict_output[x]))
                # Fausse données pour pouvoir travailler
                #data = [['longueur minimum',5],['longueur maximum',  9],['longueur moyenne' , 6.916666666666667]]
                cles = list(data.keys())
                valeurs = list(data.values())
                sg.popup(data)
                #sg.popup(len(data))


                # Create the PySimpleGUI window

                # Add the Table Element to the window
                table_layout = [[ sg.Table(values=data.items(), headings=['Statistiques', 'Valeur'], max_col_width=20,
                                 auto_size_columns=True, justification='right',
                                 alternating_row_color='lightgreen', num_rows=len(data)) ]]
                windowtbl = sg.Window('Dictionary Table',table_layout)
                while True:
                    event, values = windowtbl.read()
                    if event == sg.WIN_CLOSED:
                        break
                windowtbl.close()


