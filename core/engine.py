import fileinput
from tqdm import tqdm

from core import variables
from core.stats import StatistiqueLongueur, StatistiqueCaracteres, StatistiquesFrequences

PAQUET = variables.PAQUET

NB_LIGNES = 0

def process(stats, entries, paquet_count):
    global NB_LIGNES
    NB_LIGNES += paquet_count
    stats[0].calculer(entries)
    stats[1].calculer(entries)
    stats[2].calculer(entries)


def analyze(filename, count_lines):

    pbar = tqdm(total=count_lines)

    global PAQUET

    stat_longueurs = StatistiqueLongueur()
    stat_characters = StatistiqueCaracteres()
    stat_frequences = StatistiquesFrequences()

    stats = [stat_frequences, stat_characters, stat_longueurs]

    with fileinput.input(files=(filename), openhook=fileinput.hook_encoded("iso8859-1")) as f:

        entries = []
        count_paquet = 0

        for line in f:
            entry = line.strip()
            entries.append(entry)
            count_paquet+=1
            if (count_paquet == PAQUET):
                pbar.update(PAQUET)
                process(stats, entries, PAQUET)
                count_paquet = 0
                entries = []

        # reste du stock
        if (count_paquet != 0):
            pbar.update(count_paquet)
            process(stats, entries, count_paquet)

    pbar.close()
    stat_longueurs.afficher_statistiques()
    stat_characters.afficher_statistiques()
    stat_frequences.afficher_statistiques()

    stats = dict()
    stats['stat_longueur'] = stat_longueurs
    stats['stat_caracteres'] = stat_characters
    stats['stat_frequences'] = stat_frequences

    return stats
