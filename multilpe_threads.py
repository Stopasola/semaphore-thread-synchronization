import random
import datetime
import time
import threading

unload_list = list()
ship_list = list()


def fill_unload_list():
    unload_list.clear()
    for i in ship_list:
        if i.containers > 0 or i.load > 0:
            if i.state != "charging":
                unload_list.append([i.arrival_time, i.id])

    unload_list.sort(key=lambda s: s[0])


def show_ship(ship):
    #print('---------------')
    print('id', ship.id)
    print('state', ship.state)
    #print('ship_type', ship.ship_type)
    print('containers', ship.containers)
    print('load', ship.load)
    #print('arrival_time', ship.arrival_time)


def crane(ship_to_unload):
    unload_time = ship_to_unload.containers * 0.0001
    #print('mt cr unload_time', unload_time)
    time.sleep(unload_time)
    ship_to_unload.containers = 0
    if ship_to_unload.containers == 0 and ship_to_unload.load == 0:
        ship_to_unload.state = "empty"
    else:
        ship_to_unload.state = "full"


def bulk_terminal(ship_to_unload):
    unload_time = ship_to_unload.load * 0.001
    #print('mt bk unload_time', unload_time)
    time.sleep(unload_time)
    ship_to_unload.load = 0
    if ship_to_unload.containers == 0 and ship_to_unload.load == 0:
        ship_to_unload.state = "empty"
    else:
        ship_to_unload.state = "full"


def port_operation(lock):
    while unload_list:
        lock.acquire()
        # print('---------------')
        # print('Sessão critica')
        # print(threading.currentThread().getName())
        ship_id = unload_list[0][1]
        del unload_list[0]
        ship_to_unload = next(x for x in ship_list if x.id == ship_id)
        ship_to_unload.state = "charging"
        # print(show_ship(ship_to_unload))
        lock.release()

        if ship_to_unload.ship_type == "container" or (ship_to_unload.ship_type == "both" and ship_to_unload.containers > 0):
            crane(ship_to_unload)
        elif ship_to_unload.ship_type == "grain" or (ship_to_unload.ship_type == "both" and ship_to_unload.load > 0):
            bulk_terminal(ship_to_unload)

        lock.acquire()
        fill_unload_list()
        lock.release()


def show_ship_list(show_list):
    for i in show_list:
        print(i.id)
        print(i.state)
        print(i.ship_type)
        print(i.containers)
        print(i.load)
        print(i.arrival_time)
        print('-----')


def start_multithread_2(sh_list):
    global ship_list

    ship_list = sh_list.copy()

    fill_unload_list()
    start_time = time.time()

    lock = threading.Lock()
    t1 = threading.Thread(name='Thread_01', target=port_operation, args=(lock,))
    t2 = threading.Thread(name='Thread_02', target=port_operation, args=(lock,))

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    duration = time.time() - start_time

    #show_ship_list(ship_list)
    print('Duration 2 MT', duration)


def start_multithread_4(sh_list):
    global ship_list

    ship_list = sh_list.copy()

    fill_unload_list()
    start_time = time.time()

    lock = threading.Lock()
    t1 = threading.Thread(name='Thread_01', target=port_operation, args=(lock,))
    t2 = threading.Thread(name='Thread_02', target=port_operation, args=(lock,))
    t3 = threading.Thread(name='Thread_03', target=port_operation, args=(lock,))
    t4 = threading.Thread(name='Thread_04', target=port_operation, args=(lock,))
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t1.join()
    t2.join()
    t3.join()
    t4.join()
    duration = time.time() - start_time

    print('Duration 4 MT', duration)