"""
/jackbox/__init__.py

    Copyright (c) 2020 ShineyDev
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
        http://www.apache.org/licenses/LICENSE-2.0
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import collections
import logging

from jackbox.client import Client

from jackbox.bombintern import BombCorpClient
from jackbox.triviadeath2 import TriviaMurderParty2Client


__version__ = "0.1.1"

_VersionInfo = collections.namedtuple("_VersionInfo", "major minor micro releaselevel serial")
version_info = _VersionInfo(major=0, minor=1, micro=1, releaselevel="final", serial=0)


logging.getLogger("jackbox.py").addHandler(logging.NullHandler())
