import random
import datetime
import time
import threading




unload_list = list()
ship_list = list()



def ship_type():
    sh_type = random.randint(0, 2)
    if sh_type == 0:
        return "grain"
    elif sh_type == 1:
        return "container"
    else:
        return "both"


def date_range():
    start_date = datetime.datetime.today()
    return start_date + datetime.timedelta(days=random.randint(1, 8))


def generate(qtd):
    for i in range(1, qtd + 1):
        state = "full"
        sh_type = ship_type()
        containers = random.randint(5, 20) * 1000 if sh_type == 'both' or sh_type == 'container' else 0
        load = random.randint(10, 40) * 10 if sh_type == 'both' or sh_type == 'grain' else 0
        arrival_time = date_range()
        ship_list.append(Ship(i, state, sh_type, containers, load, arrival_time))


def show_ship_list(show_list):
    for i in show_list:
        print(i.id)
        print(i.ship_type)
        print(i.containers)
        print(i.load)
        print(i.arrival_time)
        print('-----')


def fill_unload_list():
    unload_list.clear()
    for i in ship_list:
        if i.containers > 0 or i.load > 0:
            if i.state != "charging":
                unload_list.append([i.arrival_time, i.id])

    unload_list.sort(key=lambda s: s[0])


def show_ship(ship):
    print('---------------')
    print('id', ship.id)
    print('state', ship.state)
    print('ship_type', ship.ship_type)
    print('containers', ship.containers)
    print('load', ship.load)
    print('arrival_time', ship.arrival_time)


def crane(ship_to_unload):
    unload_time = ship_to_unload.containers * 0.0001
    #print('st cr unload_time', unload_time)
    time.sleep(unload_time)  # Descarregando
    ship_to_unload.containers = 0
    if ship_to_unload.containers == 0 and ship_to_unload.load == 0:
        ship_to_unload.state = "empty"
    else:
        ship_to_unload.state = "full"


def bulk_terminal(ship_to_unload):
    unload_time = ship_to_unload.load * 0.001
    #print('st bk unload_time', unload_time)
    time.sleep(unload_time)
    ship_to_unload.load = 0
    if ship_to_unload.containers == 0 and ship_to_unload.load == 0:
        ship_to_unload.state = "empty"
    else:
        ship_to_unload.state = "full"


def port_operation():
    while unload_list:
        ship_id = unload_list[0][1]  # Acessa primeiro navio da lista
        del unload_list[0]
        ship_to_unload = next(x for x in ship_list if x.id == ship_id)
        ship_to_unload.state = "charging"

        if ship_to_unload.ship_type == "container" or (ship_to_unload.ship_type == "both" and ship_to_unload.containers > 0):
            crane(ship_to_unload)
        elif ship_to_unload.ship_type == "grain" or (ship_to_unload.ship_type == "both" and ship_to_unload.load > 0):
            bulk_terminal(ship_to_unload)

        # Sessão critica
        fill_unload_list()


def start_single_thread(sh_list):
    global ship_list

    ship_list = sh_list.copy()

    fill_unload_list()
    start_time = time.time()
    port_operation()
    duration = time.time() - start_time
    print('Duration ST', duration)