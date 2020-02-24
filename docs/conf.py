"""
/docs/conf.py
"""

import os
import re
import sys


sys.path.insert(0, os.path.abspath(".."))


# extensions

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.extlinks",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
    "sphinxcontrib_trio",
]

autodoc_typehints = "none"

intersphinx_mapping = {
    "aiohttp": ("https://aiohttp.readthedocs.io/en/stable/", None),
    "python": ("https://docs.python.org/3", None),
    "websockets": ("https://websockets.readthedocs.io/en/stable/", None),
}

# main config

highlight_language = "python3"
html_experimental_html5_writer = True
html_static_path = ["_static"]
html_theme = "alabaster"
master_doc = "index"
pygments_style = "friendly"
source_suffix = ".rst"

# project information

copyright = "2020, ShineyDev"
project = "jackbox.py"

with open("../jackbox/__init__.py", "r") as file_stream:
    release = re.search(r"^__version__ = [\"]([^\"]*)[\"]", file_stream.read(), re.MULTILINE).group(1)

# reST config

rst_prolog = """
.. |coro| replace:: This function is a |coroutine_link|_.
.. |coroutine_link| replace:: *coroutine*
.. _coroutine_link: https://docs.python.org/3/library/asyncio-task.html#coroutine
.. |jackbox_games| replace:: Jackbox Games services
.. _jackbox_games: https://jackboxgames.com/
.. |jackbox_party_pack| replace:: Jackbox Party Pack
.. _jackbox_party_pack: https://jackboxgames.com/games/
"""
