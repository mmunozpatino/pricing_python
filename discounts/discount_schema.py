# coding=utf_8

import numbers
import datetime
import utils.schema_validator as validator
import utils.errors as errors

# Validaciones generales del esquema, se valida solo lo que el usuario puede cambiar
DISCOUNT_DB_SCHEMA = {
    "article_id": {
        "required": True,
        "type": str,
        "minLen": 1,
        "maxLen": 60
        },
    "fechaDesde": {
        "required": True,
        "type": str,
        "maxLen": 2048
        },
    "discount_percentage": {
        "required": True,
        "type": numbers.Real,
        "min": 0
        },
    "discount_amount": {
        "required": True,
        "type": numbers.Real,
        "min": 0
        }
}


def newDiscount():
    """
    Crea un nuevo articulo en blanco.\n
    return dict<propiedad, valor> Articulo
    """

    return {
        "article_id": "",
        "fechaDesde": "",
        "discount_percentage": 0,
        "discount_amount": 0,
        "updated": datetime.datetime.utcnow(),
        "created": datetime.datetime.utcnow(),
        "enabled": True
    }


def validateSchema(document):
    err = validator.validateSchema(DISCOUNT_DB_SCHEMA, document)

    if (len(err) > 0):
        raise errors.MultipleArgumentException(err)
