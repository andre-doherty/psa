import fileinput
from tqdm import tqdm

# On souhaite écrire un programme qui va ouvrir un fichier texte (rockyou.txt) contenant des mots de passe à
# raison d’un mot de passe par ligne, et produire des statistiques sur l’usage des caractères (majuscules,
# minuscules, numériques, symboles), la longueur minimale, maximale et moyenne, la fréquence d’usage des
# lettres dans ce fichier.


class Statistique:

    def calculer(self):
        print("do nothing")

    def restituer_statistiques(self):
        print("do nothing")

class StatistiquesFrequences(Statistique):
    """Donnes des statistiques sur la fréquence d'usage des caractères"""

    def __init__(self):
        self.nb_caracteres = 0
        self.tab_frequence = dict()
        for i in range(256):
            self.tab_frequence[i] = 0

    def calculer(self, chaine):
        for char in chaine:
            self.nb_caracteres += 1
            code = ord(char)
            self.tab_frequence[code] += 1


    def restituer_statistiques(self):
        print("Statistiques Frequences : ")
        for key in self.tab_frequence:
            str = ""
            str +=  chr(key)
            if (str.isprintable()):
                print(key, " (", str, ") ", self.tab_frequence[key], format((float(self.tab_frequence[key])/float(self.nb_caracteres) * 100),'.2f'))
            else:
                print(key, self.tab_frequence[key], format((float(self.tab_frequence[key])/float(self.nb_caracteres) * 100),'.2f'))



class StatistiqueCaracteres(Statistique):
    """Donne des statistiques sur l'usage des caractères (majuscules, minuscules, numériques, symboles"""

    def __init__(self):
        self.nb_majuscules = 0
        self.nb_minuscules = 0
        self.nb_lettres = 0
        self.nb_numeriques = 0
        self.nb_symboles = 0
        self.total_caracteres = 0

    def calculer(self, chaine):
        for char in chaine:
            self.total_caracteres += 1
            if (char.isalpha()):
                self.nb_lettres += 1
                if (char.islower()):
                    self.nb_minuscules += 1
                else:
                    self.nb_majuscules += 1
            else:
                if (char.isdigit()):
                    self.nb_numeriques += 1
                else:
                    self.nb_symboles += 1

    def restituer_statistiques(self):
        print("Statistiques caracteres : ")
        print("nb minuscules ", self.nb_minuscules)
        print("nb majuscules ", self.nb_majuscules)
        print("nb numeriques ", self.nb_numeriques)
        print("nb symboles ", self.nb_symboles)
        print("total analysés : ", self.total_caracteres)


class StatistiqueLongueur(Statistique):
    """Donne des statistiques sur les chaines analysees : longueur max, min, moyenne"""

    def __init__(self):
        self.longueur_minimum = 100000000
        self.longueur_maximum = 0
        self.somme_longueurs = 0
        self.nb_lignes_analysees = 0

    def calculer(self, chaine):
        longueur_chaine = len(chaine)
        if (longueur_chaine < self.longueur_minimum):
            self.longueur_minimum = longueur_chaine
        if (longueur_chaine > self.longueur_maximum):
            self.longueur_maximum = longueur_chaine
        self.somme_longueurs += longueur_chaine
        self.nb_lignes_analysees += 1

    def restituer_statistiques(self):
        print("Statistiques longueur : ")
        print("longueur minimum ", self.longueur_minimum)
        print("longueur maximum ", self.longueur_maximum)
        print("longueur moyenne ", self.somme_longueurs / self.nb_lignes_analysees)

    # Press Maj+F10 to execute it or replace it with your code.


nb_lignes = 0


def process(line):
    global nb_lignes
    nb_lignes = nb_lignes + 1


def analyze(filename, count_lines):

    pbar = tqdm(total=count_lines)

    global nb_lignes

    stat_longueurs = StatistiqueLongueur()
    stat_characters = StatistiqueCaracteres()
    stat_frequences = StatistiquesFrequences()

    with fileinput.input(files=(filename), openhook=fileinput.hook_encoded("iso8859-1")) as f:
        for line in f:
            entry = line.strip()
            pbar.update(1)
            process(line)
            stat_longueurs.calculer(entry)
            stat_characters.calculer(entry)
            stat_frequences.calculer(entry)
    print(nb_lignes)
    pbar.close()
    stat_longueurs.restituer_statistiques()
    stat_characters.restituer_statistiques()
    stat_frequences.restituer_statistiques()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    count_lines = sum(1 for line in open('rockyou.txt' ,encoding="iso8859-1"))
    analyze('rockyou.txt', count_lines)