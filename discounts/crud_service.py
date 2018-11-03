# coding=utf_8

import utils.mongo as db
import utils.errors as error
import bson.objectid as bson
from datetime import datetime
import discounts.discount_schema as schema

import random
import string


def getDiscount(articleId):
    
    try:
        # print('TCL: articleId', articleId)
        print("va a buscar")
        result = db.discounts.find({"article_id": articleId})
        ultimoDescuentoSuma = 0
        ultimoDescuento = {}
        print("result", result)
        for discount in result: 
            print("discount", discount)
            strDate = discount['fechaDesde']
            print('TCL: strDate', strDate);
            objDate = datetime.strptime(strDate, '%Y-%m-%dT%H:%M:%S')
            print('TCL: objDate', objDate)
            print("el día de creación es: ",objDate.day)
            sumaPrecio = objDate.day + objDate.month + objDate.year + objDate.hour + objDate.minute
            # print("sumatoria de la fecha ",sumaPrecio)
            if(sumaPrecio > ultimoDescuentoSuma):
                ultimoDescuentoSuma = sumaPrecio
                # print("el mayor es ",sumaPrecio)
                ultimoDescuento = discount
        print("resulto mayor: ",ultimoDescuento['_id'])

        if (not result):
            raise error.InvalidArgument("_id", "Document does not exists")
        return ultimoDescuento
    except Exception: 
        raise error.InvalidArgument("_id", "Invalid object id")



def addDiscount(params):
    code = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(6))

    params['discount_code'] = code

    # print ("el codigo generado es: "+code)
    return _addOrUpdateDiscount(params)


def updateDiscount(articleId, params):
    
    # params["_id"] = discountId

    discounts = schema.newDiscount()

    print('TCL: params["article_id"]', params["article_id"])
    isNew = False
    discounts = getDiscount(params["article_id"])
    print('TCL: discounts', discounts);

    
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

    return discounts
