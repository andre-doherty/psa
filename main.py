from core.engine import analyze
from log4python.Log4python import log

# On souhaite écrire un programme qui va ouvrir un fichier texte (rockyou.txt) contenant des mots de passe à
# raison d’un mot de passe par ligne, et produire des statistiques sur l’usage des caractères (majuscules,
# minuscules, numériques, symboles), la longueur minimale, maximale et moyenne, la fréquence d’usage des
# lettres dans ce fichier.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    count_lines = sum(1 for line in open('rockyou.txt' ,encoding="iso8859-1"))

    analyze('rockyou.txt', count_lines)
    #TestLog = log("LogDemo")
    #TestLog.debug("Debug Log")
    #TestLog.info("Info Log")
