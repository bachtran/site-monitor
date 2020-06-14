""" Website status recorder """
import common
import config
import json

if __name__ == '__main__':
    print('Connecting')
    message_stream = common.MessageStream(
            config.KAFKA_CA_CERT,
            config.KAFKA_ACCESS_CERT,
            config.KAFKA_ACCESS_KEY,
            config.KAFKA_URI,
            config.KAFKA_TOPIC,
    )
    print('Receiving')
    postgres = common.Database(config.POSTGRES_URI)
    for msg in message_stream.receive_message():
        print(msg)
        decoded_msg = json.loads(msg.value)
        print(decoded_msg)
        with postgres as db:
            print('Saving in database')
            db.insert_event(decoded_msg)
            print('Saved')
