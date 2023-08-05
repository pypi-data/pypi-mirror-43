import requests
import logging
globalheaders = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"
}

def Get(url, **kwgs):
    if kwgs.get("headers"):
        headers = {**globalheaders, **kwgs.get("headers")}
    else:
        headers = globalheaders
    resp = requests.get(url, headers=headers)
    if resp.ok:
        try:
            r = resp.json()
        except Exception as e:
            logging.info(e)
            r = resp.text
        finally:
            return r