import os

from pymongo import MongoClient

from .utils import make_url_id
from .static import CHARS, URL_ID_LENGTH
from .exceptions import NoSuchUrlIdError


class DBInterface:
    def __init__(self):
        if uri := os.environ.get("MONGODB_URI"):
            client = MongoClient(uri)
        else:
            client = MongoClient()
        db = client.urls_db # database
        self.urls = db.urls # collection

    def shorten_url(self, url: str) -> str:
        """
        Creates a url id for the given url
            and adds both to the db
        """

        urls_count = self.urls.estimated_document_count()
        url_id = make_url_id(CHARS, URL_ID_LENGTH, urls_count)
        self.urls.insert_one({
            "url": url,
            "url_id": url_id
        })
        return url_id

    def get_url_by_id(self, url_id: str) -> str:
        """
        Gets the url for the given url id from
            the db
        """

        try:
            found_url = self.urls.find({"url_id": url_id}).next()
        except StopIteration:
            raise NoSuchUrlIdError
        else:
            return found_url["url"]