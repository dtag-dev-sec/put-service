
import defusedxml.ElementTree as xmlParser
import elastic, auth, sys, getopt, config, communication
from bottle import request, response, install, run, post, get, HTTPResponse
from datetime import datetime

# local variable init defaults
localServer, esindex, localPort, elasticHost, mongohost, mongoport, slackuse, slacktoken = "127.0.0.1", "ews", "8080", "127.0.0.1", "127.0.0.1", "27017", "no", ""
debug = False

createIndex = False
useConfigFile = True

peerIdents = ["WebHoneypot", "Webpage", "Dionaea", "Network(Dionaea)", "honeytrap", "Network(honeytrap)", "kippo", "SSH/console(cowrie)",
              "glastopf", "Webpage", ".gt3", "Webpage",".dio", "Network", ".kip", "SSH/console", "", ""]


#
# Function area
#

def logger(func):
    def wrapper(*args, **kwargs):
        log = open('/var/log/ewsput.txt', 'a')
        log.write('%s %s %s %s %s \n' % (request.remote_addr, datetime.now().strftime('%H:%M'),
                                         request.method, request.url, response.status))
        log.close()
        req = func(*args, **kwargs)
        return req
    return wrapper

install(logger)



#
# parse through the data tables
#
def getPeerType(id):
    for i in range (0,len(peerIdents) - 2, 2):
         honeypot = peerIdents[i]
         peerType = peerIdents[i+1]

         if (honeypot in id):
             return peerType

    return "Unclassified"


#
# fixes the URL (original request string)
#
def fixUrl(destinationPort, url, peerType):

    if ("honeytrap" in peerType):
        return "Attack on port " + str(destinationPort)

    return url

#
# handle the Alerts itself
#
def handleAlerts(tree, tenant):

    counter = 0

    for node in tree.findall('.//Alert'):

        # now parse the node

        peerType, vulnid, sourcePort, destination, destinationPort, createTime, url, analyzerID, username, password, loginStatus, version, starttime, endtime = "Unclassified", "", "", "", "", "-", "", "", "", "", "", "", "", ""

        for child in node:

            childName = child.tag

            if (childName == "Analyzer"):
                id = child.attrib.get('id')
                peerType = getPeerType(id)


            if (childName == "Source"):
                source = child.text.replace('"', '')
                sourcePort = child.attrib.get('port')

            if (childName == "CreateTime"):
                createTime = child.text

            if (childName == "Target"):
                destination = child.text.replace('"', '')
                destinationPort = child.attrib.get('port')


            if (childName == "Request"):
                type = child.attrib.get('type')

                if (type == "url"):
                    url = child.text

                # if peertype could not be identified by the identifier of the honeypot, try to use the
                # description field
                if (type == "description" and peerType == ""):
                        peerType = getPeerType(child.text)

            if (childName == "AdditionalData"):
                meaning = child.attrib.get('meaning')

                if (meaning == "username"):
                    username = child.text

                if (meaning == "password"):
                    password = child.text

                if (meaning == "login"):
                    loginStatus = child.text

                if (meaning == "version"):
                    version = child.text

                if (meaning == "starttime"):
                    starttime = child.text

                if (meaning == "endtime"):
                    endtime = child.text

                if (meaning == "cve_id"):
                    vulnid = child.text

            if (childName == "Analyzer"):
                analyzerID = child.attrib.get('id')


        url = fixUrl(destinationPort, url, peerType)

        #
        # persist CVE
        #
        if (len(str(vulnid)) > 2):
            elastic.putVuln(vulnid, elasticHost, esindex, createTime, source, debug)

        #
        # store attack itself
        #
        correction = elastic.putAlarm(vulnid, elasticHost, esindex, source, destination, createTime, tenant, url, analyzerID, peerType, username, password, loginStatus, version, starttime, endtime, sourcePort, destinationPort, debug)
        counter = counter + 1 - correction

        #
        # slack wanted
        #
        if ("yes" in slackuse):
            if len(str(slacktoken)) > 10:
                if len(str(vulnid)) > 4:
                    communication.sendSlack("cve", slacktoken, "CVE (" + vulnid + ") found.")

    print ("Info: Added " + str(counter) + " entries")
    return True


@get('/heartbeat')
def index():
    message = "A heartbeat for your"
    response = {}
    headers = {'Content-type': 'application/html'}
    response['status'] = "Success"
    raise HTTPResponse(message, status=200, headers=headers)


@get('/')
def index():
    message = ""
    response = {}
    headers = {'Content-type': 'application/html'}
    response['status'] = "Success"
    raise HTTPResponse(message, status=200, headers=headers)


@post('/ews-0.1/alert/postSimpleMessage')
def postSimpleMessage():

    postdata = request.body.read().decode("utf-8")

    message = "<Result><StatusCode>FAILED</StatusCode><Text>Authentication failed.</Text></Result>"

    tree = xmlParser.fromstring(postdata)

    userNameFromRequest, passwordFromRequest = auth.extractAuth(tree)

    if (auth.handleCommunityAuth(userNameFromRequest, passwordFromRequest)):

        message = "<Result><StatusCode>OK</StatusCode><Text></Text></Result>"
        handleAlerts(tree, True)

    elif auth.authenticate(userNameFromRequest, passwordFromRequest, mongohost, mongoport):

        message = "<Result><StatusCode>OK</StatusCode><Text></Text></Result>"
        handleAlerts(tree, False)
    else:
        print("Authentication failed....")

    response = {}
    headers = {'Content-type': 'application/html'}
    response['status'] = "Success"
    raise HTTPResponse(message, status=200, headers=headers)


#
# main program code
#

(elasticHost, esindex, localServer, localPort, mongoport, mongohost,  createIndex, useConfigFile, debug) = config.readCommandLine(elasticHost, esindex, localServer, localPort, mongoport, mongohost, createIndex, useConfigFile, debug)

if (createIndex):
    print ("Info: Just creating an index " + esindex)
    elastic.initIndex(elasticHost, esindex)

else:

    if (useConfigFile):
        print ("Info: Using configfile")
        (elasticHost, esindex, localServer, localPort, mongoport, mongohost, createIndex,debug, slacktoken, slackuse) = config.readconfig(elasticHost, esindex, localServer, localPort, mongoport, mongohost, debug, slacktoken, slackuse)
    if debug:
        print("Info: Running in debug mode")

    #
    # start server depending on parameters given from shell or config file
    #

    print ("Starting DTAG early warning system input handler on server " + str(localServer) + ":" + str(localPort) + " with elasticsearch host at " + str(elasticHost) + " and index " + str(esindex) + " using mongo at " + str(mongohost)+ ":" + str(mongoport))

    run(host=localServer, port=localPort, server='gunicorn', workers=4)

