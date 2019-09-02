
Spec
====
$company ingests thousands of sensor daily on a daily basis. The purpose of this test is to develop a
data pipeline that given a random generator of sensor data that generates data points in the
following format:
```
{
    "id": "GLOBALLY_UNIQUE_IDENTIFIER",
    "type": "Sensor",
    "content": {
        "temperature_f": 90, // Temperature in Fahrenheit
        "time_of_measurement": "2019-06-24T15:00:00" // Datetime in ISO format
    }
}
```
Your task is to develop a pipeline that will ingest this sensor data, enrich with temperature_c, and
store in a queue.
Given elements arriving in that queue, you should develop another process that will ingest data
from that queue and write into a database.
In a nutshell the steps to develop the project are:
1. Develop a random sensor data generator
2. Develop a program that will ingest this sensor data, transform and write it into a queue
3. Develop a program that will ingest data from that queue and write it into a database
4. Code needs to be versioned in a Git repository

FAQ
Q. Which languages can I use?
- A. We will not impose any language limitations but Python is highly desirable

Q. Which Database should I use?
- A. There is no restriction to which database should be used but here are the list of databases
currently being used in the company: Postgres, ElasticSearch, MongoDB, Redis, Kafka

Q. How much time do I have to complete the test?
- A. 1 Week from the received date


Unknowns
========
1. if the data should have been received via some api endpoint, read from a file or something else, i just decided to make a function which would spit out some data - this can be easily replaced.

2. what sort of queries get run on the data and how long the data needs to exist for, this would have a massive impact on what DB is chosen. it would be very easy to pump the data into a locally running redis, which is grand for short term easy to query data, if we wanted long term i might have considered something like this - https://www.timescale.com/
 , however for this i decided to aim the data at a mongodb instance, mostly becuse the data is already in JSON, and I'd never used Mongo before and wanted to have a quick look.


Results
=======
See [here](docker_for_mongo.txt) for write up of the DB and sample output.


Run me
======

Assuming mongoDB is running as described above.

$ pip install -r requirements.txt

$ python sensor.py


Test me
=======

$ python test_sensor_stuff.py


Known Fail Cases
================
1. mongodb is not running locally
2. mongodb turns off during processing or gets "full"
3. failure to insert data will not be retried (exponential backoff and an overflow queue would be ideal).


To be improved
==============
1. Logging/monitoring - it would be easy to get a good overview of whats going on with some simple counts of when we add or remove from the queue
2. testing - it only covers the actual data processing, adding testing for mongo client and the rest of the pipeline would be ideal.
3. configuration for clients/timeouts/dbs should be passed in via some externally managed config file.
4. before going anywhere near real data, the DB should be secured with username&pass at the very least.
