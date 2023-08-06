import json
import os

import requests
from retrying import retry

from . import json_converter
from .form_utils import to_multipart_form
from .error.invalid_response import InvalidResponseError

API_URL = 'https://tinycards.duolingo.com/api/1/'

DEFAULT_HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://tinycards.duolingo.com/',
    'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4)' +
                   ' AppleWebKit/537.36 (KHTML, like Gecko)' +
                   ' Chrome/58.0.3029.94 Safari/537.36')
}


def _should_retry_login(exception):
    if isinstance(exception, InvalidResponseError) \
            and 'Oops, something went wrong!' in str(exception):
        return True
    return False


class RestApi(object):
    """Repository-like facade for the Tinycards API.

    Abstracts away all queries to the original Tinycards API and handles all
    JSON (un-)marshalling.
    """

    def __init__(self):
        """Initialize a new instance of the RestApi class."""
        # JSON web token
        self.jwt = None

    @retry(stop_max_attempt_number=5, wait_fixed=500,
           retry_on_exception=_should_retry_login)
    def login(self,
              identifier=None,
              password=None):
        """Log in an user with its Tinycards or Duolingo credentials.

        Args:
            identifier (str): The Tinycards identifier to use for logging in.
                For example, a user's email address.
                Will be taken from ENV if not specified:
                .. envvar:: TINYCARDS_IDENTIFIER
            password (str): The user's password to login to Tinycards.
                Will be taken from ENV if not specified.
                .. envvar:: TINYCARDS_PASSWORD
        """
        # Take credentials from ENV if not specified.
        identifier = identifier or os.environ.get('TINYCARDS_IDENTIFIER')
        password = password or os.environ.get('TINYCARDS_PASSWORD')

        request_payload = {
            'identifier': identifier,
            'password': password
        }
        r = requests.post(url=API_URL + 'login', json=request_payload)
        json_response = r.json()

        set_cookie_headers = {
            k: v for (k, v) in
            [c.split('=') for c in r.headers['set-cookie'].split('; ')]
        }
        self.jwt = set_cookie_headers.get('jwt_token')

        user_id = json_response.get('id')
        if user_id:
            print("Logged in as '%s' (%s)"
                  % (json_response['username'], json_response['email']))
        else:
            raise InvalidResponseError("Error while trying to log in:\n%s"
                                       % json_response)

        return user_id

    # --- Read user info.

    def get_user_info(self, user_id):
        """Get info data about the given user."""
        request_url = API_URL + 'users/' + str(user_id)
        r = requests.get(url=request_url)

        if r.status_code != 200:
            raise ValueError(r.text)

        json_response = r.json()
        user_info = json_converter.json_to_user(json_response)

        return user_info

    # --- Get trends.

    def get_trends(self, types=None, limit=10, page=0, from_language='en'):
        """Get Tinycards trends for the current user.

        Args:
            types (list): What entity to search for. Can be DECK, DECK_GROUP
                and/or USER.
            limit (int): What number of results to should be returned.
            page (int): The page to return when returning more than limit
                results (zero-indexed).
            from_language: The language used for learning.

        Returns: A list of Trendable objects.

        """
        if not types:
            types = ['DECK', 'DECK_GROUP']

        request_url = API_URL + 'trendables'
        params = {'types': ','.join(types),
                  'limit': limit,
                  'page': page,
                  'fromLanguage': from_language}
        r = requests.get(url=request_url, params=params,
                         cookies={'jwt_token': self.jwt})

        if r.status_code != 200:
            raise ValueError(r.text)

        json_response = r.json()
        json_trendables_list = json_response['trendables']
        trendables = [json_converter.json_to_trendable(trendable)
                      for trendable in json_trendables_list]

        return trendables

    # --- Subscriptions

    def subscribe(self, user_id):
        """Subscribe to the given user.

        Args:
            user_id: ID of the user to subscribe to.

        Returns: If successful, returns the ID of the user subscribed to.

        """
        request_url = API_URL + 'users/' + str(user_id) + '/subscriptions'
        r = requests.post(url=request_url, cookies={'jwt_token': self.jwt})

        json_response = r.json()
        added_subscription = json_response['addedSubscription']

        return added_subscription

    def unsubscribe(self, user_id):
        """Unsubscribe the given user.

        Args:
            user_id: ID of the user to unsubscribe.

        Returns: If successful, returns the ID of the unsubscribed user.

        """
        request_url = API_URL + 'users/' + str(user_id) + '/subscriptions'
        r = requests.delete(url=request_url, cookies={'jwt_token': self.jwt})

        json_response = r.json()
        removed_subscription = json_response['removedSubscription']

        return removed_subscription

    # --- Deck CRUD

    def get_decks(self, user_id, no_cards=False):
        """Get all Decks for the currently logged in user.

        Returns:
            list: The list of retrieved decks.

        """
        request_url = API_URL + 'decks?userId=' + str(user_id)
        r = requests.get(request_url, cookies={'jwt_token': self.jwt})

        if r.status_code != 200:
            raise ValueError(r.text)

        json_response = r.json()
        decks = []
        for d in json_response['decks']:
            current_deck = json_converter.json_to_deck(d)
            decks.append(current_deck)

        if no_cards:
            return decks
        else:
            return [self.get_deck(d.id, user_id) for d in decks]

    def get_deck(self, deck_id, user_id, include_cards=True):
        """Get the Deck with the given ID.

        Args:
            deck_id (str): The ID of the deck to retrieve.
            include_cards (bool): Only include the cards of the deck when set
                to True (as by default). Otherwise cards will be an empty list.

        Returns:
            Deck: The retrieved deck.

        """
        request_url = API_URL + 'decks/' + deck_id
        if include_cards:
            request_url += '?expand=true'
        r = requests.get(url=request_url, cookies={'jwt_token': self.jwt})
        json_response = r.json()

        deck = json_converter.json_to_deck(json_response)
        # Set additional properties.
        deck.id = deck_id

        return deck

    def create_deck(self, deck):
        """Create a new Deck for the currently logged in user.

        Args:
            deck (Deck): The Deck object to create.

        Returns:
            Deck: The created Deck object if creation was successful.

        """
        request_payload = json_converter.deck_to_json(deck)
        request_payload = to_multipart_form(request_payload)
        # Clone headers to not modify the global variable.
        headers = dict(DEFAULT_HEADERS)
        headers['Content-Type'] = request_payload.content_type
        r = requests.post(url=API_URL + 'decks', data=request_payload,
                          headers=headers, cookies={'jwt_token': self.jwt})

        json_data = r.json()
        created_deck = json_converter.json_to_deck(json_data)

        return created_deck

    def update_deck(self, deck, user_id):
        """Update an existing deck.

        Args:
            deck (Deck): The Deck object to update.

        Returns:
            Deck: The updated Deck object if update was successful.

        """
        # Clone headers to not modify the global variable.
        headers = dict(DEFAULT_HEADERS)
        if deck.cover:
            # A new cover has been set on the deck, send the PATCH request as a multipart-form:
            request_payload = json_converter.deck_to_json(deck)
            request_payload = to_multipart_form(request_payload)
            headers['Content-Type'] = request_payload.content_type
        else:
            # Otherwise, send the PATCH request as JSON:
            request_payload = json_converter.deck_to_json(deck, as_json_str=True)
            request_payload = json.dumps(request_payload)
            headers['Content-Type'] = 'application/json'

        r = requests.patch(url=API_URL + 'decks/' + deck.id,
                           data=request_payload, headers=headers,
                           cookies={'jwt_token': self.jwt})

        if not r.ok:
            raise Exception('Failure while sending updates to server: %s' % r.text)

        # The response from the PATCH request does not contain cards.
        # Therefore, we have to query the updated deck with an extra request.
        updated_deck = self.get_deck(deck.id, user_id)

        return updated_deck

    def delete_deck(self, deck_id):
        """Delete an existing deck.

        Args:
            deck_id (str): The ID of the Deck to delete.

        Returns:
            Deck: The deleted Deck object if deletion was successful.

        """
        if not isinstance(deck_id, str):
            raise ValueError("'deck_id' parameter must be of type str")

        headers = DEFAULT_HEADERS

        r = requests.delete(url=API_URL + 'decks/' + deck_id, headers=headers,
                            cookies={'jwt_token': self.jwt})

        json_data = r.json()
        deleted_deck = json_converter.json_to_deck(json_data)

        return deleted_deck

    # --- Favorites CR(U)D

    def get_favorites(self, user_id):
        """Get all favorites for the given user.

        Args:
            user_id (int): ID of the user to get favorites for.

        Returns:
            list: The list of favorites.

        """
        request_url = API_URL + 'users/%d/favorites' % user_id
        r = requests.get(url=request_url, cookies={'jwt_token': self.jwt})

        if r.status_code != 200:
            raise ValueError(r.text)

        json_response = r.json()
        json_favorite_decks = [fav for fav in json_response['favorites']
                               if 'deck' in fav]
        favorites = []
        try:
            for fav in json_favorite_decks:
                current_favorite = json_converter.json_to_favorite(fav)
                favorites.append(current_favorite)
        except KeyError as ke:
            raise Exception("Unexpected JSON format:\n%s" % ke)

        return favorites

    def add_favorite(self, user_id, deck_id):
        """Add a deck to the current user's favorites.

        Args:
            user_id (int): ID of the user to favorite the deck for.
            deck_id: The ID of the deck to be added.

        Returns:
            Favorite: The added favorite.

        """
        request_url = API_URL + 'users/%d/favorites' % user_id
        request_payload = {'deckId': deck_id}
        r = requests.post(url=request_url, json=request_payload,
                          cookies={'jwt_token': self.jwt})

        json_response = r.json()
        added_favorite = json_converter.json_to_favorite(json_response)

        return added_favorite

    def remove_favorite(self, user_id, favorite_id):
        """Add a deck to the current user's favorites.

        Args:
            user_id (int): ID of the user to favorite the deck for.
            favorite_id (str): The ID of the favorite to be removed.

        Returns:
            str: The ID of the removed favorite.

        """
        request_url = API_URL + 'users/%d/favorites/%s' % (user_id,
                                                           favorite_id)
        r = requests.delete(url=request_url, cookies={'jwt_token': self.jwt})

        json_response = r.json()
        removed_favorite_id = json_response['removedFavoriteId']

        return removed_favorite_id

    # --- Search

    def search(self,
               query,
               use_fuzzy_search=True,
               types=None,
               limit=10,
               page=0):
        """Searches for decks, deck groups, or users on Tinycards.

        Args:
            query (str): The used search term(s).
            use_fuzzy_search (bool): Whether or not to use fuzzy search.
            types (list): What entity to search for. Can be DECK, DECK_GROUP
                or USER.
            limit: Number of results to be returned.
            page: The page to return when more than `limit` results are
                available (zero-indexed).

        Returns: A list of Trendable objects.

        """
        if not types:
            types = ['DECK', 'DECK_GROUP']

        request_url = API_URL + 'searchables'
        params = {'query': query,
                  'useFuzzySearch': use_fuzzy_search,
                  'types': ','.join(types),
                  'limit': limit,
                  'page': page}
        r = requests.get(url=request_url, params=params,
                         cookies={'jwt_token': self.jwt})

        if r.status_code != 200:
            raise ValueError(r.text)

        json_response = r.json()
        json_searchables_list = json_response['searchables']
        searchables = [json_converter.json_to_searchable(searchable)
                       for searchable in json_searchables_list]

        return searchables
