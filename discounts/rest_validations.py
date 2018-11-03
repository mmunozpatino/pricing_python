# coding=utf_8
# Son las validaciones de los servicios rest, se validan los parametros obtenidos desde las llamadas externas rest

import utils.errors as error
import prices.crud_service as crud
import utils.schema_validator as schemaValidator
import numbers


# Son validaciones sobre las propiedades que pueden actualizarse desde REST
DISCOUNT_UPDATE_SCHEMA = {
    "article_id": {
        "type": str,
        "minLen": 1,
        "maxLen": 60
        },
    "discount_percentage": {
        "type": numbers.Real,
        "min":0
        },
    "discount_amount": {
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

    return schemaValidator.validateAndClean(DISCOUNT_UPDATE_SCHEMA, params)


def validateEditDiscountParams(discountCode, params):
    if (not discountCode):
        raise error.InvalidArgument("_id", "Inválido")

    return schemaValidator.validateAndClean(DISCOUNT_UPDATE_SCHEMA, params)


def validatePriceExist(articleId):
    article = crud.getPrice(articleId)
    if("enabled" not in article or not article["enabled"]):
        raise error.InvalidArgument("_id", "Inválido")
