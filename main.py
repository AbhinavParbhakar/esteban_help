import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import simplepyble
import struct
import threading
import time

lock = threading.Lock()
thread_on = True

fig,one_axis = plt.subplots()
one_y = []
counter = 0
two_y = []
three_y = []
x_data = []

service_uuid = '02366e80-cf3a-11e1-9ab4-0002a5d5c51b'
characteristic_uuid = '340a1b80-cf4b-11e1-ac36-0002a5d5c51b'

def connect_to_device():
    adapter_list = simplepyble.Adapter.get_adapters()

    adapter_one = adapter_list[0]
    print("\n[SCANNING]\n")
    adapter_one.scan_for(5000)

    scan_results = adapter_one.scan_get_results()
    peripherals = [peripheral.identifier() for peripheral in scan_results]
    peripheral = scan_results[peripherals.index("BlueNRG")]
    peripheral.connect()
    return peripheral

def transform_data(raw_data:tuple):
    """
    Transformers data by changing into the standard ouput of G's
    """
    new_data = list()
    for i,data in enumerate(raw_data):
        new_data.append((data * 0.061) / 1000)

    return new_data

def notify_callback(data):
    global one_y,two_y,three_y,counter,x_data
    if True:
        if len(x_data) > 100:
            x_data.pop(0)
            one_y.pop(0)
            two_y.pop(0)
            three_y.pop(0)

        label_tuple = struct.unpack('<hhh',data)
        transformed_data = transform_data(label_tuple)
        one_y.append(transformed_data[0])
        two_y.append(transformed_data[1])
        three_y.append(transformed_data[2])
        x_data.append(counter)
        counter+=1
    print("Getting data")
peripheral = connect_to_device()

def init_function():
    global peripheral
    #peripheral.notify(service_uuid,characteristic_uuid,notify_callback)
    one_axis.set_ylim(-1,1)

def handle_read():
    global peripheral,one_y,two_y,three_y,counter,x_data
    data = peripheral.read(service_uuid,characteristic_uuid)
    if True:
        if len(x_data) > 100:
            x_data.pop(0)
            one_y.pop(0)
            two_y.pop(0)
            three_y.pop(0)

        label_tuple = struct.unpack('<hhh',data)
        transformed_data = transform_data(label_tuple)
        one_y.append(transformed_data[0])
        x_data.append(counter)
        counter+=1

def thread_callback(peripheral,one_y,two_y,three_y,counter,x_data):
    global thread_on
    while thread_on:
        time.sleep(0.1)
        handle_read()

def update(i):

    global one_axis,x_data,one_y,two_y,three_y,lock
    with lock:
        one_axis.clear()
        one_axis.plot(x_data,one_y)

threading.Thread(target=thread_callback,args=[peripheral,one_y,two_y,three_y,counter,x_data]).start()
animate = FuncAnimation(fig=fig,func=update,init_func=init_function,interval=100)

plt.show()
thread_on = False
print("ending graciously")