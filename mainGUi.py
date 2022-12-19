
# pip3 install pysimplegui
# pip install matplotlib

import PySimpleGUI as sg
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import core.engine as engine
import core.stats as statistiques
import sys
from core.engine import Engine, EngineObserver
from core.stats import Statistique, StatistiqueObserver, StatistiqueLongueur, StatistiquesFrequences, StatistiqueCaracteres
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

matplotlib.use('TkAgg')
class PsaGUI(EngineObserver, StatistiqueObserver) :

    def __init__(self):
        self.window = self.create_gui()

    def notifyEngineObserver(self, notification):
        lines_processed = notification[EngineObserver.LINES_PROCESSED]
        self.window['-STATUS-'].update(value=lines_processed)

    def notifyStatistiqueObserver(self, notification):
        pass

    def long_run(self, strategie):
        self.engine.analyze(strategie)
        self.window.write_event_value('-THREAD-', '*** The thread says.... "I am finished" ***')

    def draw_figure(self, canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        figure_canvas_agg.draw()
        return figure_canvas_agg

    def draw_pie(self, entete, data, titre):
        explode = [0.3]
        explode = explode * len(data)
        # graph pie using matplotlib
        figureObject, axesObject = plt.subplots()
        axesObject.pie(data,
                       labels=entete,
                       startangle=60,
                       autopct='%1.1f%%',
                       shadow=False,
                       explode=explode)
        axesObject.set_title(titre)
        axesObject.axis('equal')
        self.draw_figure(self.window['-PIE-'].TKCanvas, figureObject)

    def draw_hist(self, data, titre):
        figureObject, axesObject = plt.subplots()

        axesObject.bar( data.keys(),data.values(),width=1, color='green')
        axesObject.set_title(titre)

        self.draw_figure(self.window['-HISTO-'].TKCanvas, figureObject)

    def create_gui(self):
        sg.theme('Green')  # Add a touch of color
        # All the stuff inside your window.
        # default text used to get a default file , to be removed before prod default_text='C:\code\smallRYou.txt',
        # Fenetre principale
        window = sg.Window('Analyseur de mots de passe')
        plt.style.use('Solarize_Light2')

        # Simple example of TabGroup element and the options available to it
        sg.theme('Light Green')  # Please always add color to your window

        # Selection fichier

        file_layout = [[sg.T("")],
                       [sg.Text("Veuillez choisir un fichier: "), sg.Input(key="-IN2-", change_submits=True),
                        sg.FileBrowse("Ouvrir", key="-IN-TAB1")], [sg.Button("Lancer le calcul", key="-LAUNCH-")],
                        [sg.Text("Bloc traité", size=(0,1), key="-STATUS-")]
                       ]

        # Table non formatée
        # {:.2f}".format(data.items()
        data = {'': 0}
        table_layout = [
            [sg.Table(values=data.items(),
                      headings=['Statistique', 'Valeur'],
                      auto_size_columns=True,
                      justification='center',
                      alternating_row_color='green',
                      num_rows=10,
                      key='-TABLE-',
                      tooltip='Statistiques du fichier',
                      expand_x=True,
                      background_color='LightGreen',
                      text_color='red')
             ]
        ]

        # Création d un camembert
        pie_layout = [[sg.Canvas( key='-PIE-', expand_y=True, background_color='Light Green')]]
        # Création d un histogramme
        histo_layout = [[sg.Canvas( key='-HISTO-', expand_y=True, background_color='Light Green')]]

        tab_group = [
            [sg.TabGroup(
                [[sg.Tab('Instructions', file_layout, title_color='White', background_color='Green',
                         tooltip='Selectionner un fichier', element_justification='Left'),
                  sg.Tab('Statistiques Principales', table_layout, title_color='Black', background_color='Light Green',
                         tooltip='Statistiques principales du fichier', element_justification='center'),
                  sg.Tab('Répartition par Catégories', pie_layout, title_color='Black', background_color='Light Green',
                         tooltip='Grande Familles de caractères', element_justification='center'),
                  sg.Tab('Distribution des charactères', histo_layout, title_color='Black',
                         background_color='Light Green',
                         tooltip='Répartition des Charactères', element_justification='center')]],

                tab_location='centertop',
                title_color='White', tab_background_color='Green', selected_title_color='Red',
                selected_background_color='Orange', border_width=5)
            ]
        ]

        # Define Window
        window = sg.Window("Password Statistiques Analyzer", tab_group, resizable=True, finalize=True)
        window.bind('<Configure>', "Event")
        return window

    def display(self):

        while True:
                event, values = self.window.read()
                if event == sg.WIN_CLOSED :
                    break
                elif event == "-LAUNCH-":
                    filename=values["-IN2-"]
                    count_lines = sum(1 for line in open(filename, encoding="iso8859-1"))

                    self.engine = Engine([Engine.STAT_LONGUEUR, Engine.STAT_FREQUENCES, Engine.STAT_CARACTERES], filename=filename)
                    self.engine.register_observer(self)

                    thread = threading.Thread(target=self.long_run, args=(Engine.STRATEGIE_BLOCK,), daemon=True)
                    thread.start()


                elif event == "-THREAD-":

                    statistiques = self.engine.get_statistiques()

                    # traitement du resultat longueur
                    stat_longueur = statistiques[Engine.STAT_LONGUEUR]
                    resultat_longueur = stat_longueur.restituer_statistiques()

                    data = dict()
                    data[StatistiqueLongueur.LONGUEUR_MINIMUM] = resultat_longueur[StatistiqueLongueur.LONGUEUR_MINIMUM]
                    data[StatistiqueLongueur.LONGUEUR_MAXIMUM] = resultat_longueur[StatistiqueLongueur.LONGUEUR_MAXIMUM]
                    data[StatistiqueLongueur.LONGUEUR_MOYENNE]= round(resultat_longueur[StatistiqueLongueur.LONGUEUR_MOYENNE],2)
                    data['Nombre de Mots de passe'] = count_lines

                    stat_caracteres = statistiques[Engine.STAT_CARACTERES]
                    resultat_caracteres = stat_caracteres.restituer_statistiques()

                    stat2 = dict()
                    stat2[StatistiqueCaracteres.NB_SYMBOLES] = resultat_caracteres[StatistiqueCaracteres.NB_SYMBOLES]
                    stat2[StatistiqueCaracteres.NB_MAJUSCULES] = resultat_caracteres[StatistiqueCaracteres.NB_MAJUSCULES]
                    stat2[StatistiqueCaracteres.NB_MINUSCULES] = resultat_caracteres[StatistiqueCaracteres.NB_MINUSCULES]
                    stat2[StatistiqueCaracteres.NB_NUMERIQUES] = resultat_caracteres[StatistiqueCaracteres.NB_NUMERIQUES]

                    stat_frequences = statistiques[Engine.STAT_FREQUENCES]
                    resultat_frequences = stat_frequences.restituer_statistiques()
                    # frozenset((key, freeze(value)) for key, value in d.items()

                    stat3 = resultat_frequences[StatistiquesFrequences.TABLEAU_FREQUENCES]

                    stat3 = dict(stat3)
                    for key, value in stat3.items():
                        stat3[key] = float(value)
                    self.window['-TABLE-'].update(values=data.items())
                    self.draw_pie(stat2.keys(), stat2.values(), 'Répartition par type de caractères')
                    #self.draw_hist(stat3, 255, 'Répartition des caractères')
                    self.draw_hist(stat3, 'Répartition des caractères')

        self.window.close()


if __name__ == '__main__':
    gui = PsaGUI()
    gui.display()