# PRINCING MICROSERVICE

## Tabla de contenidos
- [PRINCING MICROSERVICE](#princing-microservice)
    - [Tabla de contenidos](#tabla-de-contenidos)
    - [Auth](#auth)
    - [Objetivos](#objetivos)
    - [Microservicios utilizados](#microservicios-utilizados)
    - [Recursos del microservicio](#recursos-del-microservicio)
    - [Servicios ofrecidos](#servicios-ofrecidos)
    - [Glosario](#glosario)
    - [Precios](#precios)
        - [Crear Precio](#crear-precio)
        - [Buscar Precio](#buscar-precio)
        - [Buscar Precio por Fecha](#buscar-precio-por-fecha)
        - [Actualizar Precio](#actualizar-precio)
    - [Descuentos](#descuentos)
        - [Crear Descuento](#crear-descuento)
        - [Buscar Descuento por artículo](#buscar-descuento-por-art%C3%ADculo)
        - [Buscar Descuento por código](#buscar-descuento-por-c%C3%B3digo)
        - [Buscar Descuento Fecha](#buscar-descuento-fecha)
        - [Actualizar Precio](#actualizar-precio)
    - [Rabbit](#rabbit)
        - [Rabbit GET](#rabbit-get)
            - [Validación de artículos](#validaci%C3%B3n-de-art%C3%ADculos)
            - [Logout](#logout)
        - [Rabbit POST](#rabbit-post)

## Auth

El servicio de pricing permite al usuario **autenticado** consultar **precios** y **descuentos**, para poder modificar un  precio/descuento dicho usuario necesita ser "admin" para poder hacerlo.

## Objetivos

Este microservicio tiene como objetivo permitir la administación de los precios de los distintos artículos del negocio, tanto precios o descuentos actuales o futuros, manejando fecha de validez de cada precio/precio.

## Microservicios utilizados

    -Auth
    -Catalog

## Recursos del microservicio
    - Precios
    - Descuentos
  
## Servicios ofrecidos

    -Agregar un precio o descuento
    -Consultar el/los precios de uno o varios artículos
    -Modificar un precio/descuento
    -Eliminar un precio o descuento

## Glosario

-**Precio** : Valor del costo de un atículo, se representa con un double y tiene fechas entre las cuáles dicho precio es válido.  

-**Descuento** : Valor que tiene de promoción un artículo, al igual que el precio, posee fechas entre las cuáles dicho descuento es válido.

## Precios
### Crear Precio
    Ruta que permite crear uno y varios precios nuevos. Nota: se pueden crear varios precios en una misma llamada

**URL:**  
    /v1/price

**Method:**  
    POST  

**Request header:**  
```Authorization=bearer {token}```  

**Request body:**
```
    [{
        article_id: String,
        price: double,
        fechaDesde: Date
    }]
```
**Response body:**
```
    [{
        article_id: String,
        message: "Registro creado con éxito"
    }]
```

**Reponse status:**  

**200 OK**

```
HTTP/1.1 200 OK
```
**401 Unauthorized**

```
HTTP/1.1 401 Unauthorized
```

**400 Bad Request**

```
HTTP/1.1 400 Bad Request
[{
    article_id: String,
    "error" : "{Motivo del error}"
}]
```


**500 Server Error**

```
HTTP/1.1 500 Server Error
{
    "error" : "{Motivo del error}"
}
```

### Buscar Precio
    Ruta que permite obtener un precio a partir del id del artículo deseado. Nota, se devuelve por defecto el precio vigente a la fecha. En caso de consultar un un código de descuento, se devolverá el precio con el descuento incluído.

**URL:**  
 /v1/price/:article_id?discount=discount_code 

**Method:**   
GET  

**Parámetros:**   
    - *article_id:* id del artículo deseado
  
**Response Body:** 
```   
    {
        fechaDesde: Date,
        price: double,
        article_id: String
    }
```

**Reponse status:**
**200 OK**

```
HTTP/1.1 200 OK
```  

**401 Unauthorized**

```
HTTP/1.1 401 Unauthorized
```

**400 Bad Request**

```
HTTP/1.1 400 Bad Request
{
    "error" : "{Motivo del error}"
}
```


**500 Server Error**

```
HTTP/1.1 500 Server Error
{
    "error" : "{Motivo del error}"
}
```

### Buscar Precio por Fecha
    Ruta que permite buscar el precio de un artículo para una fecha determinada

**URL:**  
/v1/price/:article_id?fecha=:fecha  

**Method:**  
GET  

**Parámetros:**  
    - *article_id:* id del artículo deseado  
    - *fecha:* fecha del precio  

**Response Body:**  
```   
    {
        fechaDesde: Date,
        price: double,
        article_id: String
    }
```
**Reponse status:**
**200 OK**

```
HTTP/1.1 200 OK
```  

**401 Unauthorized**

```
HTTP/1.1 401 Unauthorized
```

**400 Bad Request**

```
HTTP/1.1 400 Bad Request
{
    "error" : "{Motivo del error}"
}
```


**500 Server Error**

```
HTTP/1.1 500 Server Error
{
    "error" : "{Motivo del error}"
}
```

### Actualizar Precio
    Ruta que permite modificar un precio existente a partir del id del artículo correpondiente. Nota, sólo se modificará el precio vigente a la fecha

**URL:**  
/v1/price/:article_id

**Method:**  
POST  

**Parámetros:**  
    -*article_id:* id del articulo relacionado al precio existente a modificar  

**Request Body:**

```
    {
        article_id: String,
        price: double,
        fechaDesde: Date,    
    }
```

**Response Body:**

```
    {
        article_id: String,
        message: "Precio actualizado con éxito"
    }
```
**Reponse status:**
**200 OK**

```
HTTP/1.1 200 OK
```  

**401 Unauthorized**

```
HTTP/1.1 401 Unauthorized
```

**400 Bad Request**

```
HTTP/1.1 400 Bad Request
{
    "error" : "{Motivo del error}"
}
```


**500 Server Error**

```
HTTP/1.1 500 Server Error
{
    "error" : "{Motivo del error}"
}
```

## Descuentos
### Crear Descuento
    Ruta que permite crear uno y varios descuentos nuevos. Cada descuento puede ser defino por un porcentaje (representado por el decimal correspondiente), o pur una cantidad fija de dinero, es obligatorio que uno de los campos esté completo para poder crear el descuento

**URL:**  
    /v1/discount

**Method:**  
    POST  

**Request body:**
```
    [{
        article_id: String,
        discount_percentage: float,
        discount_amount: double,
        fechaDesde: Date,    
    }]
```
**Response body:**
```
    [{
        article_id: String,
        discount_code: String,
        message: "Registro creado con éxito"
    }]
```

**Reponse status:**
**200 OK**

```
HTTP/1.1 200 OK
```  

**401 Unauthorized**

```
HTTP/1.1 401 Unauthorized
```

**400 Bad Request**

```
HTTP/1.1 400 Bad Request
{
    "error" : "{Motivo del error}"
}
```


**500 Server Error**

```
HTTP/1.1 500 Server Error
{
    "error" : "{Motivo del error}"
}
```

### Buscar Descuento por artículo
    Ruta que permite obtener uno o varios descuentos a partir del id del artículo relacionado

**URL:**  
 /v1/discount/:article_id  

**Method:**   
GET  

**Parámetros:**   
    - *article_id:* id del artículo relacionado al descuento deseado
  
**Response Body:** 
```   
    [{
        id: String,
        fechaDesde: Date,
        discount_code: String,
        discount_percentage: float,
        discount_amount: double,
        article_id: String
    }]
```
**Reponse status:**
**200 OK**

```
HTTP/1.1 200 OK
```  

**401 Unauthorized**

```
HTTP/1.1 401 Unauthorized
```

**400 Bad Request**

```
HTTP/1.1 400 Bad Request
{
    "error" : "{Motivo del error}"
}
```


**500 Server Error**

```
HTTP/1.1 500 Server Error
{
    "error" : "{Motivo del error}"
}
```
### Buscar Descuento por código
    Ruta que permite obtener uno o varios descuentos a partir del id del artículo relacionado

**URL:**  
 /v1/discount/:article_id  

**Method:**   
GET  

**Parámetros:**   
    - *article_id:* id del artículo deseado
  
**Response Body:** 
```   
    {
        id: String,
        fechaDesde: Date,
        discount_code: String,
        discount_percentage: float,
        discount_amount: double,
        article_id: String
    }
```
**Reponse status:**
**200 OK**

```
HTTP/1.1 200 OK
```  

**401 Unauthorized**

```
HTTP/1.1 401 Unauthorized
```

**400 Bad Request**

```
HTTP/1.1 400 Bad Request
{
    "error" : "{Motivo del error}"
}
```


**500 Server Error**

```
HTTP/1.1 500 Server Error
{
    "error" : "{Motivo del error}"
}
```

### Buscar Descuento Fecha 
    Ruta que permite buscar el descuento de un artículo para una fecha determinada

**URL:**  
/v1/discount/:article_id?fecha=:fecha  

**Method:**  
GET  

**Parámetros:**  
    - *article_id:* id del artículo deseado  
    - *fecha:* fecha del descuento  

**Response Body:**  
```   
    {
        id: String,
        fechaDesde: Date,
        discount_code: String,
        discount_percentage: float,
        discount_amount: double,
        article_id: String
    }
```
**Reponse status:**
**200 OK**

```
HTTP/1.1 200 OK
```  

**401 Unauthorized**

```
HTTP/1.1 401 Unauthorized
```

**400 Bad Request**

```
HTTP/1.1 400 Bad Request
{
    "error" : "{Motivo del error}"
}
```


**500 Server Error**

```
HTTP/1.1 500 Server Error
{
    "error" : "{Motivo del error}"
}
```

### Actualizar Precio
    Ruta que permite modificar un descuento existente a partir del correspondiente código

**URL:**  
/v1/discout/:discount_code

**Method:**  
POST  

**Parámetros:**  
    -*discount_id:* id del descuento existente a modificar  

**Request Body:**

```
    {
        article_id: String,
        discount_code: String,
        discount_percentage: float,
        discount_amount: double,
        fechaDesde: Date,    
    }
```

**Response Body:**

```
    {
        id: String,
        message: "Registro actualizado con éxito"
    }
```
**Reponse status:**
**200 OK**

```
HTTP/1.1 200 OK
```  

**401 Unauthorized**

```
HTTP/1.1 401 Unauthorized
```

**400 Bad Request**

```
HTTP/1.1 400 Bad Request
{
    "error" : "{Motivo del error}"
}
```


**500 Server Error**

```
HTTP/1.1 500 Server Error
{
    "error" : "{Motivo del error}"
}
```
## Rabbit

### Rabbit GET

#### Validación de artículos

Escucha de mensajes article-exist desde car. Valida artículos

``` DIRECT catalog/article-exist ```

```
{
  "type": "article-exist",
  "exchange" : "{Exchange name to reply}"
  "queue" : "{Queue name to reply}"
  "message" : {
      "referenceId": "{referenceId}",
      "articleId": "{articleId}",
  }
} 
```

#### Logout

Esucha de mensajes de logout desde auth. Invalida acciones si el usuario no está logueado

``` FANOUT auth/logout```

```
{
   "type": "logout",
   "message": "{tokenId}"
}
```

### Rabbit POST

Notifica el cambio del precio de un artículo

DIRECT price/price_change

```
{
    "type":"change",
    "message":{
        "article": {id of the article},
        "price": {new price for te article},
    }
}
```

Notifica el cambio del descuento de un artículo

DIRECT price/discount_change

```
{
    "type":"change",
    "message":{
        "article": {id of the article},
        "discount": {new discount for te article},
        "discount_code": {code of the discount}
    }
}
```
