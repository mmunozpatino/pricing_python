import utils.json_serializer as json
import utils.errors as errors
import utils.security as security
import flask
import discounts.crud_service as crud
import discounts.rest_validations as restValidator


def init(app):
    """
    Iniciamos las rutas para los precios
    """
    @app.route('/v1/discount', methods=['POST'])
    def addDiscount():
        print("Petición para agregar descuento")
        try:
            security.validateAdminRole(flask.request.headers.get("Authorization"))

            token = flask.request.headers.get("Authorization")

            params = json.body_to_dic(flask.request.data)
            
            responses = []

            for discount in params:

                dis = restValidator.validateAddPriceParams(discount)
                result = crud.addDiscount(dis)
                responses.append(result.copy())


            # return "Hola para el post con el token: "+token
            return json.dic_to_json(responses)

        except Exception as err:
            return errors.handleError(err)

    @app.route('/v1/discounts/<discountCode>', methods=['POST'])
    def updateDiscount(discountCode):
        try:
            security.validateAdminRole(flask.request.headers.get("Authorization"))

            token = flask.request.headers.get("Authorization")


            # print("now "+ datetime.datetime.utcnow())

            print("articleID "+discountCode)

            params = json.body_to_dic(flask.request.data)

            params = restValidator.validateEditDiscountParams(discountCode, params)

            result = crud.updateDiscount(discountCode, params)

            return json.dic_to_json(result)
        except Exception as err:
            print("error")
            return errors.handleError(err)
    
    @app.route('/v1/discounts/<discountCode>', methods=['GET'])
    def getDiscount(discountCode):
        try:
            print("articleID "+discountCode)

            return json.dic_to_json(crud.getDiscount(discountCode))
        except Exception as err:
            return errors.handleError(err)

    @app.route('/v1/discounts/article=<articleId>', methods=['GET'])
    def getDiscountByArticle(articleId):
        try:
            return json.dic_to_json(crud.getDiscountByArticle(articleId))
        except Exception as err:
            return errors.handleError(err)

    
    @app.route('/v1/discount/<articleId>', methods=['GET'])
    def getDiscountByDate(articleId):
        print("ejecuta")
        try:
            discountDate = flask.request.args.get('fecha')
            # print("llego ", discountDate)
            return json.dic_to_json(crud.getDiscountByDate(articleId,discountDate))
            # return "funciono"

        except Exception as err:
            return errors.handleError(err)