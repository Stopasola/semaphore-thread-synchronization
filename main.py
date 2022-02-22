import random
import datetime
import time
from copy import deepcopy
from multilpe_threads import start_multithread_2, start_multithread_4
from single_thread import start_single_thread


class Ship:
    def __init__(self, id, state, ship_type, containers, load, arrival_time):
        self.id = id
        self.state = state
        self.ship_type = ship_type
        self.containers = containers
        self.load = load
        self.arrival_time = arrival_time


unload_list = list()
ship_list = list()
qtd = 5


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
        print(i.state)
        print(i.ship_type)
        print(i.containers)
        print(i.load)
        print(i.arrival_time)
        print('-----')


if __name__ == '__main__':
    generate(qtd)
    show_ship_list(ship_list)

    st_ship_list = deepcopy(ship_list)
    mt_ship_list2 = deepcopy(ship_list)
    mt_ship_list4 = deepcopy(ship_list)

    start_single_thread(st_ship_list)
    start_multithread_2(mt_ship_list2)
    start_multithread_4(mt_ship_list4)
