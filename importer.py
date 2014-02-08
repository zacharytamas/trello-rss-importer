
from sys import argv

from trello import TrelloApi

import settings
import sources

trello = TrelloApi(settings.KEY)
trello.set_token(settings.TOKEN)

if __name__ == '__main__':

    if not len(argv) > 1:
        raise Exception('You must provide the name of a data source class to use.')

    data_source = getattr(sources, argv[1])

    if data_source is None:
        raise Exception('The data source class provided could not be found.')

    data_source(trello).sync_list()
