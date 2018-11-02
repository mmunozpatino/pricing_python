# coding=utf_8
# Son las validaciones de los servicios rest, se validan los parametros obtenidos desde las llamadas externas rest

import utils.errors as error
import prices.crud_service as crud
import utils.schema_validator as schemaValidator
import numbers


# Son validaciones sobre las propiedades que pueden actualizarse desde REST
PRICE_UPDATE_SCHEMA = {
    "article_id": {
        "type": str,
        "minLen": 1,
        "maxLen": 60
        },
    "price": {
        "type": numbers.Real,
        "min":0
        },
    "fechaDesde": {
        "required": True,
        "type": str,
        "maxLen": 2048
        },
}


def validateAddPriceParams(params):
    """
    Valida los parametros para crear un objeto.\n
    params: dict<propiedad, valor> Price
    """
    if ("_id" in params):
        raise error.InvalidArgument("_id", "Inválido")

    return schemaValidator.validateAndClean(PRICE_UPDATE_SCHEMA, params)


def validateEditPriceParams(priceId, params):
    """
    Valida los parametros para actualizar un objeto.\n
    params: dict<propiedad, valor> Article
    """
    if (not priceId):
        raise error.InvalidArgument("_id", "Inválido")

    return schemaValidator.validateAndClean(PRICE_UPDATE_SCHEMA, params)


def validatePriceExist(priceId):
    article = crud.getPrice(priceId)
    if("enabled" not in article or not article["enabled"]):
        raise error.InvalidArgument("_id", "Inválido")
