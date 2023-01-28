from mg.mgio import print, input

def run_checkup(graph, db, log, options):
    loaded_keys = set(graph.keys)
    
    # check database
    stored_keys = set(db.keys())
    print("orphaned keys in database:")
    for key in stored_keys - loaded_keys:
        print('<bold>*<reset>', key)
    
    # check log
    logged_keys = set(l['id'] for l in log.old_lines)
    print("orphaned keys in log file:")
    for key in logged_keys - loaded_keys:
        print('<bold>*<reset>', key)

