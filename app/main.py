from os import getenv
import boto3
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

    AWS_ACCESS_KEY_ID = getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = getenv("AWS_SECRET_ACCESS_KEY")
    S3_BUCKET = getenv("S3_BUCKET")
    S3_KEY_PREFIX = getenv("S3_KEY_PREFIX")
    S3_ENDPOINT = getenv("S3_ENDPOINT", None)
    SSL_ENABLED = False if getenv("SSL_ENABLED") == "False" else True
    
    s3_client = boto3.client(service_name="s3",
                             use_ssl=SSL_ENABLED,
                             endpoint_url=S3_ENDPOINT,
                             aws_access_key_id=AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    logging.info("Recursively watching: {}".format(RECURSIVE_WATCH_PATH))
    i = inotify.adapters.InotifyTree(RECURSIVE_WATCH_PATH)

    for event in i.event_gen(yield_nones=False):
        (_, type_names, path, filename) = event
        logging.info("PATH=[{}] FILENAME=[{}] EVENT_TYPES={}".format(path, filename, type_names))

        # Ignore directory events
        if "IN_ISDIR" not in type_names:
            # Watch for file closure events
            if ("IN_CLOSE_WRITE" in type_names) and filename is not None:
                logging.info("Uploading file {}/{}".format(path, filename))
                response = s3_client.upload_file("{}/{}".format(path, filename),
                                                S3_BUCKET,
                                                "{}/{}".format(S3_KEY_PREFIX, filename))
                logging.info(response)

if __name__ == "__main__":
    main()
