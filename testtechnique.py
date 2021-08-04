# Connexion à la base de données
from pymongo import MongoClient
import datetime

connection_string = "mongodb://rhobs:xeiPhie3Ip8IefooLeed0Up6@15.236.51.148:27017/rhobs" # lien de connexion
client = MongoClient(connection_string)
db = client["rhobs"]
collection = db["test"]


# Question 0 : Nombre d'auditeurs par style de musique

listeners_by_music = {}
for data in collection.find():
    for key in data.keys():
        if key != "_id":
            for music in (data[key]['music']):
                if music in listeners_by_music:
                    listeners_by_music[music] += 1
                else:
                    listeners_by_music[music] = 1


def print_listeners_by_music():
    """ affiche le nombre d'auditeurs par musique """
    for music in listeners_by_music:
        print("Il y a {} personnes qui écoute de la musique ".format(listeners_by_music[music]) + music + ".")
    print("###")

print_listeners_by_music()


# Question 1 : Moyenne d'âge par music

today = [int(x) for x in str(datetime.date.today()).split("-")] # Date d'aujourd'hui

# aout5 = [1999, 8, 5]
# aout4 = [1999, 8, 4]
# aout3 = [1999, 8, 3]

def read(date_string):
    """ Prend une date au format AAAA-MM-JJ
     et la renvoie sous forme liste d'entiers [AAAA, MM, JJ] """
    return([int(x) for x in date_string.split("-")])

def get_age(date_list):
    """ Prend une date de naissance sous forme de liste
    et calcule l'âge d'une personne née à cette date
    """
    return today[0] - date_list[0] - (1 - (date_list[1] < today[1] or date_list[1] == today[1] and date_list[2] <= today[2]))
    # l'âge en année est égale à la différence entre l'année courante l'année de naissance
    # à laquelle on retire 1 si l'anniversaire n'est pas encore passé


music_sum_age = {} # Calcule la somme des âges des personnes par style de musique

for data in collection.find():
    for key in data.keys():
        if key != "_id":
            for music in (data[key]['music']):
                if music in music_sum_age:
                    music_sum_age[music] += get_age(read(data[key]["birthdate"]))
                else:
                    music_sum_age[music] = get_age(read(data[key]["birthdate"]))


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
    return "[" + str(age // taille * taille) + "," + str(age//taille * taille + taille) + "["


def pyramide(city, size):
    res = {}
    for data in collection.find():
        for key in data.keys():
            if key != "_id":
                if data[key]['city'] == city:
                    age = get_age(read(exemple[key]["birthdate"]))
                    t = tranche(a, size)
                    if t in res:
                        res[t] += 1
                    else:
                        res[t] = 1
    return res






