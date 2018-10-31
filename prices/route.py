import utils.json_serializer as json
import utils.errors as errors
import utils.security as security
import flask
import prices.crud_service as crud
import prices.rest_validations as restValidator


def init(app):
    """
    Iniciamos las rutas para los descuentos
    """
    @app.route('/v1/prices', methods=['POST'])
    def addArticle():
        print("Petición para agregar precio")
        try:

            token = flask.request.headers.get("Authorization")

            params = json.body_to_dic(flask.request.data)

            # print(params)

            for price in params:

                # print("price", price)
                pri = restValidator.validateAddPriceParams(price)
                # print("pri",pri)
                result = crud.addPrice(pri)

            

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
