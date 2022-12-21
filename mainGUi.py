
# pip3 install pysimplegui
# pip install matplotlib

import PySimpleGUI as sg
import matplotlib
import matplotlib.pyplot as plt
from core.engine import Engine, EngineObserver
from core.stats import Statistique, StatistiqueObserver, StatistiqueLongueur, StatistiquesFrequences, StatistiqueCaracteres
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading

matplotlib.use('TkAgg')
class PsaGUI(EngineObserver, StatistiqueObserver) :

    def __init__(self):
        self.window = self.create_gui()
        self.pie_figure_canvasTkAgg = None
        self.histo_figure_canvasTkAgg = None

    def notifyEngineObserver(self, notification):


        self.window.write_event_value('-NOTIFICATION-', notification)

    def notifyStatistiqueObserver(self, notification):
        pass

    def long_run(self, strategie):
        self.engine.analyze(strategie)
        self.window.write_event_value('-THREAD-', '*** The thread says.... "I am finished" ***')

    def draw_figure(self, canvas, figure):
        figureCanvasTkAgg = FigureCanvasTkAgg(figure, canvas)
        figureCanvasTkAgg.draw()
        figureCanvasTkAgg.get_tk_widget().pack(side='top', fill='both', expand=False)
        return figureCanvasTkAgg

    def draw_pie(self, entete, data, titre):
        explode = [0.3]
        explode = explode * len(data)
        # graph pie using matplotlib

        figureObject, axesObject = plt.subplots(nrows=1,ncols=1,figsize=(15,8))
        axesObject.cla() # clear the axes
        axesObject.pie(data,
                       labels=entete,
                       startangle=60,
                       autopct='%1.1f%%',
                       shadow=False,
                       explode=explode)
        axesObject.set_title(titre)
        axesObject.axis('equal')

        if self.pie_figure_canvasTkAgg != None:
            self.pie_figure_canvasTkAgg.figure.canvas._tkcanvas.destroy()

        self.pie_figure_canvasTkAgg = self.draw_figure(self.window['-PIE-'].TKCanvas, figureObject)

    def draw_hist(self, data, titre):

        figureObject, axesObject = plt.subplots(nrows=1,ncols=1,figsize=(15,8))
        char_keys = [chr(key) for key in data.keys()]
        axesObject.bar( char_keys,data.values(),width=1, color='green')
        axesObject.set_title(titre)
       # axesObject.set_yscale('log')
        figureObject.legend()
        plt.tight_layout()

        if self.histo_figure_canvasTkAgg != None:
            self.histo_figure_canvasTkAgg.figure.canvas._tkcanvas.destroy()

        self.histo_figure_canvasTkAgg= self.draw_figure(self.window['-HISTO-'].TKCanvas, figureObject)

    def create_gui(self):
        sg.theme('Green')  # Add a touch of color
        plt.style.use('Solarize_Light2')
        sg.set_options(font=("DejaVu Sans", 16))

        # Simple example of TabGroup element and the options available to it
        sg.theme('Light Green')  # Please always add color to your window

        # Selection fichier

        file_layout = [[sg.T("",background_color='Green')],
                       [sg.Text("Veuillez choisir un fichier: "), sg.Input(key="-IN2-", change_submits=True),
                        sg.FileBrowse("Ouvrir", key="-IN-TAB1")], [sg.Button("Lancer un calcul", key="-LAUNCH-")],
                       [sg.Text("Barre de Progression", size=(0,1)),sg.ProgressBar(100, 'h', size=(30, 20), k='-PROGRESS-',expand_x=True)],
                        [sg.Text("", size=(0,1), key="-STATUS-",background_color='Green', text_color='White', justification='center',expand_x=True)]
                       ]

        # Table non formatée
        # {:.2f}".format(data.items()
        data = {}
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


        tablehist_layout = [
            [sg.Table(values=data.items(),
                      headings=['Code Ascii','Char', 'Fréquence', 'Occurence'],
                      auto_size_columns=True,
                      justification='center',
                      alternating_row_color='green',
                      num_rows=55,
                      key='-TABLEH-',
                      tooltip='Statistiques du fichier',
                      expand_x=True,
                      background_color='LightGreen',
                      text_color='white')
             ]
        ]
        # Création d un camembert
        self.canvas_categories = sg.Canvas( key='-PIE-', expand_y=True, background_color='Light Green')
        pie_layout = [[self.canvas_categories]]
        # Création d un histogramme
        self.canvas_repartition = sg.Canvas( key='-HISTO-', expand_x=True, expand_y=True, background_color='Light Green')
        histo_layout = [[self.canvas_repartition]]

        tab_group = [
            [sg.TabGroup(
                [[sg.Tab('Instructions', file_layout, title_color='White', background_color='Green',
                         tooltip='Selectionner un fichier', element_justification='Left', font='Arial 10'),
                  sg.Tab('Statistiques Principales', table_layout, title_color='Black', background_color='Light Green',
                         tooltip='Statistiques principales du fichier', element_justification='center'),
                  sg.Tab('Répartition par Catégories', pie_layout, title_color='Black', background_color='Light Green',
                         tooltip='Grande Familles de caractères', element_justification='center'),
                  sg.Tab('Distribution des Caractères', histo_layout, title_color='Black',
                         background_color='Light Green',
                         tooltip='Répartition des Caractères', element_justification='center'),
                  sg.Tab('Table de Distribution', tablehist_layout, title_color='Black', background_color='Light Green',
                         tooltip='Statistiques principales du fichier', element_justification='center')
                  ]],

                tab_location='centertop',
                title_color='White', tab_background_color='Green', selected_title_color='Red',
                selected_background_color='Orange', border_width=5)
            ]
        ]

        # Define Window
        window = sg.Window("Password Statistiques Analyzer", tab_group, resizable=True, finalize=True,size=(1024, 600))
        window.bind('<Configure>', "Event")

        return window

    def display(self):

        refresh = 0

        while True:
                event, values = self.window.read()
                if event == sg.WIN_CLOSED :
                    break
                elif event == "-LAUNCH-":
                    filename=values["-IN2-"]

                    if (filename != ''):
                        #count_lines = sum(1 for line in open(filename, encoding="iso8859-1"))
                        count_lines = 0

                        self.window['-LAUNCH-'].Update(disabled=True)
                        self.window['-HISTO-'].update()
                        self.window['-PIE-'].update()
                        self.window['-TABLE-'].update(values={})
                        self.engine = Engine([Statistique.STAT_LONGUEUR, Statistique.STAT_FREQUENCES, Statistique.STAT_CARACTERES], filename=filename)
                        self.engine.register_observer(self)

                        self.window['-STATUS-'].update(value="En cours...")

                        thread = threading.Thread(target=self.long_run, args=(Engine.STRATEGIE_MULTITHREADED,), daemon=True)
                        thread.start()

                elif event == '-NOTIFICATION-':
                    notification = values['-NOTIFICATION-']
                    lines_processed = notification[EngineObserver.LINES_PROCESSED]
                    total_bytes_processed = notification[EngineObserver.TOTAL_BYTES_PROCESSED]
                    total_bytes_to_process = notification[EngineObserver.TOTAL_BYTES]

                    self.window['-PROGRESS-'].update(total_bytes_processed, total_bytes_to_process)

                    refresh += 1
                    if refresh == 10:
                        self.update_visualisation(notification[EngineObserver.CURRENT_STATISTICS_STATE], filename, lines_processed)
                        refresh = 0

                elif event == "-THREAD-":

                    self.window['-STATUS-'].update(value="Terminé")

                    lines_processed = self.engine.get_nb_lignes_traitees()

                    statistiques = self.engine.get_statistiques()
                    self.update_visualisation(statistiques, filename, lines_processed)

                    self.window['-LAUNCH-'].Update(disabled=False)


        self.window.close()

    def update_visualisation(self, statistiques, filename, count_lines):
        # traitement du resultat longueur
        stat_longueur = statistiques[Statistique.STAT_LONGUEUR]
        resultat_longueur = stat_longueur.restituer_statistiques()

        stat_generales_model = dict()
        stat_generales_model['Fichier'] = filename
        stat_generales_model[StatistiqueLongueur.LONGUEUR_MINIMUM] = resultat_longueur[
            StatistiqueLongueur.LONGUEUR_MINIMUM]
        stat_generales_model[StatistiqueLongueur.LONGUEUR_MAXIMUM] = resultat_longueur[
            StatistiqueLongueur.LONGUEUR_MAXIMUM]
        stat_generales_model[StatistiqueLongueur.LONGUEUR_MOYENNE] = round(
            resultat_longueur[StatistiqueLongueur.LONGUEUR_MOYENNE], 2)
        stat_generales_model['Nombre de Mots de passe traités'] = count_lines

        stat_caracteres = statistiques[Statistique.STAT_CARACTERES]
        resultat_caracteres = stat_caracteres.restituer_statistiques()

        stat_caracteres_model = dict()
        stat_caracteres_model[StatistiqueCaracteres.NB_SYMBOLES] = resultat_caracteres[
            StatistiqueCaracteres.NB_SYMBOLES]
        stat_caracteres_model[StatistiqueCaracteres.NB_MAJUSCULES] = resultat_caracteres[
            StatistiqueCaracteres.NB_MAJUSCULES]
        stat_caracteres_model[StatistiqueCaracteres.NB_MINUSCULES] = resultat_caracteres[
            StatistiqueCaracteres.NB_MINUSCULES]
        stat_caracteres_model[StatistiqueCaracteres.NB_NUMERIQUES] = resultat_caracteres[
            StatistiqueCaracteres.NB_NUMERIQUES]

        stat_frequences = statistiques[Statistique.STAT_FREQUENCES]
        resultat_frequences = stat_frequences.restituer_statistiques()

        nb_total_caracteres = resultat_frequences[StatistiquesFrequences.NB_CARACTERES]


        stat_frequences_model = resultat_frequences[StatistiquesFrequences.TABLEAU_FREQUENCES]

        stat_frequences_model_h = dict(stat_frequences_model)
        #for key, value in stat_frequences_model_h.items():
        #    stat_frequences_model_h[key] = format((float(value)/float(nb_total_caracteres) * 100),'.2f')

        self.window['-TABLE-'].update(values=stat_generales_model.items())
        self.draw_pie(stat_caracteres_model.keys(), stat_caracteres_model.values(), filename)
        self.draw_hist(stat_frequences_model, filename)
        self.window['-TABLEH-'].update(values=[[k, chr(k), format((float(v)/float(nb_total_caracteres) * 100),'.2f'), v] for k, v in stat_frequences_model_h.items()])



if __name__ == '__main__':
    gui = PsaGUI()
    gui.display()