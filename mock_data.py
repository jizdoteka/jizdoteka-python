from random import randint
from emailusernames.utils import create_user, create_superuser

##
##  INFO: Natahnete si pres ./manage.py shell a potom naloadujte a pustte
##



MAN_LIST = ["Adam", "Bedr", "Clark", "Danik", "Ervun", "Filip", "Gustav", "Honza",
            "Issac", "Jirka", "Karel"]
WOMAN_LIST = ["Lenka", "Marus", "Nikola", "Olina", "Petra", "Quentina", "Radka",
              "Stanka", "Tanislava", "Ursula", "Verca", "Wanda", "Yvona", "Zuzka"]

SUR_LIST = ["Novej", "Zaryja", "Nuna", "Ereta", "Bursyk", "Igoru", "Kvalk", "Tucka",
            "Deste", "Teras"]

MAIL_LIST = ["@volny.cz", "@gmail.com", "@github.com", "@erha.cz"]

list_peopl = []

PERS_LIST = MAN_LIST + WOMAN_LIST

soubor = open("mock_data.txt", "w")

#create_superuser("admin@admin.cz", "admin")  ## odkomentujte si pro vkladani!
for inc in range(20):
    nah_jm = PERS_LIST[randint(0, len(PERS_LIST) - 1)]
    nah_pr = SUR_LIST[randint(0, len(SUR_LIST) - 1)]
    nah_mail = MAIL_LIST[randint(0, len(MAIL_LIST) - 1)]

    heslo = nah_jm.lower() + nah_pr.lower()
    mail = nah_jm.lower() + nah_pr.lower() + nah_mail
    #create_user(mail, heslo) ## odkomentujte si pro vkladani!
    soubor.write(mail  + " -heslo je pred zavinacem!\n")

soubor.close()
