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

                # print("price", price)
                dis = restValidator.validateAddPriceParams(discount)
                # print("pri",pri)
                result = crud.addDiscount(dis)

            # for price in params:

            # print("price", price)

            security.isValidToken(token)

            return "Hola para el post con el token: "+token
        except Exception as err:
            return errors.handleError(err)

        # try:
        #     # security.isValidToken()
        #     # params = json.body_to_dic(flask.request.data)

        #     # result = crud.
        #     print("hola")
        #     return True

        # except Exception as err:
        #     return False
