import os

from core.engine import Engine, EngineObserver
#from log4python.Log4python import log
from tqdm import tqdm
from core.stats import StatistiqueObserver, Statistique

# On souhaite écrire un programme qui va ouvrir un fichier texte (rockyou.txt) contenant des mots de passe à
# raison d’un mot de passe par ligne, et produire des statistiques sur l’usage des caractères (majuscules,
# minuscules, numériques, symboles), la longueur minimale, maximale et moyenne, la fréquence d’usage des
# lettres dans ce fichier.

class ConsoleGUI(EngineObserver, StatistiqueObserver) :

    def __init__(self, filename, line_count, file_size, progress_by_bytes=True):
        self.filename = filename
        self.line_count = line_count
        self.total_bytes = file_size

        if progress_by_bytes == True:
            self.pbar = tqdm(total=self.total_bytes)
            self.update_per_byte = True
        else:
            self.pbar = tqdm(total=self.line_count)
            self.update_per_byte = False

        self.total_lines_processed = 0
        self.total_bytes_processed = 0


    def notifyEngineObserver(self, notification):
        lines_processed = notification[EngineObserver.LINES_PROCESSED]
        self.total_lines_processed += lines_processed

        bytes_processed = notification[EngineObserver.BYTES_PROCESSED]
        self.total_bytes_processed += bytes_processed

        if self.update_per_byte:
            self.pbar.update(bytes_processed)
            #print (self.total_bytes_processed, "total=", self.total_bytes)
        else:
            self.pbar.update(lines_processed)
            #print (lines_processed, "total=", self.total_lines_processed)



    def notifyStatistiqueObserver(self, notification):
        #print("notified!")
        pass

    @staticmethod
    def long_run(engine):
        engine.analyze(Engine.STRATEGIE_LIGNE)

    def process_analysis(self, demanded_statistiques, paquet_size=1*1048*1024, engine_strategy=Engine.STRATEGIE_MULTITHREADED):

        engine = Engine(demanded_statistiques, filename=self.filename, paquet=paquet_size)
        engine.register_observer(self)

        statistiques = engine.get_statistiques()
        #stat = statistiques[Constantes.STAT_LONGUEUR]
        #stat.register_listener(self)

        #thread = threading.Thread(target=self.long_run, args=(engine,), daemon=True)
        #thread.start()
        # wait until finished
        #thread.join()
        #self.long_run(engine)
        engine.analyze(engine_strategy)

        for statistique_name in statistiques:
            statistique = statistiques[statistique_name]
            resultat = statistique.restituer_statistiques()
            print(statistique_name)
            print(resultat)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #sample = 'smallrock.txt'
    sample = 'rockyou.txt'
    #sample = 'rockyou2021.txt'

    #count_lines = sum(1 for line in open(sample ,encoding="iso8859-1"))
    filesize = os.path.getsize(sample)
    if (filesize < 100*1024*1024):
        count_lines = sum(1 for line in open(sample, encoding="iso8859-1"))
    else:
        count_lines = 0 # too long to calculate

    consoleGui = ConsoleGUI(sample, count_lines, filesize, progress_by_bytes=False)
    consoleGui.process_analysis([Statistique.STAT_LONGUEUR, Statistique.STAT_FREQUENCES, Statistique.STAT_CARACTERES],
                                    paquet_size=2*1024*1024, engine_strategy=Engine.STRATEGIE_MULTITHREADED)
    #consoleGui.process_analysis([Constantes.STAT_FREQUENCES])

    #pbar = tqdm(total=count_lines)
    #TestLog = log("LogDemo")
    #TestLog.debug("Debug Log")
    #TestLog.info("Info Log")

