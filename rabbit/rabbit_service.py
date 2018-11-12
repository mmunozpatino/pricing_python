# # coding=utf_8

import pika
import utils.security as security
import threading
import utils.json_serializer as json
import utils.config as config
# import articles.rest_validations as articleValidation
# import articles.crud_service as crud
import utils.schema_validator as validator
import traceback

EVENT = {
    "type": {
        "required": True,
        "type": str
    },
    "message": {
        "required": True
    }
}

EVENT_CALLBACK = {
    "type": {
        "required": True,
        "type": str
    },
    "message": {
        "required": True
    },
    "exchange": {
        "required": True
    },
    "queue": {
        "required": True
    }
}


MSG_ARTICLE_EXIST = {
    "articleId": {
        "required": True,
        "type": str
    },
    "referenceId": {
        "required": True,
        "type": str
    }
}


def init():
    """
    Inicializa los servicios Rabbit
    """
    initAuth()
    initCatalog()


def initAuth():
    """
    Inicializa RabbitMQ para escuchar eventos logout.
    """
    authConsumer = threading.Thread(target=listenAuth)
    authConsumer.start()


def initCatalog():

    catalogConsumer = threading.Thread(target=listenCatalog)
    catalogConsumer.start()


def listenAuth():
    EXCHANGE = "auth"

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=config.get_rabbit_server_url()))
        channel = connection.channel()

        channel.exchange_declare(exchange=EXCHANGE, exchange_type='fanout')

        result = channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange=EXCHANGE, queue=queue_name)

        def callback(ch, method, properties, body):
            event = json.body_to_dic(body.decode('utf-8'))
            if(len(validator.validateSchema(EVENT, event)) > 0):
                return

            if (event["type"] == "logout"):
                security.invalidateSession(event["message"])

        print("RabbitMQ Auth conectado")

        channel.basic_consume(callback, queue=queue_name, no_ack=True)

        channel.start_consuming()
    except Exception:
        print("RabbitMQ Auth desconectado, intentando reconectar en 10'")
        threading.Timer(10.0, initAuth).start()

def listenCatalog():

    EXCHANGE = "catalog"
    QUEUE = "catalog"

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=config.get_rabbit_server_url()))
        channel = connection.channel()

        channel.exchange_declare(exchange=EXCHANGE, exchange_type='direct')

        channel.queue_declare(queue=QUEUE)

        channel.queue_bind(queue=QUEUE, exchange=EXCHANGE, routing_key=QUEUE)

        def callback(ch, method, properties, body):
            event = json.body_to_dic(body.decode('utf-8'))
            if(len(validator.validateSchema(EVENT_CALLBACK, event)) > 0):
                return

            if (event["type"] == "article-exist"):
                message = event["message"]
                if(len(validator.validateSchema(MSG_ARTICLE_EXIST, message)) > 0):
                    return

                exchange = event["exchange"]
                queue = event["queue"]
                referenceId = message["referenceId"]
                articleId = message["articleId"]

                print("RabbitMQ Catalog GET article-exist catalogId:%r , articleId:%r", referenceId, articleId)

                try:
                    articleValidation.validateArticleExist(articleId)
                    sendArticleValid(exchange, queue, referenceId, articleId, True)
                except Exception:
                    sendArticleValid(exchange, queue, referenceId, articleId, False)

            if (event["type"] == "article-data"):
                message = event["message"]
                if(len(validator.validateSchema(MSG_ARTICLE_EXIST, message)) > 0):
                    return

                exchange = event["exchange"]
                queue = event["queue"]
                referenceId = message["referenceId"]
                articleId = message["articleId"]

                print("RabbitMQ Catalog GET article-data catalogId:%r , articleId:%r", referenceId, articleId)

                try:
                    article = crud.getArticle(articleId)
                    valid = ("enabled" in article and article["enabled"])
                    stock = article["stock"]
                    price = article["price"]
                    articleValidation.validateArticleExist(articleId)
                    sendArticleData(exchange, queue, referenceId, articleId, valid, stock, price)
                except Exception:
                    sendArticleData(exchange, queue, referenceId, articleId, False, 0, 0)

        print("RabbitMQ Catalog conectado")

        channel.basic_consume(callback, queue=QUEUE, consumer_tag=QUEUE, no_ack=True)

        channel.start_consuming()
    except Exception:
        traceback.print_exc()
        print("RabbitMQ Catalog desconectado, intentando reconectar en 10'")
        threading.Timer(10.0, initCatalog).start()

def sendNewPrice(exchange, queue, type, prices):

    print("LLAMA A LA FUNCION")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.get_rabbit_server_url()))
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange, exchange_type='fanout')
    channel.queue_declare(queue = queue)

    message = {
        "type": type,
        "message": prices
    }

    channel.basic_publish(exchange=exchange, routing_key=queue, body=json.dic_to_json(message))
    print("llega")
    print(" [x] Sent %r" % message)

    connection.close()


def sendNewDiscount(exchange, queue, type, Discounts):

    # print("LLAMA A LA FUNCION")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=config.get_rabbit_server_url()))
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange, exchange_type='fanout')
    channel.queue_declare(queue = queue)

    message = {
        "type": type,
        "message": Discounts
    }

    channel.basic_publish(exchange=exchange, routing_key=queue, body=json.dic_to_json(message))
    # print("llega")
    print(" [x] Sent %r" % message)

    connection.close()
