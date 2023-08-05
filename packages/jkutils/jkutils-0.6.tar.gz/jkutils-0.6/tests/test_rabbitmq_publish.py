from jkutils.rabbitmq import MQPublisher


def test_pulish():
    p = MQPublisher("amqp://xxx:xxx@127.0.0.1:20003/")
    p.publish(exchange="test", exchange_type="topic", durable=True, routing_key="teddy", msg="xxx")
    assert True


def test_pulish_with_properties():
    p = MQPublisher("amqp://xxx:xxx@127.0.0.1:20003/")
    p.publish(exchange="test", exchange_type="topic", durable=True, routing_key="teddy", msg="xxx",
              properties={"delivery_mode": 2})
    assert True
