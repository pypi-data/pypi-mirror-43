from jkutils.rabbitmq import MQPublisher


def test_report():
    p = MQPublisher("amqp://xxx:xxx@127.0.0.1:111/")
    p.publish(exchange="test", exchange_type="topic", durable=True, routing_key="teddy", msg="xxx")
    assert True
