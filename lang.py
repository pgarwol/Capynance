import configparser
from main import App

pl = configparser.ConfigParser()
en = configparser.ConfigParser()
pl.read("lang_pl.properties")
en.read("lang_en.properties")

# Access properties
pl_val = pl.get("login", "do_login")
en_val = en.get("login", "do_login")


# def lang(key: str) -> str:
#     # used_lang = main.App.session.language  # TODO: get lang from Session
#     print(used_lang)
#     print(pl.get("login", "do_login"))
