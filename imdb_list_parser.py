import requests as r
import pandas as pd
from bs4 import BeautifulSoup as bs

class IMDBparser:
    """IMDBparser - Parses IMDB lists.
    """    
    def __init__(self, list_url):
        self.list_url: str

        self.list_url = list_url
        if not self.list_url.startswith("https://"):
            raise("list_url must start with an \"https://\".")
        
        if not self.list_url.find("imdb.com"):
            raise("list_url must point to \"imdb.com\". Domain not found.")

        if not self.list_url.find("imdb.com/list/"):
            raise("list_url must point to an IMDB list.")


    def _fetch_contents(self):
        _html_contents = r.get(self.list_url).content
        _html_parsed_contents = bs(_html_contents, "html.parser")
        self._list_items = _html_parsed_contents.find_all("div", "lister-item-content")


    def get_list(self) -> dict:
        """get_list() - Fetches HTML contents of an IMDB list webpage and sorts the data into a dictionary.

        Returns:
            dict: Dictionary of IMDB list.
        """        
        self._fetch_contents()
        _master_dict = []

        for movie in self._list_items:
            _movie_title = movie.select("h3.lister-item-header > a")[0].text
            _movie_rating = movie.select("span.ipl-rating-star__rating")[0].text
            _movie_votes = movie.find("span", {"name": "nv"})["data-value"]
            _movie_director = ""
            _movie_stars = ""
            _movie_gross = ""
            _master_dict.append(
                {
                    "movie_title": _movie_title,
                    "movie_rating": _movie_rating,
                    "movie_votes": _movie_votes
                }
            )
        return _master_dict


    def print_list(self):
        """print_list() - Uses the get_list() method and prints the return value to STDOUT.
        """        
        self._fetch_contents()
        print(self.get_list())



## Example usage:
# IMDB_LIST_URL = "https://www.imdb.com/list/ls021407125/"
# list_a = IMDBparser(IMDB_LIST_URL)


## Pandas example to save the output of get_list() to an Excel spreadsheet (Linux/Mac).
# import os
# myhome = os.getenv("HOME")
# df = pd.DataFrame(master_dict)
# df.to_excel(f"{myhome}/Desktop/imdb_list.xlsx", index=False)

if __name__ == "__main__":
    pass

