#!/usr/bin/env python3
try:
    import lz4.block as lz4
except ImportError:
    import lz4
import argparse
import json
from sys import stdin, stdout, argv, stderr

browser_default_input_format = {
    'firefox': 'mozilla',
}

def open_firefox_session():
    # hardcoded for PoC
    session="/home/thomas/.mozilla/firefox.backup/p0i4j91j.default-backup-crashrecovery-20190418_144722/sessionstore-backups/previous.jsonlz4"
    # firefox format:
    # windows->tabs->entries (can have sub windows->tabs->entries)
    # qutebrowser format:
    # {'windows': tabs: { history:{active:true, pinned:false, title:Foo, url:
    # Bar, zoom: 1.0}
    sessf = open(session, 'rb')
    assert sessf.read(8) == b'mozLz40\0'
#    sessf.seek(8)
#    print(sessf.read())
    firesession = json.loads(lz4.decompress(sessf.read()))
    print(json.dumps(firesession))



open_firefox_session()
