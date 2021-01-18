import glob

from mg.io import print, input


def run_checkup(deck, options):
    print("orphaned references in data files...")
    cardkeys = {c.link.index() for c in deck.allcards}
    for db in deck.dbs:
        lostkeys = []
        for key in db:
            if key not in cardkeys:
                lostkeys.append(key)
        for oldkey in lostkeys:
            print("oldkey:", oldkey)
            newkey = input("newkey:", r="(enter to delete row)")
            if newkey:
                db[newkey] = db[oldkey]
            del db[oldkey]
    print("TODO: Also apply this mapping to the log file?")
