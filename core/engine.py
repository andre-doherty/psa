import fileinput
from abc import ABC, abstractmethod

from core import Constantes
from core.stats import StatistiqueLongueur, StatistiqueCaracteres, StatistiquesFrequences, Statistique

import multiprocessing as mp, os

class EngineObserver(ABC):
    LINES_PROCESSED = "lines_processed"

    @abstractmethod
    def notifyEngineObserver(self, notification):
        pass

class Engine:

    DEFAULT_PAQUET_SIZE = 1024*1024

    STRATEGIE_LIGNE = "strategie_lignes"
    STRATEGIE_BLOCK = "strategie_blocs"
    STRATEGIE_MULTITHREADED = "strategie_multithreaded"

    def __init__(self, demanded_stats, filename, paquet = DEFAULT_PAQUET_SIZE):
        self.nb_lignes = 0
        self.paquet = paquet
        self.filename = filename
        self.nb_lignes_traitees = 0

        self.observers = []

        self.statistics = dict()
        for demanded_stat in demanded_stats:
            if demanded_stat == Constantes.STAT_LONGUEUR:
                self.statistics[Constantes.STAT_LONGUEUR] = StatistiqueLongueur()
            if demanded_stat == Constantes.STAT_CARACTERES:
                self.statistics[Constantes.STAT_CARACTERES] = StatistiqueCaracteres()
            if demanded_stat == Constantes.STAT_FREQUENCES:
                self.statistics[Constantes.STAT_FREQUENCES] = StatistiquesFrequences()

    def get_statistiques(self):
        return self.statistics

    def register_observer(self, engineObserver: EngineObserver):
        self.observers.append(engineObserver)

    def unregister_observer(self, engineObserver: EngineObserver):
        self.observers.remove(engineObserver)

    def notify_observers(self, notification):
        for observer in self.observers:
            observer.notifyEngineObserver(notification)

    def _process(self, stats, entries):
        for stat in stats.values():
            stat.calculer(entries)
        if len(self.observers) != 0:
            notification = dict()
            notification[EngineObserver.LINES_PROCESSED] = len(entries)
            self.notify_observers(notification)


    # multi-process strategy
    # read block of datas, parses those into lines and process those
    def process_wrapper(self, filename, chunkStart, chunkSize):
        print("process_wrapper", filename, chunkStart, chunkSize)
        with open(filename, encoding="iso8859-1", errors='ignore') as f:
            f.seek(chunkStart)
            lines = f.read(chunkSize).splitlines()

            statistiques = dict()

            statistiques[Constantes.STAT_LONGUEUR] = StatistiqueLongueur()
            statistiques[Constantes.STAT_CARACTERES] = StatistiqueCaracteres()
            statistiques[Constantes.STAT_FREQUENCES] = StatistiquesFrequences()
            self._process(statistiques, lines)

            for statistique_name in statistiques:
                statistique = statistiques[statistique_name]
                resultat = statistique.restituer_statistiques()
                print(statistique_name)
                print(resultat)

    def chunkify(self, fname, size=1024 * 1024):
        fileEnd = os.path.getsize(fname)
        with open(fname, 'rb') as f:
            chunkEnd = f.tell()
            while True:
                chunkStart = chunkEnd
                f.seek(size, 1)
                f.readline()
                chunkEnd = f.tell()
                yield chunkStart, chunkEnd - chunkStart
                if chunkEnd > fileEnd:
                    break

    def process_multithreaded(self):

        cores = 4
        # init objects
        pool = mp.Pool(cores)
        jobs = []

        # create jobs
        for chunkStart, chunkSize in self.chunkify(self.filename, size=self.paquet):
            print (chunkStart, chunkSize)
            jobs.append(pool.apply_async(self.process_wrapper, (self.filename, chunkStart, chunkSize)))

        # wait for all jobs to finish
        for job in jobs:
            job.get()

        # clean up
        pool.close()


    # multi lines strategy :
    # read line by line and process packets of lines
    def process_multilines(self):

        with fileinput.input(files=(self.filename), openhook=fileinput.hook_encoded("iso8859-1")) as f:

            entries = []
            count_paquet = 0

            for line in f:
                entry = line.rstrip()
                entries.append(entry)
                count_paquet += 1

                # process with a whole packet of strings
                if (count_paquet == self.paquet):
                    self._process(self.statistics, entries, count_paquet)
                    count_paquet = 0
                    entries = []

            # process the leftover (not a full packet of strings)
            if (count_paquet != 0):
                self._process(self.statistics, entries, count_paquet)
    #def process_analysis(filename):

    # read blocks, parse those into lines and process those lines list
    def read_and_process_chunk(self, chunk_start, chunk_size):
        with open(self.filename, encoding="iso8859-1", errors='ignore') as f:
            f.seek(chunk_start)
            chunk = f.read(chunk_size).splitlines()
            if len(chunk) != 0:
                offset = f.tell()

                # eventually complete the last read password
                endofstring = ''
                f.seek(offset-1)
                item = f.read(1)
                #print("previous " + item)
                if (item != '\n'):
                    while True:
                        item = f.read(1)
                        if (item == '\n'):
                            break
                        endofstring += item
                    #print(endofstring)
                    chunk[-1] = chunk[-1] + endofstring
                    offset = f.tell()

                count_paquet = len(chunk)
                self._process(self.statistics, chunk, count_paquet)
                return offset
            else:
                return -1


    def process_all_chunks(self, chunk_size):
        offset = 0
        while True:
            offset = self.read_and_process_chunk(offset, chunk_size)
            if (offset == -1):
                break


    def analyze(self, strategie = STRATEGIE_LIGNE):

        if (strategie == self.STRATEGIE_BLOCK):
            self.process_all_chunks(self.paquet)
            return

        if (strategie == self.STRATEGIE_MULTITHREADED):
            self.process_multithreaded()
            return

        if (strategie == self.STRATEGIE_LIGNE):
            self.process_multilines()
            return
