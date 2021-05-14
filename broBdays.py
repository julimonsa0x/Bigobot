from datetime import timedelta, date, time, datetime
#import time
#import pytz
from tzlocal import get_localzone
from time import gmtime, strftime  

#                                      #
####-----> Cumple de los bros <-----####

# local = get_localzone()
# zone_ar = pytz.timezone('America/Argentina/Buenos_Aires')
ahora = date.today()  # fecha de hoy
ahorita = ['0:00:00']  # if the birthday is today, print happy birthday
# ahora = datetime.now()  si queremos la hora tambien, cambiar los date --> datetime

cumple_nico = date(2022, 5, 9) - ahora  #con estas 3 lineas calculo la fecha de nico
cumple_nico = str(cumple_nico).split(".")
if cumple_nico == ahorita:
    nicoBday = str("¡¡Es hoy, feliz cumple!!")
else: 
    nicoBday = str("Faltan  " + cumple_nico[0])



cumple_reteke = date(2021, 10, 27) - ahora  #con estas 3 lineas calculo la fecha de reteke
cumple_reteke= str(cumple_reteke).split(".")
if cumple_reteke == ahorita:
    rtkBday = str("¡¡Es hoy, feliz cumple!!")
else: 
    rtkBday = str("Faltan  " + cumple_reteke[0])



cumple_souskenin = date(2021, 10, 8) - ahora  #con estas 3 lineas calculo la fecha de souskenin
cumple_souskenin = str(cumple_souskenin).split(".")
if cumple_souskenin == ahorita:
    sskBday = str("¡¡Es hoy, feliz cumple!!")
else: 
    sskBday = str("Faltan  " + cumple_souskenin[0])



cumple_copi = date(2021, 6, 21) - ahora  #con estas 3 lineas calculo la fecha de copipedro
cumple_copi = str(cumple_copi).split(".")      
if cumple_copi == ahorita:
    copiBday = str("¡¡Es hoy, feliz cumple!!")
else: 
    copiBday = str("Faltan  " + cumple_copi[0])



cumple_tambo = date(2021, 9, 17) - ahora  #con estas 3 lineas calculo la fecha de tambo
cumple_tambo = str(cumple_tambo).split(".")
if cumple_tambo == ahorita:
    tamboBday = str("¡¡Es hoy, feliz cumple!!")
else: 
    tamboBday = str("Faltan  " + cumple_tambo[0])



cumple_jopi = date(2022, 4, 16) - ahora  #con estas 3 lineas calculo la fecha de jopiYo
cumple_jopi = str(cumple_jopi).split(".")
if cumple_jopi == ahorita:
    jopiBday = str("¡¡Es hoy, feliz cumple!!")
else: 
    jopiBday = str("Faltan  " + cumple_jopi[0])



cumple_sofi = date(2022, 1, 14) - ahora  #con estas 3 lineas calculo la fecha de sofi
cumple_sofi = str(cumple_sofi).split(".")
if cumple_sofi == ahorita:
    sofiBday = str("¡¡Es hoy, feliz cumple!!")
else: 
    sofiBday = str("Faltan  " + cumple_sofi[0])


cumple_mato = date(2022, 1, 21) - ahora  #con estas 3 lineas calculo la fecha del mato
cumple_mato = str(cumple_mato).split(".")
if cumple_mato == ahorita:
    matoBday = str("¡¡Es hoy, feliz cumple!!")
else: 
    matoBday = str("Faltan  " + cumple_mato[0])



cumple_lezca = date(2022, 1, 24) - ahora  #con estas 3 lineas calculo la fecha del lezca
cumple_lezca = str(cumple_lezca).split(".")
if cumple_lezca == ahorita:
    lezcBday = str("¡¡Es hoy, feliz cumple!!")
else: 
    lezcBday = str("Faltan  " + cumple_lezca[0])



cumple_seki = date(2022, 1, 23) - ahora  #con estas 3 lineas calculo la fecha del seki
cumple_seki = str(cumple_seki).split(".")
if cumple_seki == ahorita:
    sekiBday = str("¡¡Es hoy, feliz cumple!!")
else: 
    sekiBday = str("Faltan  " + cumple_seki[0])



cumple_monsa = date(2021, 5, 17) - ahora  #con estas 3 lineas calculo la fecha mia (autor)
cumple_monsa = str(cumple_monsa).split(".")
if cumple_monsa == ahorita:
    juliBday = str("¡¡Es hoy, feliz cumple!!")
else: 
    juliBday = str("Faltan  " + cumple_monsa[0])


cumple_bot = date(2021, 12, 23) - ahora  #con estas 3 lineas calculo la fecha del bot (creacion)
cumple_bot = str(cumple_bot).split(".")
if cumple_bot == ahorita:
    botBday = str("¡¡1 año en servicio!!")
else: 
    botBday = str("Faltan  " + cumple_bot[0])

cumple_stalker = date(2022, 2, 27) - ahora  #con estas 3 lineas calculo la fecha de stalker
cumple_stalker = str(cumple_stalker).split(".")
if cumple_stalker == ahorita:
    stalkerBday = str("¡¡Es hoy, feliz cumple!!")
else: 
    stalkerBday = str("Faltan  " + cumple_stalker[0])


#al importar "from datetime import datetime", los cumples pasaron de datetime.datetime(...)
#a datetime(...), esto fue necesario para la variable {current hour}