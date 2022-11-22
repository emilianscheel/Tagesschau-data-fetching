import datetime
import json
import os
import re

from bs4 import BeautifulSoup

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


def convert(jsonData={}, timestamp="", filePaths=[]):

    database = json.loads(
        open(dataFolder + "database.json", encoding="utf-8").read())

    def convertJsonData(jsonData, timestamp=""):

        dataFromDate = datetime.datetime.strptime(
            timestamp, dateFormat).strftime(dateFormat)

        for index, news in enumerate(jsonData["news"]):

            if not 'sophoraId' in news:
                continue

            # if news article in database with same sophoraId already exists,
            # then just update lastDownload property
            if any(x['sophoraId'] == news['sophoraId'] for x in database):
                for x in database:
                    if (x['sophoraId'] == news['sophoraId']):
                        x["lastDownload"] = dataFromDate

                        # add new ranking
                        x["rankings"].append(
                            {"timestamp": dataFromDate, "score": index+1})
                continue

            newsObject = {
                "sophoraId": news['sophoraId'],
                "title": news["title"] if "title" in news else "",
                "content": "",
                "date": news['date'] if 'date' in news else "",
                "firstDownload": dataFromDate,
                "lastDownload": dataFromDate,
                "author": "",
                "sender": "",
                "tags": [],
                "geotags": [],
                "linkBoxes": [],
                "related": [],
                "ressort": news['ressort'] if 'ressort' in news else "",
                "breakingNews": news['breakingNews'] if 'breakingNews' in news else "",
                "category": "",
                "rankings": []
            }

            # add ranking
            if index not in newsObject["rankings"]:
                newsObject["rankings"].append(
                    {"timestamp": dataFromDate, "score": index+1})

                # add tags
            if 'tags' in news:
                for tag in news['tags']:
                    newsObject["tags"].append(tag["tag"])

            # add geotags
            if 'geotags' in news:
                for geotag in news['geotags']:
                    newsObject["geotags"].append(geotag["tag"])

            # add category (from tracking)
            if 'tracking' in news:
                topicTree = news["tracking"][0]["sid"].split('.')
                topicTree.pop(0)
                topicTree.pop(-1)
                newsObject["category"] = "/".join(topicTree)

            # handling content
            if 'content' in news:
                for contentSection in news["content"]:
                    if (contentSection["type"] == "text" or contentSection["type"] == "headline"):
                        sectionValueRaw = contentSection["value"]
                        sectionValue = removeHTMLTags(
                            sectionValueRaw).replace("\"", "")

                        # add author
                        if (sectionValueRaw.startswith("<em>Von")):
                            newsFrom = sectionValue.replace(
                                'Von ', '').split(', ')
                            newsObject["author"] = newsFrom.pop(0)
                            newsObject["sender"] = ", ".join(newsFrom)
                            continue

                        # add content
                        newsObject["content"] += sectionValue if newsObject["content"] == "" else "\n" + sectionValue

                    # add linked articles
                    elif contentSection["type"] == "box":
                        contentSectionBox = contentSection["box"]
                        linkBox = {
                            "title": contentSectionBox["title"] if "title" in contentSectionBox else "",
                            "subtitle": contentSectionBox["subtitle"] if "subtitle" in contentSectionBox else "",
                            "sophoraId": "",
                        }

                        if "link" in contentSectionBox:
                            soup = BeautifulSoup(
                                contentSectionBox["link"], "html.parser")
                            links = [a['href']
                                     for a in soup.find_all('a', href=True)]
                            linkBox["sophoraId"] = links[0].split(
                                '/')[-1].replace('.json', '')

                        newsObject["linkBoxes"].append(linkBox)

                    # add related articles
                    elif contentSection["type"] == "related":
                        for relatedArticle in contentSection["related"]:
                            relatedObject = {
                                "title": relatedArticle["title"].replace("\"", '"') if "title" in relatedArticle else "",
                                "subtitle": relatedArticle["subtitle"] if "subtitle" in relatedArticle else "",
                                "sophoraId": relatedArticle["sophoraId"] if "sophoraId" in relatedArticle else "",
                                "date": relatedArticle["date"] if "date" in relatedArticle else ""
                            }
                            newsObject["related"].append(relatedObject)

            database.append(newsObject)

    # if filePaths were given,
    # then use their associated data for converting
    if len(filePaths) > 0:
        for filePath in filePaths:
            file = open(filePath, encoding="utf-8")
            fileName = os.path.basename(file.name).split('.')[0]

            # check that fileName matches dateformat
            if not validateDateFormat(fileName):
                continue

            fileJsonData = json.loads(file.read())

            # check that fileJsonData has property named 'news'
            if not 'news' in fileJsonData:
                continue

            convertJsonData(fileJsonData, timestamp=fileName)

    # no filePaths were given
    # use jsonData instead
    else:
        convertJsonData(jsonData, timestamp=timestamp)

    file = open(dataFolder + "database.json", "w")
    file.write(json.dumps(database, ensure_ascii=False, indent=4))
    file.close()


def createDatabaseDir():
    if not os.path.exists(dataFolder):
        os.mkdir(dataFolder)

    if not os.path.isfile(dataFolder + "database.json"):
        open(dataFolder + "database.json", "x")
        file = open(dataFolder + "database.json",
                    "w")
        file.write(json.dumps([], ensure_ascii=False, indent=4))
        file.close()


if __name__ == "__main__":
    createDatabaseDir()
    convert()
