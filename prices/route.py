import utils.json_serializer as json
import utils.errors as errors
import utils.security as security
import flask
import prices.crud_service as crud
import prices.rest_validations as restValidator
import datetime


def init(app):
    """
    Iniciamos las rutas para los precios
    """
    @app.route('/v1/prices', methods=['POST'])
    def addPrice():
        print("Petición para agregar precio")
        try:

            token = flask.request.headers.get("Authorization")

            security.isValidToken(token)

            params = json.body_to_dic(flask.request.data)

            # print(params)

            for price in params:

                # print("price", price)
                pri = restValidator.validateAddPriceParams(price)
                # print("pri",pri)
                result = crud.addPrice(pri)

            return "Hola para el post con el token: "+token
        except Exception as err:
            return errors.handleError(err)

    @app.route('/v1/prices/<articleId>', methods=['POST'])
    def updatePrice(articleId):
        try:

            token = flask.request.headers.get("Authorization")

            security.isValidToken(token)

            # print("now "+ datetime.datetime.utcnow())

            print("articleID "+articleId)

            params = json.body_to_dic(flask.request.data)

            params = restValidator.validateEditPriceParams(articleId, params)

            result = crud.updatePrice(articleId, params)

            return json.dic_to_json(result)
        except Exception as err:
            print("error")
            return errors.handleError(err)

    
    @app.route('/v1/prices/<articleId>', methods=['GET'])
    def getPrice(articleId):
        print("ejecuta")
        try:
            
            return json.dic_to_json(crud.getPrice(articleId))
        except Exception as err:
            return errors.handleError(err)

    @app.route('/v1/price/<articleId>', methods=['GET'])
    def getPriceByDate(articleId):
        print("ejecuta")
        try:
            priceDate = flask.request.args.get('fecha')
            # print("llego ", priceDate)
            return json.dic_to_json(crud.getPriceByDate(articleId,priceDate))
            # return "funciono"

        except Exception as err:
            return errors.handleError(err)
