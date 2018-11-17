# coding=utf_8

import utils.mongo as db
import utils.errors as error
import bson.objectid as bson
from datetime import datetime
import discounts.discount_schema as schema

import random
import string

from rabbit.rabbit_service import sendNewDiscount



def getDiscount(discountCode):
    
    try:
        # print("va a buscar")
        result = db.discounts.find_one({"discount_code": discountCode})
        # print("result", result)

        if (not result):
            raise error.InvalidArgument("_id", "Document does not exists")
        return result
    except Exception: 
        raise error.InvalidArgument("_id", "Invalid object id")


def getDiscountByArticle(articleId):
    try:
        result = db.discounts.find({"article_id": articleId})
        discounts = []
        for discount in result:
            discounts.append(discount)
        if( not result ):
            raise error.InvalidArgument("_id", "Document does not exists")
        return discounts
    except Exception:
        raise error.InvalidArgument("_id", "Invalid object id")

def getDiscountByDate(articleId, discountDate):
    
    try:
        print("llego ",discountDate)
        discountDate = datetime.strptime(discountDate, '%d/%m/%y')

        result = db.discounts.find({"article_id": articleId})
        resultPrice = {}
        for price in result: 
            strDate = price['fechaDesde']
            objDate = datetime.strptime(strDate, '%Y-%m-%dT%H:%M:%S')
            if(objDate.year == discountDate.year and objDate.month == discountDate.month and objDate.day == discountDate.day):
                # print("encontró", price)
                resultPrice = price
                # return price
        if(resultPrice):
            return resultPrice
        else:
            return {}

        if (not result):
            raise error.InvalidArgument("_id", "Document does not exists")
        return ultimoPrecio
    except Exception: 
        raise error.InvalidArgument("_id", "Invalid object id")


def addDiscount(params):
    code = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(6))

    params['discount_code'] = code

    # print ("el codigo generado es: "+code)
    return _addOrUpdateDiscount(params)


def updateDiscount(discountCode, params):
    print('TCL: discountCode', discountCode);
    
    # params["_id"] = discountId

    discounts = schema.newDiscount()

    # print('TCL: params["article_id"]', params["article_id"])
    isNew = False
    discounts = getDiscount(discountCode)
    # print('TCL: discounts', discounts);

    
    # Actualizamos los valores validos a actualizar
    discounts.update(params)

    # print("params: ",params)

    discounts["updated"] = datetime.utcnow()
    params["_id"] = discounts["_id"]

    schema.validateSchema(discounts)

    del discounts["_id"]
    r = db.discounts.replace_one(
        {"_id": bson.ObjectId(params["_id"])}, discounts)
    discounts["_id"] = params["_id"]

    response = {}
    response["article_id"] = discounts["article_id"]
    response["message"] = "Descuento actualizado con exito"
    menssage= {}
    menssage['article'] = discounts["article_id"]
    menssage['discount_code'] = discounts['discount_code']
    sendNewDiscount("discounts", "discounts", "update-discount", menssage)

    
    return response


def delArticle(articleId):
    article = getArticle(articleId)
    article["updated"] = datetime.datetime.utcnow()
    article["enabled"] = False
    db.articles.save(article)


def _addOrUpdateDiscount(params):
    """
    Agrega o actualiza un articulo. \n
    params: dict<property, value>) Articulo\n
    return dict<propiedad, valor> Articulo
    """
    isNew = True

    discounts = schema.newDiscount()

    if ("_id" in params):
        isNew = False
        discounts = getdiscounts(params["_id"])

    # Actualizamos los valores validos a actualizar
    discounts.update(params)

    discounts["updated"] = datetime.utcnow()

    schema.validateSchema(discounts)

    if (not isNew):
        del discounts["_id"]
        r = db.discounts.replace_one(
            {"_id": bson.ObjectId(params["_id"])}, discounts)
        discounts["_id"] = params["_id"]
    else:
        discounts["_id"] = db.discounts.insert_one(discounts).inserted_id
        response = {}
        menssage = {}
        response['article'] = discounts["article_id"]
        response['discount_code'] = discounts['discount_code']
        response['message'] = 'Descuento creado con éxito'
        menssage['article'] = discounts["article_id"]
        menssage['discount_code'] = discounts['discount_code']
        sendNewDiscount("discounts", "discounts", "new-discount", menssage)


    return response
