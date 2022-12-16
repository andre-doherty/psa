from core import Constantes
from core.engine import Engine, EngineObserver
#from log4python.Log4python import log
from tqdm import tqdm

import threading

from core.stats import StatistiqueObserver

# On souhaite écrire un programme qui va ouvrir un fichier texte (rockyou.txt) contenant des mots de passe à
# raison d’un mot de passe par ligne, et produire des statistiques sur l’usage des caractères (majuscules,
# minuscules, numériques, symboles), la longueur minimale, maximale et moyenne, la fréquence d’usage des
# lettres dans ce fichier.

class ConsoleGUI(EngineObserver, StatistiqueObserver) :

    def __init__(self, filename, line_count):
        self.filename = filename
        self.line_count = line_count
        self.pbar = tqdm(total=line_count)

    def notifyEngineObserver(self, notification):
        lines_processed = notification[EngineObserver.LINES_PROCESSED]
        self.pbar.update(lines_processed)

    def notifyStatistiqueObserver(self, notification):
        #print("notified!")
        pass

    @staticmethod
    def long_run(engine):
        engine.analyze(Engine.STRATEGIE_MULTITHREADED)

    def process_analysis(self, demanded_statistiques):

        engine = Engine(demanded_statistiques, filename=self.filename, paquet=2048*1024)
        engine.register_observer(self)

        statistiques = engine.get_statistiques()
        #stat = statistiques[Constantes.STAT_LONGUEUR]
        #stat.register_listener(self)

        #thread = threading.Thread(target=self.long_run, args=(engine,), daemon=True)
        #thread.start()
        # wait until finished
        #thread.join()
        self.long_run(engine)

        for statistique_name in statistiques:
            statistique = statistiques[statistique_name]
            resultat = statistique.restituer_statistiques()
            print(statistique_name)
            print(resultat)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #sample = 'smallrock.txt'
    sample = 'rockyou.txt'
    #sample = 'c:\\users\\adohe\\Downloads\\rockyou2021.txt'

    #count_lines = sum(1 for line in open(sample ,encoding="iso8859-1"))
    count_lines = 0

    consoleGui = ConsoleGUI(sample, count_lines)
    consoleGui.process_analysis([Constantes.STAT_LONGUEUR, Constantes.STAT_FREQUENCES, Constantes.STAT_CARACTERES])
    #consoleGui.process_analysis([Constantes.STAT_FREQUENCES])

    #pbar = tqdm(total=count_lines)
    #TestLog = log("LogDemo")
    #TestLog.debug("Debug Log")
    #TestLog.info("Info Log")

