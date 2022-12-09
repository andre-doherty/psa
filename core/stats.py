from abc import abstractmethod, ABC

from core import Constantes


class StatistiqueObserver(ABC):
    @abstractmethod
    def notifyStatistiqueObserver(self):
        pass

class Statistique:

    def __init__(self):
        self.observers = []

    def register_listener(self, observer):
        self.observers.append(observer)

    def unregister_listener(self, observer):
        self.observers.remove(observer)

    def notify_observer(self):
        for observer in self.observers:
            observer.notifyStatistiqueObserver()

    @abstractmethod
    def get_type(self):
        pass

    @abstractmethod
    def calculer(self, chaines):
        pass

    @abstractmethod
    def restituer_statistiques(self):
        pass


class StatistiquesFrequences(Statistique):
    """Donne des statistiques sur la fréquence d'usage des caractères"""

    TABLEAU_FREQUENCES = "tableau_frequence"

    def __init__(self):
        self.nb_caracteres = 0
        self.tab_frequence = dict()
        for i in range(256):
            self.tab_frequence[i] = 0

        Statistique.__init__(self)

    def get_type(self):
        return Constantes.STAT_FREQUENCES

    def calculer(self, chaines):
        for chaine in chaines:
            for char in chaine:
                self.nb_caracteres += 1
                code = ord(char)
                self.tab_frequence[code] += 1

    def restituer_statistiques(self):

        tableau_frequences = dict()
        for key in self.tab_frequence:
            tableau_frequences[key] = format((float(self.tab_frequence[key])/float(self.nb_caracteres) * 100),'.2f')

        resultat = dict()
        resultat[StatistiquesFrequences.TABLEAU_FREQUENCES] = tableau_frequences
        return resultat


class StatistiqueCaracteres(Statistique):
    """Donne des statistiques sur l'usage des caractères (majuscules, minuscules, numériques, symboles"""

    NB_MAJUSCULES = "nb_majuscules"
    NB_MINUSCULES = "nb_minuscules"
    NB_NUMERIQUES = "nb_numeriques"
    NB_SYMBOLES = "nb_symboles"
    TOTAL_CARACTERES = "total_caracteres"

    def __init__(self):
        self.nb_majuscules = 0
        self.nb_minuscules = 0
        self.nb_lettres = 0
        self.nb_numeriques = 0
        self.nb_symboles = 0
        self.total_caracteres = 0

        self.cache_alpha = dict()

        Statistique.__init__(self)

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

    def restituer_statistiques(self):

        resultat = dict()
        resultat[StatistiqueCaracteres.NB_MAJUSCULES] = self.nb_majuscules
        resultat[StatistiqueCaracteres.NB_MINUSCULES] = self.nb_minuscules
        resultat[StatistiqueCaracteres.NB_NUMERIQUES] = self.nb_numeriques
        resultat[StatistiqueCaracteres.NB_SYMBOLES] = self.nb_symboles
        resultat[StatistiqueCaracteres.TOTAL_CARACTERES] = self.total_caracteres

        return resultat

class StatistiqueLongueur(Statistique):
    """Donne des statistiques sur les chaines analysees : longueur max, min, moyenne"""

    LONGUEUR_MINIMUM = "longueur_minimum"
    LONGUEUR_MAXIMUM = "longueur_maximum"
    LONGUEUR_MOYENNE = "longueur_moyenne"

    def __init__(self):
        self.longueur_minimum = 100000000
        self.longueur_maximum = 0
        self.somme_longueurs = 0
        self.nb_lignes_analysees = 0

        Statistique.__init__(self)

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

    def restituer_statistiques(self):

        resultat = dict()

        resultat[StatistiqueLongueur.LONGUEUR_MINIMUM] = self.longueur_minimum
        resultat[StatistiqueLongueur.LONGUEUR_MAXIMUM] = self.longueur_maximum
        resultat[StatistiqueLongueur.LONGUEUR_MOYENNE] = self.somme_longueurs / self.nb_lignes_analysees

        return resultat
