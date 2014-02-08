import feedparser


class DataSource(object):

    feed_url = None
    target_list_id = None
    board_id = None

    def __init__(self, trello):
        self.trello = trello
        self.board_id = trello.lists.get_board(self.target_list_id)['id']
        self.fetch_data()

    def create_card(self, card_info):
        self.trello.cards.new(card_info['name'],
                              self.target_list_id,
                              card_info['desc'])
        print "Created card for", card_info['name']

    def sync_list(self):
        new_cards = self.get_all_card_info()
        existing_cards = self.trello.boards.get_card(self.board_id)

        # Remove cards that we already have so we don't create duplicates.
        for card in existing_cards:
            if card['name'] in new_cards:
                print "Skipping", card['name']
                del new_cards[card['name']]

        for card in new_cards.values():
            self.create_card(card)

    def fetch_data(self):
        self.data = feedparser.parse(self.feed_url)
        return self.data

    def get_all_card_info(self):
        raise NotImplementedError('You must implement this method.')


class ApartmentSearchCraigslist(DataSource):
    """A data source which grabs the latest apartments
    in Kansas City with Google Fiber from Craigslist."""

    # URL to the RSS feed needed.
    feed_url = 'http://kansascity.craigslist.org/search/apa?catAbb=apa&hasPic=1&query=fiber&s=0&format=rss'
    # The Trello ID of the list you'd like to add these items to.
    target_list_id = '52f59a8b8d309f7d166c8d30'

    def get_all_card_info(self):
        cards = {}

        for entry in self.data['entries']:
            name = self.clean_name(entry['title'])
            card = { 'name': name,
                     'desc': '%s \n\n %s' % (entry['summary'],
                                             entry['dc_source']) }
            cards[name] = card

        return cards

    def clean_name(self, name):
        """Method to clean a posting's name."""
        # Right now just returns the name untouched but I may
        # need to do some escaping, etc. here in a bit.
        return name


