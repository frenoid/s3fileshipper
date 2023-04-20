import inotify.adapters
import logging
import sys

logging.basicConfig(stream=sys.stdout,
                    level=logging.DEBUG,
                    format="%(asctime)s %(message)s",
                    datefmt="%m/%d/%Y &I:%M:%S %p")

def main():
    logging.info("Start inotify")
    i = inotify.adapters.Inotify()

    logging.info("Watching/tmp")
    i.add_watch("/tmp")

    with open("/tmp/test_file", "w"):
        pass

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event
        logging.info("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(path, filename, type_names))

if __name__ == "__main__":
    main()
