# PRINCING MICROSERVICE

//TODO:  
    -agregar un glosario
    -consultar si el precio existe
    -ver usuario anonimo con auth
    -agregar status response 200 y un error
## Tabla de contenidos
- [PRINCING MICROSERVICE](#princing-microservice)
    - [Tabla de contenidos](#tabla-de-contenidos)
    - [Auth](#auth)
    - [Objetivos](#objetivos)
    - [Microservicios utilizados](#microservicios-utilizados)
    - [Recursos del microservicio](#recursos-del-microservicio)
    - [Servicios ofercidos](#servicios-ofercidos)
    - [Precios](#precios)
        - [Crear Precio](#crear-precio)
        - [Buscar Precio](#buscar-precio)
        - [Buscar Precio por Fecha](#buscar-precio-por-fecha)
        - [Actualizar Precio](#actualizar-precio)
        - [Eliminar Precio](#eliminar-precio)
    - [Descuentos](#descuentos)
        - [Crear Descuento](#crear-descuento)
        - [Buscar Descuento](#buscar-descuento)
        - [Buscar Descuento Fecha](#buscar-descuento-fecha)
        - [Actualizar Precio](#actualizar-precio)
        - [Eliminar Precio](#eliminar-precio)

## Auth

El servicio de pricing tiene funciones habilitadas por más de que el usuario no se encuentre autenticado, por ejemplo para consultar un precio el usuario no necesita estar autenticado, para poder ver descuentos si necesita estar autenticado, para modificar un  precio/descuento dicho usuario necesita ser "admin" para poder hacerlo

## Objetivos

Este microservicio tiene como objetivo permitir la administación de los precios de los distintos artículos del negocio, tanto precios o descuentos actuales o futuros, manejando fecha de validez de cada precio/precio.

## Microservicios utilizados

    -Auth

## Recursos del microservicio
    - Precios
    - Descuentos
  
## Servicios ofercidos

    -Agregar un precio o descuento
    -Consultar el/los precios de uno o varios artículos
    -Modificar un precio/descuento
    -Eliminar un precio o descuento

## Precios
### Crear Precio
    Ruta que permite crear uno y varios precios nuevos

**URL:**  
    /v1/price

**Method:**  
    POST  

**Request body:**
```
    [{
        article_id: String,
        price: double,
        fechaDesde: Date,
        fechaHasta: Date
    }]
```
**Response body:**
```
    [{
        id: String,
        message: "Registro creado con éxito"
    }]
```
### Buscar Precio
    Ruta que permite obtener un precio a partir de su correspondiente id

**URL:**  
 /v1/price/:article_id  

**Method:**   
GET  

**Parámetros:**   
    - *article_id:* id del artículo deseado
  
**Response Body:** 
```   
    {
        id: String,
        fechaDesde: Date,
        fechaHasta: Date,
        price: double,
        article_id: String
    }
```
### Buscar Precio por Fecha
    Ruta que permite buscar el precio de un artículo para una fecha determinadad

**URL:**  
/v1/price/:article_id&:fecha  

**Method:**  
GET  

**Parámetros:**  
    - *article_id:* id del artículo deseado  
    - *fecha:* fecha del precio  

**Response Body:**  
```   
    {
        id: String,
        fechaDesde: Date,
        fechaHasta: Date,
        price: double,
        article_id: String
    }
```

### Actualizar Precio
    Ruta que permite modificar un precio existente a partir del correspondiente id

**URL:**  
/v1/price/:price_id

**Method:**  
POST  

**Parámetros:**  
    -*price_id:* id del precio existente a modificar  

**Request Body:**

```
    {
        article_id: String,
        price: double,
        fechaDesde: Date,
        fechaHasta: Date
    }
```

**Response Body:**

```
    {
        id: String,
        message: "Registro actualizado con éxito"
    }
```

### Eliminar Precio
    Ruta que permite eliminar un precio actual de la base de datos

**URL:**  
/v1/price/:price_id  

**Method:**  
DELETE  

**Parámetros:**  
    -*price_id:* id del precio a eliminar de la base de datos

**Response Body:**
```
    {
        id: String,
        message: "Registro eliminado con éxito"
    }
```


## Descuentos
### Crear Descuento
    Ruta que permite crear uno y varios descuentos nuevos

**URL:**  
    /v1/discount

**Method:**  
    POST  

**Request body:**
```
    [{
        article_id: String,
        discount: float,
        fechaDesde: Date,
        fechaHasta: Date
    }]
```
**Response body:**
```
    [{
        id: String,
        message: "Registro creado con éxito"
    }]
```
### Buscar Descuento
    Ruta que permite obtener uno o varios descuentos a partir del id del artículo relacionado

**URL:**  
 /v1/discount/:article_id  

**Method:**   
GET  

**Parámetros:**   
    - *article_id:* id del artículo deseado
  
**Response Body:** 
```   
    [{
        id: String,
        fechaDesde: Date,
        fechaHasta: Date,
        discount: float,
        article_id: String
    }]
```

### Buscar Descuento Fecha 
    Ruta que permite buscar el descuento de un artículo para una fecha determinadad

**URL:**  
/v1/price/:article_id&:fecha  

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
        fechaHasta: Date,
        discount: float,
        article_id: String
    }
```

### Actualizar Precio
    Ruta que permite modificar un descuento existente a partir del correspondiente id

**URL:**  
/v1/discout/:discount_id

**Method:**  
POST  

**Parámetros:**  
    -*discount_id:* id del descuento existente a modificar  

**Request Body:**

```
    {
        article_id: String,
        discount: float,
        fechaDesde: Date,
        fechaHasta: Date
    }
```

**Response Body:**

```
    {
        id: String,
        message: "Registro actualizado con éxito"
    }
```

### Eliminar Precio
    Ruta que permite eliminar un descuento actual de la base de datos

**URL:**  
/v1/discount/:discount_id  

**Method:**  
DELETE  

**Parámetros:**  
    -*discount_id:* id del descuento a eliminar de la base de datos

**Response Body:**
```
    {
        id: String,
        message: "Registro eliminado con éxito"
    }
```

