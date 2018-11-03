# coding=utf_8

import utils.mongo as db
import utils.errors as error
import bson.objectid as bson
from datetime import datetime
import prices.price_schema as schema
# import ipdb; ipdb.set_trace()


def getPrice(articleId):

    try:
        # print('TCL: articleId', articleId)
        # print("va a buscar")
        result = db.prices.find({"article_id": articleId})
        ultimoPrecioSuma = 0
        ultimoPrecio = {}
        # print("result", result)
        for price in result: 
            # print("price", price)
            strDate = price['fechaDesde']
            # print('TCL: strDate', strDate);
            objDate = datetime.strptime(strDate, '%Y-%m-%dT%H:%M:%S')
            # print('TCL: objDate', objDate)
            # print("el día de creación es: ",objDate.day)
            sumaPrecio = objDate.day + objDate.month + objDate.year + objDate.hour + objDate.minute
            # print("sumatoria de la fecha ",sumaPrecio)
            if(sumaPrecio > ultimoPrecioSuma):
                ultimoPrecioSuma = sumaPrecio
                # print("el mayor es ",sumaPrecio)
                ultimoPrecio = price
        print("resulto mayor: ",ultimoPrecio['_id'])

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
    # print('TCL: prices', prices);

    
    # Actualizamos los valores validos a actualizar
    prices.update(params)

    # print("params: ",params)

    prices["updated"] = datetime.utcnow()
    params["_id"] = prices["_id"]

    schema.validateSchema(prices)

    del prices["_id"]
    r = db.prices.replace_one(
        {"_id": bson.ObjectId(params["_id"])}, prices)
    prices["_id"] = params["_id"]

    response = {}
    response["article_id"] = prices["article_id"]
    response["message"] = "Precio actualizado con exito"
    
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
        prices["_id"] = db.prices.insert_one(prices).inserted_id

    return prices
