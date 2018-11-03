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

            token = flask.request.headers.get("Authorization")

            params = json.body_to_dic(flask.request.data)
            
            for discount in params:

                dis = restValidator.validateAddPriceParams(discount)
                result = crud.addDiscount(dis)


            security.isValidToken(token)

            return "Hola para el post con el token: "+token
        except Exception as err:
            return errors.handleError(err)

    @app.route('/v1/discounts/<discountCode>', methods=['POST'])
    def updateDiscount(discountCode):
        try:

            token = flask.request.headers.get("Authorization")

            security.isValidToken(token)

            # print("now "+ datetime.datetime.utcnow())

            print("articleID "+discountCode)

            params = json.body_to_dic(flask.request.data)

            params = restValidator.validateEditDiscountParams(discountCode, params)

            result = crud.updateDiscount(discountCode, params)

            return json.dic_to_json(result)
        except Exception as err:
            print("error")
            return errors.handleError(err)

