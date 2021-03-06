#!/usr/bin/env python3
try:
    import lz4.block as lz4
except ImportError:
    import lz4
import argparse
import json
import yaml

# todo: nearly everything... especially pinned/active tabs
# todo: nested sessionrestore in nested yaml files?
browser_default_input_format = {
    'firefox': 'mozilla',
}


def parse_firefox_windows(windows):
    # handle the windows-array (for sessionrestore)
    qute = {"windows": []}
#    print("Converting %i open windows" % (len(windows)))
    count = 0
#    for window in fsession["windows"]:
    for window in windows:
        qutewindow = {"active": True, "tabs": [], "geometry":"FOOBAR"}
        # I sed replace FOOBAR later with a valid geometry, but for not this
        # has to do
        for tab in window["tabs"]:
            count+=1
#            print(count)
            history = [] # history of the tab
            for entry in tab["entries"]:
#                print(entry["url"])
                if entry["url"] == "about:sessionrestore":
                    pass
#                    qute["windows"] += \
#                    parse_firefox_windows(tab["formdata"]["id"]["sessionData"]["windows"])["windows"]
                else:
                    if ("url" in entry) and ("title" in entry):
                        history.append({"url":entry["url"],
                                            "title":entry["title"],
                                            "pinned":False})
                    elif not("url" in entry) and "title" in entry:
                        history.append({"url": "urlcouldnotbeloaded",
                                            "title":entry["title"],
                                            "pinned":False})
                    elif not("title" in entry) and "url" in entry:
                        history.append({"url":entry["url"],
                                            "title":"Title could not be loaded",
                                            "pinned":False})
                    else:
                        history.append({"url":"urlcouldnotbeloaded",
                                            "title":"Title could not be loaded",
                                            "pinned":False})
            if len(history)>0:
                history[-1]["active"]=1
                qutewindow["tabs"].append({"history":history, "url":history[-1]["url"], "title":history[-1]["title"]})
        qute["windows"].append(qutewindow)
    return qute


def open_firefox_session():
    # hardcoded for PoC
    session="/home/thomas/.mozilla/firefox.backup/p0i4j91j.default-backup-crashrecovery-20190418_144722/sessionstore-backups/previous.jsonlz4"
    # firefox format:
    # windows->tabs->entries (can have sub windows->tabs->entries)
    # qutebrowser format:
    # {'windows': tabs: { history:{active:true, pinned:false, title:Foo, url:
    # Bar, zoom: 1.0}
    # history: original_url, url, url, ...
    sessf = open(session, 'rb')
    assert sessf.read(8) == b'mozLz40\0'
#    sessf.seek(8)
#    print(sessf.read())
    fsession = json.loads(lz4.decompress(sessf.read()))
    qute = parse_firefox_windows(fsession["windows"])
#    print(fsession)
    print(yaml.dump(qute, default_flow_style=False))

open_firefox_session()

