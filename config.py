from configparser import ConfigParser
import sys, getopt



def readconfig(elasticHost, esindex, localServer, localPort, mongoport, mongohost,debug):
    config = ConfigParser()

    candidates = ['/etc/ews/ewsput.cfg']

    config.read(candidates)

    elasticHost = config.get("elasticsearch", "ip")
    esindex = config.get("elasticsearch", "index")

    localServer = config.get('home', 'ip')
    localPort = config.get('home', 'port')

    mongohost = config.get('mongo', 'ip')
    mongoport = config.get('mongo', 'port')

    debugCmd = config.get('general', 'debug')
    if (debugCmd == "1"):
        debug = True
    else:
        debug = False

    return (elasticHost, esindex, localServer, localPort, mongoport, mongohost, False, debug)


def readCommandLine(elasticHost, esindex, localServer, localPort, mongoport, mongohost, createIndex, useConfigFile, debug):

    #
    # Read command line args
    #
    myopts, args = getopt.getopt(sys.argv[1:], "b:s:i:p:mh:mp:c:d")
    debugCmd = "0"

    for o, a in myopts:
        useConfigFile = False

        if o == '-s':
            elasticHost = a
        elif o == '-i':
            esindex = a
        elif o == '-p':
            localPort = a
        elif o == '-b':
            localServer = a
        elif o == '-mh':
            mongohost = a
        elif o == '-mp':
            mongoport = a
        elif o == '-d':
            debugCmd = a
        elif o == '-c':
            createIndex = True


    if (debugCmd == "1"):
        debug = True
    else:
        debug = False

    return (elasticHost, esindex, localServer, localPort, mongoport, mongohost, createIndex, useConfigFile, debug)
