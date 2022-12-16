import multiprocessing as mp,os
from abc import ABC, abstractmethod

from core import Constantes
from core.stats import StatistiqueLongueur, StatistiqueCaracteres, StatistiquesFrequences, Statistique

class EngineObserver(ABC):
    LINES_PROCESSED = "lines_processed"

    @abstractmethod
    def notifyEngineObserver(self, notification):
        pass

class Multidemo:
    DEFAULT_PAQUET_SIZE = 1024 * 1024

    STRATEGIE_LIGNE = "strategie_lignes"
    STRATEGIE_BLOCK = "strategie_blocs"
    STRATEGIE_MULTITHREADED = "strategie_multithreaded"

    def __init__(self, demanded_stats, filename, paquet=DEFAULT_PAQUET_SIZE):
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

    def process_wrapper(self, chunkStart, chunkSize):
        with open("rockyou.txt", encoding="iso8859-1", errors='ignore') as f:
            f.seek(chunkStart)
            lines = f.read(chunkSize).splitlines()
            self._process(self.statistics, lines)


    def chunkify(self, fname,size=1024*1024):
        fileEnd = os.path.getsize(fname)
        with open(fname,'rb') as f:
            chunkEnd = f.tell()
            while True:
                chunkStart = chunkEnd
                f.seek(size,1)
                f.readline()
                chunkEnd = f.tell()
                yield chunkStart, chunkEnd - chunkStart
                if chunkEnd > fileEnd:
                    break

    def launch(self):
        #init objects
        cores = 4
        pool = mp.Pool(cores)
        jobs = []

        #create jobs
        for chunkStart,chunkSize in self.chunkify("rockyou.txt"):
            jobs.append( pool.apply_async(self.process_wrapper,(chunkStart,chunkSize)) )

        #wait for all jobs to finish
        for job in jobs:
            job.get()

        #clean up
        pool.close()


#if __name__ == '__main__':
#    multidemo = Multidemo()
#    multidemo.launch()