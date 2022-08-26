import datetime
from time import sleep

from scrape_wt_wiki import get_wiki_changelog

dt0 = datetime.datetime.now()
while True:
    if (datetime.datetime.now() - dt0).days >= 1:
        dt0 = datetime.datetime.now()
        # call function to both update based on changelog
        # and also put update the DB
        pass
    else:
        sleep(60)




