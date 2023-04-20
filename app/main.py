from os import getenv
import inotify.adapters
import logging
import sys

logging.basicConfig(stream=sys.stdout,
                    level=logging.DEBUG,
                    format="%(asctime)s %(message)s",
                    datefmt="%m/%d/%Y &I:%M:%S %p")



def main():
    logging.info("Start inotify")
    RECURSIVE_WATCH_PATH: str = getenv("RECURSIVE_WATCH_PATH", None)

    if RECURSIVE_WATCH_PATH is None:
        logging.info("Watches are None")
        logging.info("RECURSIVE_WATCH_PATH must be non-empty")
        sys.exit(1)
            

    logging.info("Recursively watching: {}".format(RECURSIVE_WATCH_PATH))
    i = inotify.adapters.InotifyTree(RECURSIVE_WATCH_PATH)

    with open("/tmp/test_file", "w"):
        pass
    with open("/tmp/norman", "w"):
        pass
    with open("/tmp/file1.txt", "w"):
        pass

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event
        logging.info("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(path, filename, type_names))

if __name__ == "__main__":
    main()
