import glob
import os
import json
import datetime
import re

dataFolder = os.path.abspath('') + "/data/"

dateFormat = "%d-%m-%Y--%H-%M-%S"


def validateDateFormat(dateText):
    try:
        datetime.datetime.strptime(dateText, dateFormat)
    except ValueError:
        return False
    return True


def removeHTMLTags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def convert():
    filePaths = glob.glob(dataFolder + "*.json")

    database = []

    for filePath in filePaths:

        file = open(filePath, encoding="utf-8")
        fileName = os.path.basename(file.name).split('.')[0]
        jsonData = json.loads(file.read())

        if not validateDateFormat(fileName):
            continue

        dataFromDate = datetime.datetime.strptime(
            fileName, dateFormat).strftime(dateFormat)

        if (not 'news' in jsonData):
            continue

        for news in jsonData["news"]:

            if (not 'sophoraId' in news):
                continue

            if any(x['sophoraId'] == news['sophoraId'] for x in database):
                for x in database:
                    if (x['sophoraId'] == news['sophoraId']):
                        x["lastDownload"] = dataFromDate
                continue

            newsObject = {
                "sophoraId": news['sophoraId'],
                "title": news["title"],
                "content": "",
                "firstDownload": dataFromDate,
                "lastDownload": dataFromDate,
                "author": ""
            }

            if (not 'content' in news):
                continue

            for contentSection in news["content"]:
                if (contentSection["type"] == "text" or contentSection["type"] == "headline"):

                    sectionValue = removeHTMLTags(
                        contentSection["value"]).replace("\"", "")

                    if (sectionValue.startswith("Von")):
                        newsObject["author"] = sectionValue.replace("Von ", "")
                        continue

                    newsObject["content"] += "\n" + sectionValue

            database.append(newsObject)

    if not os.path.isfile(dataFolder + "database.json"):
        open(dataFolder + "database.json", "x")

    file = open(dataFolder + "database.json", "w")
    file.write(json.dumps(database, ensure_ascii=False))
    file.close()


def createDataFolder():
    if (os.path.exists(dataFolder) == False):
        os.mkdir(dataFolder)


if __name__ == "__main__":

    convert()
