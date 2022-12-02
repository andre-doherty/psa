from core import Constantes


class Statistique:

    def get_type(self):
        return "unknown"

    def calculer(self):
        print("do nothing")

    def afficher_statistiques(self):
        print("do nothing")

    def restituer_statistiques(self):
        return dict()



class StatistiquesFrequences(Statistique):
    """Donnes des statistiques sur la fréquence d'usage des caractères"""

    def __init__(self):
        self.nb_caracteres = 0
        self.tab_frequence = dict()
        for i in range(256):
            self.tab_frequence[i] = 0

    def get_type(self):
        return Constantes.STAT_FREQUENCES

    def calculer(self, chaines):
        for chaine in chaines:
            for char in chaine:
                self.nb_caracteres += 1
                code = ord(char)
                self.tab_frequence[code] += 1


    def afficher_statistiques(self):
        print("Statistiques Frequences : ")
        for key in self.tab_frequence:
            str = ""
            str +=  chr(key)
            if (str.isprintable()):
                print(key, " (", str, ") ", self.tab_frequence[key], format((float(self.tab_frequence[key])/float(self.nb_caracteres) * 100),'.2f'))
            else:
                print(key, self.tab_frequence[key], format((float(self.tab_frequence[key])/float(self.nb_caracteres) * 100),'.2f'))

    def restituer_statistiques(self):
        return dict()


class StatistiqueCaracteres(Statistique):
    """Donne des statistiques sur l'usage des caractères (majuscules, minuscules, numériques, symboles"""

    def __init__(self):
        self.nb_majuscules = 0
        self.nb_minuscules = 0
        self.nb_lettres = 0
        self.nb_numeriques = 0
        self.nb_symboles = 0
        self.total_caracteres = 0

        self.cache_alpha = dict()

    def get_type(self):
        return Constantes.STAT_CARACTERES

    def isalpha(self, charactere):
        if (charactere in self.cache_alpha):
            return self.cache_alpha.get(charactere)
        else:
            value = charactere.isalpha()
            self.cache_alpha[charactere] = value
            return value

    def islower(self, charactere):
        return charactere.islower()

    def isdigit(self, charactere):
        return charactere.isdigit()

    def calculer(self, chaines):
        for chaine in chaines:
            for char in chaine:
                self.total_caracteres += 1
                if (self.isalpha(char)):
                    self.nb_lettres += 1
                    if (self.islower(char)):
                        self.nb_minuscules += 1
                    else:
                        self.nb_majuscules += 1
                else:
                    if (self.isdigit(char)):
                        self.nb_numeriques += 1
                    else:
                        self.nb_symboles += 1

    def afficher_statistiques(self):
        print("Statistiques caracteres : ")
        print("nb minuscules ", self.nb_minuscules)
        print("nb majuscules ", self.nb_majuscules)
        print("nb numeriques ", self.nb_numeriques)
        print("nb symboles ", self.nb_symboles)
        print("total analysés : ", self.total_caracteres)

    def restituer_statistiques(self):
        return dict()

class StatistiqueLongueur(Statistique):
    """Donne des statistiques sur les chaines analysees : longueur max, min, moyenne"""

    def __init__(self):
        self.longueur_minimum = 100000000
        self.longueur_maximum = 0
        self.somme_longueurs = 0
        self.nb_lignes_analysees = 0

    def get_type(self):
        return Constantes.STAT_LONGUEUR

    def calculer(self, chaines):
        for chaine in chaines:
            longueur_chaine = len(chaine)
            if (longueur_chaine < self.longueur_minimum):
                self.longueur_minimum = longueur_chaine
            if (longueur_chaine > self.longueur_maximum):
                self.longueur_maximum = longueur_chaine
            self.somme_longueurs += longueur_chaine
            self.nb_lignes_analysees += 1

    def afficher_statistiques(self):
        print("Statistiques longueur : ")
        print("longueur minimum ", self.longueur_minimum)
        print("longueur maximum ", self.longueur_maximum)
        print("longueur moyenne ", self.somme_longueurs / self.nb_lignes_analysees)

    def restituer_statistiques(self):
        return dict()
