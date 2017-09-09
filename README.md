#Intro




**Preconditions**

Python3
Install Elasticsearch 5.5 ++
Install MongoDB 3.xx ++

**Install**

pip3 install -r requirements.txt 
Copy ewsput.cfg from etc/ews/ to /etc/ews/eqsput.cfg
Install Maxmind GeoIP libraries at /var/lib/

    GeoIP.dat
    GeoCity.dat
    GeoIPASNum.dat
    
**Then let the code create a new index** 

    python3 worker.py -c -p 9933 -b 192.168.1.64 -u 192.168.1.64 -i ews-2017.1


**Example command line for running the backend (command line settings override config file)**

    python3 worker.py -p 9933 -b 192.168.1.64 -u 192.168.1.64 -i ews-2017.1


**Command line option**

-p local port to listen on

-b local ip / interface to listen on

-u ip of elasticsearch

-i index to be used on elasticsearch server

-h mongohost

-l mongoport

-c just create the index

-t test only the configured connections


**Config file**

The config file is located at /etcews/ewsput.cfg

    [home]
    ip= {{ LOCAL_LISTEN_IP }}
    port= {{ LOCAL_LISTEN_PORT }}
   
    [mongo]
    ip= {{ MONGO_IP }}
    port= {{ MONGO_PORT }}
    
    [elasticsearch]
    port= {{ ELASTIC_PORT }}
    ip= {{ ELASTIC_IP }}
    index= {{ ELASTIC_INDEX }}
    
    [general]
    debug=0
    
    [slack]
    use= {{ SLACK_USE }}
    token= {{ SLACK_TOKEN }}

**Credits**

Code by Andre Vorbach and Markus Schmall

Overall help, friendly extensions / comments / suggestions by Markus Schroer

Valuable discussions with Aydin Kocas, Markus Schroer, Marco Ochse and Rainer Schmidt

**Used frameworks / tools:**

Maxmind GeoIP (https://dev.maxmind.com/geoip/legacy/geolite/)
Gunicorn
Bottle
Elasticsearch
Mongo
