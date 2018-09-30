# PRINCING MICROSERVICE

## Objetivo

## Servicios ofercidos

- [Precios](#precios)
  

## Consultas GET

### /v1/price/:article_i
Response: 
```   
    {
        id: String,
        fechaDesde: Date,
        fechaHasta: Date,
        price: double,
        article_id: String
    }
```
### /v1/price/:article_id&:fecha
response:    
```
    {
        id: String,
        fechaDesde: Date,
        fechaHasta: Date,
        price: float,
        article_id: String,
        discount: float
    }
```
### /v1/discount/:article_id
response:
```
    [{
        id: String,
        fechaDesde: Date,
        fechaHasta: Date,
        detalle: String
    }]
```
### /v1/discount/:article_id&:fecha
response:
```
    [{
        id: String,
        fechaDesde: Date,
        fechaHasta: Date,
        detalle: String
    }]
```
## Consultas POST



### /v1/price
```
request:
    [{
        article_id: String,
        price: float,
        fechaDesde: Date,
        fechaHasta: Date
    }]
```
response:
```
    {
        id: [String],
        message: "Registro creado con éxito"
    }
```
### /v1/discount/
request:
```
    [{
        article_id: String,
        price: float,
        fechaDesde: Date,
        fechaHasta: Date
    }]
```
response:
```
    {
        id: String,
        message: "Registro creado con éxito"
    }
```
