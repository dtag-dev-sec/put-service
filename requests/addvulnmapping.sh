#!/usr/bin/env bash

curl -XPUT 'localhost:9200/ews2017.1/_mapping/CVE?pretty' -H 'Content-Type: application/json' -d'
{
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
}
'
