#Some variables are in French, others in English — I know it's not ideal practice, but let's go with it this time.

import re

#fonction pour recuperer AM OU PM
def moment_of_the_day(hour):
    if "".join(re.findall(r"PM",hour))=="PM":
        return "".join(re.findall(r"PM",hour))
    else:
        return "AM"

#fonction pour recuperer les heures ou minutes
def hours_minute(hour):
    two_point_index = hour.index(":")
    time = [ int(hour[:two_point_index]) , int(hour[two_point_index + 1:two_point_index+3]) ]

    return time


#calcul de l'heure final
def give_me_the_final_hours(hour,add_hour,day_time,switch, day):
    if add_hour < 12 :
        if (hour+add_hour)//12:
            day_time = (day_time+1)%2 
            switch = 1
        if switch and day_time == 1:
            day+=1
        hour = (hour+add_hour) % 12

        return [hour,add_hour,day_time,day]

    else:
        add_hour-=12
        day_time = (day_time+1)%2
        if day_time == 1:
            day+=1
       
        return give_me_the_final_hours(hour,add_hour,day_time,0,day)


#fonction de mise en forme
def make_it_clear(final_hour):

    #mise ne forme de la solution
    if final_hour["hour"]==0:
        final_hour["hour"]="12"
    else:
        final_hour["hour"] = str(final_hour["hour"])

    final_hour["minute"]=str(final_hour["minute"])
    if len(final_hour["minute"])==1:
        a=list(final_hour["minute"])
        a.insert(0,"0")
        a="".join(a)
        final_hour["minute"]=a
    
    if final_hour["number_of_days_later"]==1:
        final_hour["number_of_days_later"]="(next day)"
    elif final_hour["number_of_days_later"]==0:
        pass 
    else:
        final_hour["number_of_days_later"]=f'({final_hour["number_of_days_later"]} days later)'

    return final_hour


#fonction principale
def add_time(start, duration , day=""):
    #variable utile
    pm_am = ["PM","AM"]
    week=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    #création de notre dictionnaire qui va stocker les infos
    final_hour={
        "hour": 0,
        "minute": 0,
        "day_time": "",
        "day": day.lower().title(),
        "number_of_days_later" : 0

    }
    
    
    #on récupère les informations sur start
    final_hour["day_time"]=moment_of_the_day(start) #PM ou AM
    final_hour["hour"] , final_hour["minute"] = hours_minute(start)[0], hours_minute(start)[1]  #on récupère le temps

    #on récupère les infos à ajouter
    add_hour , add_minute = hours_minute(duration)[0],hours_minute(duration)[1]

    #on ajoute les minutes c'est le plus facile
    add_hour += (add_minute+final_hour["minute"])//60
    final_hour["minute"] = (add_minute+final_hour["minute"])%60

    #maintenant on ajoute les heures avec une fonction recursif
    final_list = give_me_the_final_hours(final_hour["hour"],add_hour,pm_am.index(final_hour["day_time"]),0,0)

    #on ajoute les variables

    #on ajoute les heures
    final_hour["hour"] = final_list[0] 

    #on ajpoute pm ou am
    final_hour["day_time"]=pm_am[final_list[2]]

    #on ajoute le nouveau jour
    if final_hour["day"]:
        final_hour["day"] = week[(week.index(final_hour["day"])+final_list[3] ) % 7]

    #on ajoute le nombre de jour next
    final_hour["number_of_days_later"] = final_list[3]

    final_hour=make_it_clear(final_hour)
    

    if day:
        if not final_hour["number_of_days_later"]:
             return f'{final_hour["hour"]}:{final_hour["minute"]} {final_hour["day_time"]}, {final_hour["day"]}'
        else:
            return f'{final_hour["hour"]}:{final_hour["minute"]} {final_hour["day_time"]}, {final_hour["day"]} {final_hour["number_of_days_later"]}'
            
    else:

        if not final_hour["number_of_days_later"]:
            return f'{final_hour["hour"]}:{final_hour["minute"]} {final_hour["day_time"]}'
        else:
            return f'{final_hour["hour"]}:{final_hour["minute"]} {final_hour["day_time"]} {final_hour["number_of_days_later"]}'
            
            

print(add_time('8:16 PM', '466:02', 'tuesday'))

