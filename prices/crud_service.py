# coding=utf_8

import utils.mongo as db
import utils.errors as error
import bson.objectid as bson
from datetime import datetime
import prices.price_schema as schema
# import ipdb; ipdb.set_trace()


def getPrice(articleId):

    try:
        print('TCL: articleId', articleId);
        result = db.prices.find_one({"_id": bson.ObjectId("5bdb8bde2f49670e3c373a57")})
        strDate = result['fechaDesde']
        # strDate = '2/4/18'
        objDate = datetime.strptime(strDate, '%m/%d/%y')
        print('TCL: result', result)
        print('TCL: result', objDate.day)
        # for price in result: 
        #     print("el dia es ")
        #     print("hola")
        #     x = datetime.datetime.now()
        #     print("fechaDesde " + x.year)
            # dy = datetime.strptime(price["fechaDesde"], '%j')
        if (not result):
            raise error.InvalidArgument("_id", "Document does not exists")
        return result
    except Exception:
        raise error.InvalidArgument("_id", "Invalid object id")


def addPrice(params):

    return _addOrUpdatePrice(params)


def updatePrice(articleId, params):

    # params["_id"] = priceId

    prices = schema.newPrice()

    print('TCL: params["article_id"]', params["article_id"])
    isNew = False
    prices = getPrice(params["article_id"])
    print('TCL: prices', prices);

    
    # Actualizamos los valores validos a actualizar
    prices.update(params)

    # prices["updated"] = datetime.datetime.utcnow()

    schema.validateSchema(prices)

    del prices["_id"]
    r = db.prices.replace_one(
        {"_id": bson.ObjectId(params["_id"])}, prices)
    prices["_id"] = params["_id"]
    
    return prices


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

    prices["updated"] = datetime.datetime.utcnow()

    schema.validateSchema(prices)

    if (not isNew):
        del prices["_id"]
        r = db.prices.replace_one(
            {"_id": bson.ObjectId(params["_id"])}, prices)
        prices["_id"] = params["_id"]
    else:
        prices["_id"] = db.prices.insert_one(prices).inserted_id

    return prices
