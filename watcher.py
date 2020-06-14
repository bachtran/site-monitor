""" Website status checker """
import argparse
import common
import config
import json
import time


def perform_site_check():
    status = checker.get_status()
    print(status)
    # Send message to kafka, json encoded
    message = json.dumps(status._asdict())
    print('Sending')
    message_stream.send_message(message)
    print('Sent')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--url",
                        help="Overwrite the SITE_TO_CHECK config if specified")
    parser.add_argument("--interval",
                        help="Optional. When specified check is repeated with given interval in seconds",
                        type=int)
    parser.add_argument("--regex",
                        help="Optional. When specified the site return text is checked against regex")
    args = parser.parse_args()

    checker = common.WebsiteChecker(args.url if args.url else config.SITE_TO_CHECK, regex=args.regex)
    print('Connecting')
    message_stream = common.MessageStream(
        config.KAFKA_CA_CERT,
        config.KAFKA_ACCESS_CERT,
        config.KAFKA_ACCESS_KEY,
        config.KAFKA_URI,
        config.KAFKA_TOPIC,
    )

    if args.interval:
        while True:
            perform_site_check()
            time.sleep(args.interval)

    perform_site_check()

