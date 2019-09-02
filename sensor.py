import random
import datetime
import logging
import time
import queue
import threading

from pymongo import MongoClient

def get_new_data():
    '''
    Generates some sample sensor output
    with a varying reading for farenheight. 
    '''
    new_f = random.randint(-500,500)
    sensor_data = {
        "id": "GLOBALLY_UNIQUE_IDENTIFIER",
        "type": "Sensor",
        "content": {
            "temperature_f": new_f, # Temperature in Fahrenheit
            "time_of_measurement": datetime.datetime.utcnow().isoformat() # Datetime in ISO format
        }
    }
    return sensor_data


def process_data(data):
    try:
        temp_f = data['content']['temperature_f']
    except KeyError:
        logging.exception('Malformed data.')
        return

    # now we have temp_f, convert to temp_c
    # (temp_f°F − 32) × 5/9 = temp_c°C
    # 5/9 = 0.5555555555555556
    temp_c = (temp_f - 32) * (0.5555555555555556)

    del data['content']['temperature_f']
    data['content']['temperature_c'] = temp_c
    return data


def add_to_queue(data, q):
    '''
    takes data and queue, just add.
    '''
    q.put(data)


def run_data_getter(q):
    '''
    gets data, processed it, puts it in a q
    '''
    while True:
        data = get_new_data()
        processed_data = process_data(data)
        add_to_queue(processed_data, q)
        time.sleep(5)


def get_from_queue(q):
   return q.get()


def write_to_db(data, collection):
    '''
    dunno what to do yet
    '''
    try:
        collection.insert_one(data)
    except Exception as e:
        logging.exception("failed to insert data")


def run_data_writer(q, collection):
    while True:
        try:
            data = get_from_queue(q)
        except queue.Empty:
            # no data, thats grand
            continue
        else:
            # we have data, lets write it
            write_to_db(data, collection)


def run_the_data():
    '''

    '''
    # just using stock settings for the mongo db setup.
    mongo_client = MongoClient('localhost', 27017)
    db = mongo_client['data']
    collection = db.sensor_temps
    # basic queue, need to know more about the type of
    # data/machine to configure a different type of queue.
    new_q = queue.Queue()
    get_and_process_t = threading.Thread(target=run_data_getter, args=(new_q,))
    write_to_db_t = threading.Thread(target=run_data_writer, args=(new_q, collection))
    get_and_process_t.start()
    write_to_db_t.start()
    while True:
        qsize = new_q.qsize()
        if qsize != 0:
            print("q has data")



if __name__ == '__main__':
    run_the_data()


