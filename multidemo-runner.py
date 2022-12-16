from core.engine import Engine, EngineObserver
from core.stats import Statistique

from tqdm import tqdm

from core import Constantes

class MultidemoRunner(EngineObserver):

    def __init__(self, filename, line_count):
        self.filename = filename
        self.line_count = line_count
        self.pbar = tqdm(total=line_count)

    def notifyEngineObserver(self, notification):
        lines_processed = notification[EngineObserver.LINES_PROCESSED]
        self.pbar.update(lines_processed)

    def process_analysis(self, demanded_statistiques):

        engine = Engine(demanded_statistiques, filename=self.filename, paquet=50*1048*1024)
        engine.register_observer(self)

        statistiques = engine.get_statistiques()
        #stat = statistiques[Constantes.STAT_LONGUEUR]
        #stat.register_listener(self)

        #thread = threading.Thread(target=self.long_run, args=(engine,), daemon=True)
        #thread.start()
        # wait until finished
        #thread.join()
        #self.long_run(engine)

        engine = Engine([Statistique.STAT_LONGUEUR, Statistique.STAT_FREQUENCES, Statistique.STAT_CARACTERES],
                        self.filename)
        engine.analyze(Engine.STRATEGIE_MULTITHREADED)

        for statistique_name in statistiques:
            statistique = statistiques[statistique_name]
            resultat = statistique.restituer_statistiques()
            print(statistique_name)
            print(resultat)

if __name__ == '__main__':
    # sample = 'smallrock.txt'
    sample = 'rockyou.txt'
    # sample = 'c:\\users\\adohe\\Downloads\\rockyou2021.txt'

    # count_lines = sum(1 for line in open(sample ,encoding="iso8859-1"))
    count_lines = 0

    runner = MultidemoRunner(sample, count_lines)
    runner.process_analysis([Statistique.STAT_LONGUEUR, Statistique.STAT_FREQUENCES, Statistique.STAT_CARACTERES])
    #engine = Engine([Constantes.STAT_LONGUEUR, Constantes.STAT_FREQUENCES, Constantes.STAT_CARACTERES], 'rockyou.txt')
    #engine.analyze(Engine.STRATEGIE_MULTITHREADED)