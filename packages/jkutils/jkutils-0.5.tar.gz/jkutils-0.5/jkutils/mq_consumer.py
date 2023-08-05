import pika

parameters = pika.URLParameters("amqp://xxwdev:xxwdev2018@172.16.1.49:20003/")


def on_message(channel, method_frame, header_frame, body):
    print(method_frame.delivery_tag)
    print(body)
    print()
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.basic_consume(on_message, "test")
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()
