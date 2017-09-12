import defusedxml.ElementTree as xmlParser

from xml.etree.ElementTree import tostring
import pygeoip, urllib, datetime
from geoip import geolite2
import hashlib

from elasticsearch import Elasticsearch


countries = ["AD","Andorra","AE","United Arab Emirates","AG","Antigua and Barbuda","AI","Anguilla","AL","Albania","AM","Armenia","AO","Angola","AQ","Antarctica","AR","Argentina","AS","American Samoa","AT","Austria","AU","Australia","AW","Aruba","AX","Åland Islands","AZ","Azerbaijan","BA","Bosnia and Herzegovina","BB","Barbados","BD","Bangladesh","BE","Belgium","BF","Burkina Faso","BG","Bulgaria","BH","Bahrain","BI","Burundi","BJ","Benin","BL","Saint Barthélemy","BM","Bermuda","BN","Brunei Darussalam","BO","Bolivia, Plurinational State of","BQ","Bonaire, Sint Eustatius and Saba","BR","Brazil","BS","Bahamas","BT","Bhutan","BV","Bouvet Island","BW","Botswana","BY","Belarus","BZ","Belize","CA","Canada","CC","Cocos (Keeling) Islands","CD","Congo, the Democratic Republic of the","CF","Central African Republic","CG","Congo","CH","Switzerland","CI","Côte d'Ivoire","CK","Cook Islands","CL","Chile","CM","Cameroon","CN","China","CO","Colombia","CR","Costa Rica","CU","Cuba","CV","Cape Verde","CW","Curaçao","CX","Christmas Island","CY","Cyprus","CZ","Czech Republic","DE","Germany","DJ","Djibouti","DK","Denmark","DM","Dominica","DO","Dominican Republic","DZ","Algeria","EC","Ecuador","EE","Estonia","EG","Egypt","EH","Western Sahara","ER","Eritrea","ES","Spain","ET","Ethiopia","FI","Finland","FJ","Fiji","FK","Falkland Islands (Malvinas)","FM","Micronesia, Federated States of","FO","Faroe Islands","FR","France","GA","Gabon","GB","United Kingdom","GD","Grenada","GE","Georgia","GF","French Guiana","GG","Guernsey","GH","Ghana","GI","Gibraltar","GL","Greenland","GM","Gambia","GN","Guinea","GP","Guadeloupe","GQ","Equatorial Guinea","GR","Greece","GS","South Georgia and the South Sandwich Islands","GT","Guatemala","GU","Guam","GW","Guinea-Bissau","GY","Guyana","HK","Hong Kong","HM","Heard Island and McDonald Islands","HN","Honduras","HR","Croatia","HT","Haiti","HU","Hungary","ID","Indonesia","IE","Ireland","IL","Israel","IM","Isle of Man","IN","India","IO","British Indian Ocean Territory","IQ","Iraq","IR","Iran, Islamic Republic of","IS","Iceland","IT","Italy","JE","Jersey","JM","Jamaica","JO","Jordan","JP","Japan","KE","Kenya","KG","Kyrgyzstan","KH","Cambodia","KI","Kiribati","KM","Comoros","KN","Saint Kitts and Nevis","KP","Korea, Democratic People's Republic of","KR","Korea, Republic of","KW","Kuwait","KY","Cayman Islands","KZ","Kazakhstan","LA","Lao People's Democratic Republic","LB","Lebanon","LC","Saint Lucia","LI","Liechtenstein","LK","Sri Lanka","LR","Liberia","LS","Lesotho","LT","Lithuania","LU","Luxembourg","LV","Latvia","LY","Libya","MA","Morocco","MC","Monaco","MD","Moldova, Republic of","ME","Montenegro","MF","Saint Martin (French part)","MG","Madagascar","MH","Marshall Islands","MK","Macedonia, the Former Yugoslav Republic of","ML","Mali","MM","Myanmar","MN","Mongolia","MO","Macao","MP","Northern Mariana Islands","MQ","Martinique","MR","Mauritania","MS","Montserrat","MT","Malta","MU","Mauritius","MV","Maldives","MW","Malawi","MX","Mexico","MY","Malaysia","MZ","Mozambique","NA","Namibia","NC","New Caledonia","NE","Niger","NF","Norfolk Island","NG","Nigeria","NI","Nicaragua","NL","Netherlands","NO","Norway","NP","Nepal","NR","Nauru","NU","Niue","NZ","New Zealand","OM","Oman","PA","Panama","PE","Peru","PF","French Polynesia","PG","Papua New Guinea","PH","Philippines","PK","Pakistan","PL","Poland","PM","Saint Pierre and Miquelon","PN","Pitcairn","PR","Puerto Rico","PS","Palestine, State of","PT","Portugal","PW","Palau","PY","Paraguay","QA","Qatar","RE","Réunion","RO","Romania","RS","Serbia","RU","Russian Federation","RW","Rwanda","SA","Saudi Arabia","SB","Solomon Islands","SC","Seychelles","SD","Sudan","SE","Sweden","SG","Singapore","SH","Saint Helena, Ascension and Tristan da Cunha","SI","Slovenia","SJ","Svalbard and Jan Mayen","SK","Slovakia","SL","Sierra Leone","SM","San Marino","SN","Senegal","SO","Somalia","SR","Suriname","SS","South Sudan","ST","Sao Tome and Principe","SV","El Salvador","SX","Sint Maarten (Dutch part)","SY","Syrian Arab Republic","SZ","Swaziland","TC","Turks and Caicos Islands","TD","Chad","TF","French Southern Territories","TG","Togo","TH","Thailand","TJ","Tajikistan","TK","Tokelau","TL","Timor-Leste","TM","Turkmenistan","TN","Tunisia","TO","Tonga","TR","Turkey","TT","Trinidad and Tobago","TV","Tuvalu","TW","Taiwan, Province of China","TZ","Tanzania, United Republic of","UA","Ukraine","UG","Uganda","UM","United States Minor Outlying Islands","US","United States","UY","Uruguay","UZ","Uzbekistan","VA","Vatican City State","VC","Saint Vincent and the Grenadines","VE","Venezuela, Bolivarian Republic of","VG","Virgin Islands, British","VI","Virgin Islands, U.S.","VN","Viet Nam","VU","Vanuatu","WF","Wallis and Futuna","WS","Samoa","YE","Yemen","YT","Mayotte","ZA","South Africa","ZM","Zambia","ZW","Zimbabwe",
            "", ""]

#
# return full country name
#
def getCountries(id):
    for i in range (0,len(countries) - 2, 2):
         shortCode = countries[i]
         countryName = countries[i+1]

         if (shortCode in id):
             return countryName

    return ""

def getGeoIP(sourceip, destinationip):

    gi = pygeoip.GeoIP("/var/lib/GeoIP/GeoIP.dat")
    giCity = pygeoip.GeoIP("/var/lib/GeoIP/GeoLiteCity.dat")
    giASN = pygeoip.GeoIP('/var/lib/GeoIP/GeoIPASNum.dat')


    try:
        lat = giCity.record_by_addr(sourceip)['latitude']
        long = giCity.record_by_addr(sourceip)['longitude']
        latDest = giCity.record_by_addr(destinationip)['latitude']
        longDest = giCity.record_by_addr(destinationip)['longitude']
        country = gi.country_code_by_addr(sourceip)
        countryName = getCountries(country)
        asn = giASN.org_by_addr(sourceip)
        asnTarget = giASN.org_by_addr(destinationip)
        countryTarget = gi.country_code_by_addr(destinationip)
        countryTargetName = getCountries(countryTarget)

        return (lat, long, country, asn, asnTarget, countryTarget, countryName, countryTargetName, latDest, longDest)

    except:

        print ("Failure at creating GeoIP information:: Returning dummy information to keep sicherheitstacho UI happy")
        return ("0.0", "0.0", "-", "-", "-", "-", "-", "-", "0.0", "0.0")

#
# init index and mappings
#
def initIndex(host, index):

    es = Elasticsearch([{'host': host, 'port': "9200"}])

    # index settings
    settings = {
        "settings": {
            "number_of_shards": 5,
            "number_of_replicas": 1
        },
        "mappings": {
            "Alert": {
                "properties": {
                    "createTime": {
                        "type": "date",
                        "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
                    },
                    "recievedTime": {
                        "type": "date",
                        "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
                    },
                    "sourceEntryIp": {
                        "type": "ip"
                    },
                    "targetEntryIp": {
                        "type": "ip"
                    },
                    "clientDomain": {
                        "type": "boolean"
                    },
                }
            },
            "CVE": {
                "properties": {
                    "firstSeen": {
                        "type": "date",
                        "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
                    },
                    "lastSeen": {
                        "type": "date",
                        "format": "yyyy-MM-dd HH:mm:ss||yyyy-MM-dd||epoch_millis"
                    },
                    "firstIp": {
                        "type": "ip"
                    },
                    "number": {
                        "type": "text"
                    }

                }
            },

            "IP": {
                "properties": {
                    "ip": {
                        "type": "ip"
                    },
                    "longitude": {
                        "type": "text"
                    },
                    "latitude": {
                        "type": "text"
                    },
                    "country": {
                        "type": "text"
                    },
                    "asn": {
                        "type": "text"
                    },
                    "countyname": {
                        "type": "text"
                    }

                }
            }

        }
    }
    # create index
    es.indices.create(index=index, ignore=400, body=settings)



#
# checks, if a given cve is existing already
#
def ipExisting(ip, host, index):

    es = Elasticsearch(host)

    query = '{"query":{"bool":{"must":[{"query_string":{"default_field":"ip","query":"' + ip + '"}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}}'

    res = es.search(index=index, doc_type="IP", body=query)

    for hit in res['hits']['hits']:

        return True

    return False


#
# store ip
#
def putIP(ip, elasticHost, esindex, country, countryname, asn, debug):

    m = hashlib.md5()
    m.update((ip).encode())

    vuln = {
        "asn": asn,
        "countryname": countryname,
        "ip": ip,
        "country": country

    }

    if debug:
        print("Not storing ip: " + str(ip))
        return 0

    try:
        es = Elasticsearch(elasticHost)
        res = es.index(index=esindex, doc_type='IP', id=m.hexdigest(), body=vuln)
        return 0

    except:
        print ("Error when persisting IP " + ip)
        return 1







#
# store alerts, which include a vulnerability id
#
def putVuln(vulnid, elasticHost, esindex, createTime, ip, debug):

    m = hashlib.md5()
    m.update((createTime + vulnid).encode())

    vuln = {
        "firstSeen" : createTime,
        "lastSeen": createTime,
        "firstIp": ip,
        "number": vulnid

    }

    if debug:
        print("Not sending out vulnerability: " + str(vulnid))
        return 0

    try:
        es = Elasticsearch(elasticHost)
        res = es.index(index=esindex, doc_type='CVE', id=m.hexdigest(), body=vuln)
        return 0

    except:
        print ("Error when persisting")
        return 1

#
# stores an alarm in the index
#
def putAlarm(vulnid, host, index, sourceip, destinationip, createTime, tenant, url, analyzerID, peerType, username, password, loginStatus, version, startTime, endTime, sourcePort, destinationPort,debug):

    m = hashlib.md5()
    m.update((createTime + sourceip + destinationip + url + analyzerID).encode())

    (lat, long, country, asn, asnTarget, countryTarget, countryName, countryTargetName, latDest, longDest) = getGeoIP(
        sourceip, destinationip)

    currentTime = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


    alert = {
        "country": country,
        "countryName": countryName,
        "vulnid": '%s' % vulnid,
        "originalRequestString": '%s' % url,
        "sourceEntryAS": asn,
        "createTime": createTime,
        "clientDomain": tenant,
        "peerIdent": analyzerID,
        "peerType": peerType,
        "client": "-",
        "location": str(lat) + " , " + str(long),
        "locationDestination": str(latDest) + " , " + str(longDest),
        "sourceEntryIp": sourceip,
        "sourceEntryPort": sourcePort,
        "additionalData": "",
        "targetEntryIp": destinationip,
        "targetEntryPort": destinationPort,
        "targetCountry": countryTarget,
        "targetCountryName": countryTargetName,
        "targetEntryAS": asnTarget,
        "username": username,  # for ssh sessions
        "password": password,  # for ssh sessions
        "login": loginStatus,  # for SSH sessions
        "targetport": "",
        "clientVersion": version,
        "sessionStart": startTime,
        "sessionEnd": endTime,
        "recievedTime": currentTime
    }

    if debug:
        print("Not sending out alert: " + str(alert))
        return 0

    try:
        es = Elasticsearch(host)
        res = es.index(index=index, doc_type='Alert', id=m.hexdigest(), body=alert)
        return 0

    except:
        print ("Error when persisting")
        return 1



#
# checks, if a given cve is existing already
#
def cveExisting(cve, host, index):
    es = Elasticsearch(host)

    query = '{"query":{"bool":{"must":[{"query_string":{"default_field":"number","query":"' + cve + '"}}],"must_not":[],"should":[]}},"from":0,"size":10,"sort":[],"aggs":{}}'

    res = es.search(index=index, doc_type="CVE", body=query)

    for hit in res['hits']['hits']:

        #cveFound = "%(number)s " % hit["_source"]
        #if (cve in cveFound):
        return True

    return False


def queryAlerts(server, index, maxAlerts):
    xml = """{
  "sort": {
    "createTime": {
      "order": "desc"
    }
  }
}"""

    returnData = ""

    es = Elasticsearch()

    res = es.search(index=index, doc_type="Alert", body={"query": {"match_all": {}}})

    print("Got %d Hits:" % res['hits']['total'])

    EWSSimpleAlertInfo = xmlParser.Element('EWSSimpleAlertInfo')
    alerts = xmlParser.SubElement(EWSSimpleAlertInfo, "Alerts")

    for hit in res['hits']['hits']:

        requestString = "%(originalRequestString)s " % hit["_source"]
        print("%(originalRequestString)s " % hit["_source"])

        alert = xmlParser.SubElement(alerts, "Alert")
        requestXML = xmlParser.SubElement(alert, "Request")
        requestXML.text = requestString

    returnData = tostring(EWSSimpleAlertInfo)

    return returnData


