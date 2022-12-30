import os
import argparse

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

    def process_analysis(self, demanded_statistiques, paquet_size=1*1048*1024, engine_strategy=Engine.STRATEGIE_MULTIPROCESS, cores = 8):

        engine = Engine(demanded_statistiques, filename=self.filename, paquet=paquet_size, cores = cores)
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

    parser = argparse.ArgumentParser(description='Compute statistics on passwords text database.')
    parser.add_argument('--sample', help='file name')
    parser.add_argument('--cores', type=int, default=8, help='number of cores to use (multiprocessing only)')
    parser.add_argument('--strategy', choices=['lines', 'block', 'multiprocess'], default='multiprocess')
    parser.add_argument('--paquet', type=int, default=10*1024*1024, help='read block or lines at once')
    parser.add_argument('--stats', nargs="+", help='specify stats to compute : length, frequency, characters. Default all')

    args = parser.parse_args()

    sample = args.sample
    cores = args.cores
    strategy = args.strategy
    paquet = args.paquet
    stats = args.stats

    #print (sample, cores, strategy, paquet, stats)

    filesize = os.path.getsize(sample)
    if (filesize < 150*1024*1024):
        count_lines = sum(1 for line in open(sample, encoding="iso8859-1"))
    else:
        count_lines = 0 # too long to calculate

    if strategy == 'multiprocess':
        progress_mode_by_block = True
        engine_strategy = Engine.STRATEGIE_MULTIPROCESS
    elif strategy == 'block':
        progress_mode_by_block = True
        engine_strategy = Engine.STRATEGIE_BLOCK
    elif strategy == 'lines':
        progress_mode_by_block = False
        engine_strategy = Engine.STRATEGIE_LIGNE

    if stats is None:
        stats_to_compute = [Statistique.STAT_LONGUEUR, Statistique.STAT_FREQUENCES, Statistique.STAT_CARACTERES]
    else:
        stats_to_compute = []
        if 'length' in stats:
            stats_to_compute.append(Statistique.STAT_LONGUEUR)
        if 'frequency' in stats:
            stats_to_compute.append(Statistique.STAT_FREQUENCES)
        if 'characters' in stats:
            stats_to_compute.append(Statistique.STAT_CARACTERES)
    #print (stats_to_compute)

    consoleGui = ConsoleGUI(sample, count_lines, filesize, progress_by_bytes=progress_mode_by_block)
    consoleGui.process_analysis(stats_to_compute, paquet_size=paquet, engine_strategy=engine_strategy, cores=cores)

