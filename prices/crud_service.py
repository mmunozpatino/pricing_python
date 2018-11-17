# coding=utf_8

import utils.mongo as db
import utils.errors as error
import bson.objectid as bson
from datetime import datetime
import prices.price_schema as schema

from rabbit.rabbit_service import sendNewPrice
# from rabbit.rabbit_service import sendChangePrice


def getPrice(articleId):

    try:
        # print('TCL: articleId', articleId)
        # print("va a buscar")
        # TODO: verificar también la vigencia de los precios y ver la suma
        result = db.prices.find({"article_id": articleId})
        ultimoPrecioSuma = 0
        ultimoPrecio = {}
        # print("result", result)
        for price in result:
            # print("price", price)
            strDate = price['fechaDesde']
            print('TCL: strDate', strDate)
            objDate = datetime.strptime(strDate, '%Y-%m-%dT%H:%M:%S')
            # print('TCL: objDate', objDate)
            # print("el día de creación es: ",objDate.day)
            sumaPrecio = objDate.day + objDate.month + \
                objDate.year + objDate.hour + objDate.minute
            # print("sumatoria de la fecha ",sumaPrecio)
            if(sumaPrecio > ultimoPrecioSuma):
                ultimoPrecioSuma = sumaPrecio
                # print("el mayor es ",sumaPrecio)
                ultimoPrecio = price
        print("el precio mayor es: ", ultimoPrecioSuma)
        print("resulto mayor: ", ultimoPrecio)


        if (not result):
            raise error.InvalidArgument("_id", "Document does not exists")
        return ultimoPrecio
    except Exception:
        raise error.InvalidArgument("_id", "Invalid object id")


def getPriceByDate(articleId, priceDate):

    try:
        print("llego ", priceDate)
        priceDate = datetime.strptime(priceDate, '%d/%m/%y')

        result = db.prices.find({"article_id": articleId})
        resultPrice = {}
        for price in result:
            strDate = price['fechaDesde']
            objDate = datetime.strptime(strDate, '%Y-%m-%dT%H:%M:%S')
            if(objDate.year == priceDate.year and objDate.month == priceDate.month and objDate.day == priceDate.day):
                # print("encontró", price)
                resultPrice = price
                # return price
        if(resultPrice):
                
            resp = {}
            resp['fechaDesde'] = resultPrice['fechaDesde']
            resp['price'] = resultPrice['price']
            resp['article_id'] = resultPrice['article_id']
            return resp
        else:
            return {}

        if (not result):
            raise error.InvalidArgument("_id", "Document does not exists")
        return ultimoPrecio
    except Exception:
        raise error.InvalidArgument("_id", "Invalid object id")


def addPrice(params):

    return _addOrUpdatePrice(params)


def updatePrice(articleId, params):

    # params["_id"] = priceId

    prices = schema.newPrice()

    # print('TCL: params["article_id"]', params["article_id"])
    isNew = False
    prices = getPrice(params["article_id"])
    print('TCL: prices', prices);

    # Actualizamos los valores validos a actualizar
    prices.update(params)
    print('TCL: prices', prices);

	# print("​prices: ", prices)

    print("params: ",params)

    prices["updated"] = datetime.utcnow()
    # params["_id"] = prices["_id"]
    print("prices Up: ",prices)

    schema.validateSchema(prices)

    params["_id"] = prices["_id"]
    del prices["_id"]
    r = db.prices.replace_one(
        {"_id": bson.ObjectId(params["_id"])}, prices)
    prices["_id"] = params["_id"]

    response = {}
    response["article_id"] = prices["article_id"]
    response["message"] = "Precio actualizado con exito"

    menssage = {}
    menssage['article'] = prices["article_id"]
    menssage['price'] = prices['price']
    sendNewPrice("prices", "prices", "update-price", menssage)

    return response


def delArticle(articleId):

    article = getArticle(articleId)
    article["updated"] = datetime.datetime.utcnow()
    article["enabled"] = False
    db.articles.save(article)


def _addOrUpdatePrice(params):
    print('TCL: params', params)

    isNew = True

    prices = schema.newPrice()

    if ("_id" in params):

        print('TCL: params["article_id"]', params["article_id"])
        isNew = False
        prices = getPrice(params["article_id"])

    # Actualizamos los valores validos a actualizar
    prices.update(params)

    prices["updated"] = datetime.utcnow()

    schema.validateSchema(prices)

    if (not isNew):
        del prices["_id"]
        r = db.prices.replace_one(
            {"_id": bson.ObjectId(params["_id"])}, prices)
        prices["_id"] = params["_id"]
    else:
        response = {}
        menssage = {}
        response["article_id"] = prices["article_id"]
        response["message"] = "Precio creado con exito"
        menssage['article'] = prices["article_id"]
        menssage['price'] = prices['price']
        prices["_id"] = db.prices.insert_one(prices).inserted_id
        sendNewPrice("prices", "prices", "new-price", menssage)

    return response
