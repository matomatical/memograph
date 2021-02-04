import sys

from mg.io      import print
from mg.options import get_options
from mg.graph   import KnowledgeGraph
from mg.data    import Database, Log, load_graph

from mg.main.status  import run_status
from mg.main.drill   import run_drill
from mg.main.learn   import run_learn
from mg.main.checkup import run_checkup

def main():
    # parse command-line input
    options = get_options()
    print("<bold>**<reset> welcome <bold>**<reset>")

    # load graph and memory model data
    try:
        db = Database(options.db_path)
        log = Log(options.log_path)
        graph = KnowledgeGraph(load_graph(options.graph_path), db, log)
    except Exception as e:
        print("<red><bold>error:<reset>", e)
        sys.exit(1)

    # run program
    saving = False
    try:
        if options.subcommand == "status":
            saving = False
            run_status(graph, options)
        elif options.subcommand == "drill":
            saving = True
            run_drill(graph, options)
        elif options.subcommand == "review":
            saving = True
            run_drill(graph, options, review=True)
        elif options.subcommand == "learn":
            saving = True
            run_learn(graph, options)
        elif options.subcommand == "checkup":
            saving = True
            run_checkup(graph, options)
        else:
            saving = False
            print(subcommand, "not implemented")
    except KeyboardInterrupt:
        print("\nbye!")
    except EOFError:
        print("\nbye! (not saving)")
        saving = False
    if saving:
        print("saving...", flush=True, end=" ")
        db.save()
        log.save()
        print("done!")

