# importation des modules
from pymongo import MongoClient
import datetime

# Connexion à la base de données
connection_string = "mongodb://rhobs:xeiPhie3Ip8IefooLeed0Up6@15.236.51.148:27017/rhobs" # lien de connexion
client = MongoClient(connection_string)
db = client["rhobs"]
collection = db["test"]


# Question 0 : Nombre d'auditeurs par style de musique

listeners_by_music = {}
for data in collection.find():
    for key in data.keys():
        if key != "_id": # on récupère le nom de la personne avec la clef qui n'est pas son id
            for music in data[key]['music']: # on parcourt les musiques écoutées par la personne
                if music in listeners_by_music:
                    listeners_by_music[music] += 1 # on incrémente de 1 le nombre d'auditeurs de cette musique
                else:
                    listeners_by_music[music] = 1 # on initialise le nombre d'auditeurs à 1 pour une musique qui n'a pas encore été rencontrée


def print_listeners_by_music():
    """ affiche le nombre d'auditeurs par musique """
    for music in listeners_by_music:
        print("Il y a {} personnes qui écoutent de la musique ".format(listeners_by_music[music]) + music + ".")
    print("###")

print_listeners_by_music()


# Question 1 : Moyenne d'âge par music

today = [int(x) for x in str(datetime.date.today()).split("-")] # Date d'aujourd'hui


def read(date_string):
    """ Prend une date au format AAAA-MM-JJ sous forme de chaîne de caractères
     et la renvoie sous forme liste d'entiers [AAAA, MM, JJ] """
    return([int(x) for x in date_string.split("-")])

def get_age(date_list):
    """ Prend une date de naissance sous forme de liste
    et calcule l'âge d'une personne née à cette date
    """
    return today[0] - date_list[0] - (1 - (date_list[1] < today[1] or date_list[1] == today[1] and date_list[2] <= today[2]))
    # l'âge en année est égale à la différence entre l'année courante l'année de naissance
    # et on retire 1 si l'anniversaire n'est pas encore passé

# get_age(read(xxx)) permet donc de calculer l'âge d'une personne de la base de données

music_sum_age = {} # Calcule d'abord la somme des âges des personnes par style de musique

for data in collection.find():
    for key in data.keys():
        if key != "_id": # récupère le nom de la personne
            for music in data[key]['music']:
                if music in music_sum_age:
                    music_sum_age[music] += get_age(read(data[key]["birthdate"])) # on incrémente la somme par l'âge de la personne de cette musique
                else:
                    music_sum_age[music] = get_age(read(data[key]["birthdate"])) # on initialise à l'âge de la personne si la musique n'est pas dans le dictionnaire



average_age_by_music = {key: music_sum_age[key] / listeners_by_music[key] for key in listeners_by_music.keys()} # Moyenne d'âge par musique

def print_average_age_by_music():
    for key in average_age_by_music.keys():
        print("La moyenne d'âge des auditeurs de musique " + key + " est de " + str(round(average_age_by_music[key])) + " ans.")
    print("###")

print_average_age_by_music()



# Question 2 : Pyramide des âges

def tranche(age, size):
    """ Prend en entrée un entier âge, et un entier size
    et renvoie la tranche d'âge de taille size associé """
    return "[" + str(age // size * size) + "," + str(age//size * size + size) + "["


def pyramide(city, size):
    """ Prend en entrée une ville et un entier size
    et renvoie un dictionnaire contenant l'ensemble des tranches d'âges de taille size
    auxquelles on associe le nombre de personnes de cette tranche d'âge habitant dans la ville """
    res = {}
    for data in collection.find():
        for key in data.keys():
            if key != "_id": # récupère le nom de la personne
                if data[key]['city'] == city:
                    age = get_age(read(data[key]["birthdate"]))
                    intervalle = tranche(age, size)
                    if intervalle in res:
                        res[intervalle] += 1
                    else:
                        res[intervalle] = 1
    return res

def test_pyramide():
    print("test de la fonction pyramide")
    print("###")
    print('pyramide("Gay", 4)')
    print(pyramide("Gay", 4))
    print("###")
    print('pyramide("Fabre", 3)')
    print(pyramide("Fabre", 3))

test_pyramide()



