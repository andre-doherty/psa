import random
import PySimpleGUI as sg
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
#from matplotlib import gridspec
#import core.engine as engine
#import core.variables as variables
#import core.stats as statistiques
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

matplotlib.use('TkAgg')

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    figure_canvas_agg.draw()
    return figure_canvas_agg


def draw_pie(entete, data, titre):
    explode = [0.2]
    explode = explode * len(data)
    # graph pie using matplotlib
    figureObject, axesObject = plt.subplots()
    axesObject.pie(data,
                   labels=entete,
                   startangle=90,
                   autopct='%1.1f%%',
                   shadow=True,
                   explode=explode)
    axesObject.set_title(titre)
    axesObject.axis('equal')
    draw_figure(window['-PIE-'].TKCanvas, figureObject)

def draw_hist( data,n_bins, titre):
    sg.popup(data.keys())
    sg.popup(data.values())
    #if binwidth == 0:
    #    binwidth = 1
    #n_bins = range(min(data.values()), max(data) + binwidth, binwidth

    figureObject, axesObject = plt.subplots()

    axesObject.hist(data.values(),
                   bins=n_bins, density=True, histtype='bar', color='blue', label=data.keys())
    axesObject.set_title(titre)
    for s in ['top', 'bottom', 'left', 'right']:
        axesObject.spines[s].set_visible(False)
    # Remove x, y ticks
    axesObject.xaxis.set_ticks_position('none')
    axesObject.yaxis.set_ticks_position('none')

    draw_figure(window['-HISTO-'].TKCanvas, figureObject)

#Données de test
NStat=3
data = {'longueur minimum' : 5,
        'longueur maximum': 9,
        'longueur moyenne': 6.916666666666667}

stat2={'nb minuscules':  192,
       'nb majuscules':  1,
       'nb numeriques':  57,
       'nb symboles':  1}

#frozenset((key, freeze(value)) for key, value in d.items()
stat3={0: '0.00', 1: '0.00', 2: '0.00', 3: '0.00', 4: '0.00', 5: '0.00', 6: '0.00', 7: '0.00', 8: '0.00', 9: '0.00', 10: '0.00', 11: '0.00', 12: '0.00', 13: '0.00', 14: '0.00', 15: '0.00', 16: '0.00', 17: '0.00', 18: '0.00', 19: '0.00', 20: '0.00', 21: '0.00', 22: '0.00', 23: '0.00', 24: '0.00', 25: '0.00', 26: '0.00', 27: '0.00', 28: '0.00', 29: '0.00', 30: '0.00', 31: '0.00', 32: '0.00', 33: '0.00', 34: '0.00', 35: '0.00', 36: '0.00', 37: '0.00', 38: '05.00', 39: '10.00', 40: '20.00', 41: '10.00', 42: '0.00', 43: '0.00', 44: '0.00', 45: '0.00', 46: '0.00', 47: '0.00', 48: '2.41', 49: '5.62', 50: '2.81', 51: '2.81', 52: '2.41', 53: '2.41', 54: '2.01', 55: '1.20', 56: '0.80', 57: '0.40', 58: '0.00', 59: '0.00', 60: '0.00', 61: '0.00', 62: '0.00', 63: '0.00', 64: '0.00', 65: '0.00', 66: '0.00', 67: '0.00', 68: '0.00', 69: '0.00', 70: '0.00', 71: '0.00', 72: '0.00', 73: '0.00', 74: '0.00', 75: '0.00', 76: '0.00', 77: '0.00', 78: '0.00', 79: '0.00', 80: '0.00', 81: '0.00', 82: '0.00', 83: '0.00', 84: '0.00', 85: '0.00', 86: '0.00', 87: '0.00', 88: '0.00', 89: '0.00', 90: '0.00', 91: '0.00', 92: '0.00', 93: '0.00', 94: '0.00', 95: '0.00', 96: '0.00', 97: '4.82', 98: '1.61', 99: '4.42', 100: '2.01', 101: '8.84', 102: '0.80', 103: '1.61', 104: '2.41', 105: '5.22', 106: '0.80', 107: '0.80', 108: '6.83', 109: '1.20', 110: '4.42', 111: '6.83', 112: '2.41', 113: '0.40', 114: '5.22', 115: '5.22', 116: '2.41', 117: '2.41', 118: '1.61', 119: '1.20', 120: '0.00', 121: '3.61', 122: '0.00', 123: '0.00', 124: '0.00', 125: '0.00', 126: '0.00', 127: '0.00', 128: '0.00', 129: '0.00', 130: '0.00', 131: '0.00', 132: '0.00', 133: '0.00', 134: '0.00', 135: '0.00', 136: '0.00', 137: '0.00', 138: '0.00', 139: '0.00', 140: '0.00', 141: '0.00', 142: '0.00', 143: '0.00', 144: '0.00', 145: '0.00', 146: '0.00', 147: '0.00', 148: '0.00', 149: '0.00', 150: '0.00', 151: '0.00', 152: '0.00', 153: '0.00', 154: '0.00', 155: '0.00', 156: '0.00', 157: '0.00', 158: '0.00', 159: '0.00', 160: '0.00', 161: '0.00', 162: '0.00', 163: '0.00', 164: '0.00', 165: '0.00', 166: '0.00', 167: '0.00', 168: '0.00', 169: '0.00', 170: '0.00', 171: '0.00', 172: '0.00', 173: '0.00', 174: '0.00', 175: '0.00', 176: '0.00', 177: '0.00', 178: '0.00', 179: '0.00', 180: '0.00', 181: '0.00', 182: '0.00', 183: '0.00', 184: '0.00', 185: '0.00', 186: '0.00', 187: '0.00', 188: '0.00', 189: '0.00', 190: '0.00', 191: '0.00', 192: '0.00', 193: '0.00', 194: '0.00', 195: '0.00', 196: '0.00', 197: '0.00', 198: '0.00', 199: '0.00', 200: '0.00', 201: '0.00', 202: '0.00', 203: '0.00', 204: '0.00', 205: '0.00', 206: '0.00', 207: '0.00', 208: '0.00', 209: '0.00', 210: '0.00', 211: '0.00', 212: '0.00', 213: '0.00', 214: '0.00', 215: '0.00', 216: '0.00', 217: '05.00', 218: '0.00', 219: '0.00', 220: '0.00', 221: '10.00', 222: '0.00', 223: '0.00', 224: '0.00', 225: '0.00', 226: '0.00', 227: '0.00', 228: '0.00', 229: '0.00', 230: '0.00', 231: '0.00', 232: '0.00', 233: '0.00', 234: '0.00', 235: '0.00', 236: '0.00', 237: '0.00', 238: '0.00', 239: '0.00', 240: '0.00', 241: '0.00', 242: '0.00', 243: '0.00', 244: '0.00', 245: '0.00', 246: '0.00', 247: '0.00', 248: '0.00', 249: '0.00', 250: '0.00', 251: '0.00', 252: '0.00', 253: '0.00', 254: '0.00', 255: '0.00'}


#Fenetre principale
window=sg.Window('Analyseur de mots de passe')
plt.style.use('Solarize_Light2')


# Simple example of TabGroup element and the options available to it
sg.theme('Light Green')     # Please always add color to your window


#Selection fichier

file_layout = [[sg.T("")], [sg.Text("Veuillez choisir un fichier: "), sg.Input(key="-IN2-",  change_submits=True),
        sg.FileBrowse("Ouvrir", key="-IN-TAB1")], [sg.Button("Lancer le calcul", key="-LAUNCH-")]
               ]
#Table non formatée
#{:.2f}".format(data.items()
table_layout = [
    [sg.Table(values=data.items(),
              headings=['Statistique', 'Valeur'],
              auto_size_columns=True,
              justification='center',
              alternating_row_color='green',
              num_rows=len(data),
              key='-TABLE-',
              tooltip='Statistiques du fichier',
              expand_x=True)
     ]
]


#Création d un camembert
pie_layout = [[sg.Canvas(key='-PIE-',size=(400 * 2, 400),expand_y=True, background_color='Light Green')]]
histo_layout = [[sg.Canvas(size=(400 * 2, 400), key='-HISTO-',expand_y=True, background_color='Light Green')]]

tab_group = [
    [sg.TabGroup(
        [[sg.Tab('Instructions', file_layout, title_color='White', background_color='Green',
                 tooltip='Selectionner un fichier', element_justification='Left'),
          sg.Tab('Statistiques Principales', table_layout, title_color='Black', background_color='Light Green',
                 tooltip='Statistiques principales du fichier', element_justification='center'),
          sg.Tab('Répartition par Catégories', pie_layout, title_color='Black', background_color='Light Green',
                 tooltip='Grande Familles de caractères', element_justification='center'),
          sg.Tab('Distribution des charactères', histo_layout, title_color='Black', background_color='Light Green',
                 tooltip='See all your contacts', element_justification='center')]],

        tab_location='centertop',
        title_color='White', tab_background_color='Green', selected_title_color='Red',
        selected_background_color='Orange', border_width=5)
        , sg.Button('Exit')
    ]
]




# Define Window
window = sg.Window("Password Statistiques Analyzer", tab_group)


while True:
    event, values = window.read()
    print(event, values)
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "-LAUNCH-":
                #sg.popup(values["-IN2-"], "submitted")
                inputfile=values["-IN2-"]
                count_lines = sum(1 for line in open(inputfile, encoding="iso8859-1"))
                #display_results()
                sg.popup(count_lines, " lines submitted")

                draw_pie(stat2.keys(), stat2.values(), 'Répartition par type de caractères')
                draw_hist(stat3, 255, 'Répartition des caractères')


window.close()