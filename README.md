**Intro



**Preconditions**

Python3
Install Elasticsearch 5.4 ++
Install MongoDB 3.xx ++

**Install**

pip3 install -r requirements.txt 
Copy ewsput.cfg from etc/ews/ to /etc/ews/eqsput.cfg
Install Maxmind GeoIP libraries at /var/lib/

    GeoIP.dat
    GeoCity.dat
    GeoIPASNum.dat


**Example command line**

python3 worker.py -p 9933 -b 192.168.1.64 -s 192.168.1.64 -i ews-2017.1


**Command line option**

-p local port to listen on

-b local ip / interface to listen on

-s ip of elasticsearch

-i index to be used on elasticsearch server

-h mongohost

-l mongoport

-c just create the index

**Credits**

Some auth code by Andre Vorbach

Overall help, friendly extensions / comments by Markus Schroer

**Used frameworks / tools:**

Maxmind GeoIP (https://dev.maxmind.com/geoip/legacy/geolite/)
Gunicorn
Bottle