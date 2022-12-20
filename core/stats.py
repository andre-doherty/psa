import time
from abc import abstractmethod, ABC

class StatistiqueObserver(ABC):

    TIMESTAMP = "timestamp"
    CURRENT_STATISTICS = "current_statistiques"

    @abstractmethod
    def notifyStatistiqueObserver(self, notification):
        pass

class Statistique:
    STAT_LONGUEUR = "stat_longueur"
    STAT_CARACTERES = "stat_caracteres"
    STAT_FREQUENCES = "stat_frequences"

    def __init__(self):
        self.observers = []

    def register_listener(self, observer):
        self.observers.append(observer)

    def unregister_listener(self, observer):
        self.observers.remove(observer)

    def notify_observer(self, notification):
        for observer in self.observers:
            observer.notifyStatistiqueObserver(notification)

    @abstractmethod
    def get_type(self):
        pass

    @abstractmethod
    def calculer(self, chaines):
        pass

    @abstractmethod
    def restituer_statistiques(self):
        pass


    def create_notification_payload(self):
        notification = dict()
        notification[StatistiqueObserver.TIMESTAMP] = time.time()
        notification[StatistiqueObserver.CURRENT_STATISTICS] = self.restituer_statistiques()

        return notification

class StatistiquesFrequences(Statistique):
    """Donne des statistiques sur la fréquence d'usage des caractères"""

    TABLEAU_FREQUENCES = "tableau_frequence"
    NB_CARACTERES = "nb_caracteres"

    def __init__(self):
        self.nb_caracteres = 0
        #self.tab_frequence = dict()
        #for i in range(256):
        #    self.tab_frequence[i] = 0
        self.not_ascii = dict()

        Statistique.__init__(self)

    def get_type(self):
        return Statistique.STAT_FREQUENCES

    def calculer(self, chaines):
        for chaine in chaines:
            for char in chaine:
                self.nb_caracteres += 1
                if (char in self.not_ascii):
                    value = self.not_ascii[char]
                    value += 1
                    self.not_ascii[char] = value
                else:
                    self.not_ascii[char] = 1
        if len(self.observers) != 0:
            self.notify_observer(self.create_notification_payload())

    def restituer_statistiques(self):

        tableau_frequences = dict()
        for key in sorted(self.not_ascii):
            if self.nb_caracteres != 0:
                #tableau_frequences[key] = format((float(self.not_ascii[key])/float(self.nb_caracteres) * 100),'.2f')
                tableau_frequences[ord(key)] = self.not_ascii[key]
            else:
                tableau_frequences[ord(key)] = "N/A"

        resultat = dict()
        resultat[StatistiquesFrequences.NB_CARACTERES] = self.nb_caracteres
        resultat[StatistiquesFrequences.TABLEAU_FREQUENCES] = tableau_frequences
        return resultat

    def merge(self, stat):
        statistique = StatistiquesFrequences()
        statistique = stat
        self.nb_caracteres += statistique.nb_caracteres
        statistique_tab_caracteres = statistique.not_ascii
        for key in statistique_tab_caracteres:
            if key in self.not_ascii:
                self.not_ascii[key] = self.not_ascii[key] + statistique_tab_caracteres[key]
            else:
                self.not_ascii[key] = statistique_tab_caracteres[key]


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
        return Statistique.STAT_CARACTERES

    def calculer(self, chaines):
        for chaine in chaines:
            self.total_caracteres += len(chaine)
            for char in chaine:
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

        if len(self.observers) != 0:
            self.notify_observer(self.create_notification_payload())

    def restituer_statistiques(self):

        resultat = dict()
        resultat[StatistiqueCaracteres.NB_MAJUSCULES] = self.nb_majuscules
        resultat[StatistiqueCaracteres.NB_MINUSCULES] = self.nb_minuscules
        resultat[StatistiqueCaracteres.NB_NUMERIQUES] = self.nb_numeriques
        resultat[StatistiqueCaracteres.NB_SYMBOLES] = self.nb_symboles
        resultat[StatistiqueCaracteres.TOTAL_CARACTERES] = self.total_caracteres

        return resultat

    def merge(self, stat):
        statistique = StatistiqueCaracteres()
        statistique = stat
        self.nb_majuscules += statistique.nb_majuscules
        self.nb_minuscules += statistique.nb_minuscules
        self.nb_symboles += statistique.nb_symboles
        self.nb_numeriques += statistique.nb_numeriques
        self.total_caracteres += statistique.total_caracteres


class StatistiqueLongueur(Statistique):
    """Donne des statistiques sur les chaines analysees : longueur max, min, moyenne"""

    LONGUEUR_MINIMUM = "longueur_minimum"
    LONGUEUR_MAXIMUM = "longueur_maximum"
    LONGUEUR_MOYENNE = "longueur_moyenne"
    REPARTITION = "repartition"

    def __init__(self):
        self.somme_longueurs = 0
        self.nb_lignes_analysees = 0

        self.tab_longueurs = dict()

        Statistique.__init__(self)

    def get_type(self):
        return Statistique.STAT_LONGUEUR

    def calculer(self, chaines):
        for chaine in chaines:
            longueur_chaine = len(chaine)
            if longueur_chaine in self.tab_longueurs:
                compteur = self.tab_longueurs[longueur_chaine]
                compteur += 1
                self.tab_longueurs[longueur_chaine] = compteur
            else:
                self.tab_longueurs[longueur_chaine] = 1

            self.somme_longueurs += longueur_chaine
            self.nb_lignes_analysees += 1

        if len(self.observers) != 0:
            self.notify_observer(self.create_notification_payload())

    def restituer_statistiques(self):

        repartition = dict()

        sorted_longueurs = sorted(self.tab_longueurs)

        if (len(self.tab_longueurs) != 0):
            longueur_minimum = sorted_longueurs[0]
            longueur_maximum = sorted_longueurs[-1]
        else:
            longueur_minimum = 0
            longueur_maximum = 0

        for longueur in sorted_longueurs :
            repartition[longueur] = self.tab_longueurs[longueur]

        resultat = dict()

        resultat[StatistiqueLongueur.REPARTITION] = repartition
        resultat[StatistiqueLongueur.LONGUEUR_MINIMUM] = longueur_minimum
        resultat[StatistiqueLongueur.LONGUEUR_MAXIMUM] = longueur_maximum
        if self.nb_lignes_analysees != 0:
            resultat[StatistiqueLongueur.LONGUEUR_MOYENNE] = self.somme_longueurs / self.nb_lignes_analysees
        else:
            resultat[StatistiqueLongueur.LONGUEUR_MOYENNE] = "N/A"

        return resultat

    def merge(self, stat):
        statistique = StatistiqueLongueur()
        statistique = stat
        self.somme_longueurs += statistique.somme_longueurs
        self.nb_lignes_analysees += statistique.nb_lignes_analysees
        statistique_tab_longueur = statistique.tab_longueurs
        for key in statistique_tab_longueur:
            if key in self.tab_longueurs:
                self.tab_longueurs[key] = self.tab_longueurs[key] + statistique_tab_longueur[key]
            else:
                self.tab_longueurs[key] = statistique_tab_longueur[key]