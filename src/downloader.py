import urllib.request
import json


def getData(url):
    try:
        return urllib.request.urlopen(url).read().decode("utf8")
    except urllib.error.URLError as e:
        print("Invalid URL: %s"%str(e))
    except urllib.error.HTTPError as e:
        print("HTTP error: %s"%str(e))
    except Exception as e:
        print("Unknown error: %s"%str(e))
    return None


def getJson(data):
    try:
        return json.loads(data)
    except ValueError as e:
        print("Invalid JSON file: %s"%str(e))
    except Exception as e:
        print("Unknown error: %s"%str(e))
    return None