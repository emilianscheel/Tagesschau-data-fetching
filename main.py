#!/usr/bin/python

import urllib3
from datetime import datetime
import json
import os
from converter import convert
from converter import createDatabaseDir


dataFolder = os.path.abspath('') + "data/"


def fetch():

    apiURL = "https://www.tagesschau.de/api2/"

    dateTimeObj = datetime.now()
    timestamp = dateTimeObj.strftime(
        "%d-%m-%Y--%H-%M-%S")

    http = urllib3.PoolManager()
    request = http.request('GET', apiURL)
    if (request.status != 200):
        return
    jsonData = json.loads(request.data.decode('utf-8'))

    convert(jsonData=jsonData, timestamp=timestamp)

    """
    filename = timestamp + ".json"

    if not os.path.isfile(dataFolder + filename):
        open(dataFolder + filename, "x")

    file = open(dataFolder + filename, "w")
    file.write(json.dumps(jsonData))
    file.close()
    """


if __name__ == "__main__":
    createDatabaseDir()
    fetch()
