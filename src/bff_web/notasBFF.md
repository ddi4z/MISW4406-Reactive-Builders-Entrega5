# Guía de Levantamiento de Aplicaciones

Este documento explica cómo levantar los servicios del proyecto **AlpesPartners** con Docker Compose y cómo funciona el **Backend For Frontend (BFF)** en relación al microservicio de **Asociaciones Estratégicas**.

---

## 🚀 1. Levantar Docker Compose con Microservicio de Asociaciones y BFF

Este comando levanta el microservicio **Asociaciones Estratégicas**, junto con su infraestructura de **Pulsar** y el servicio **BFF**.

```bash
docker compose --profile asociaciones_estrategicas --profile pulsar --profile bff up --force-recreate --build
```

---

## 🗄️ 2. Levantar Base de Datos Asociaciones

Si necesitas levantar únicamente la base de datos MySQL del microservicio de **Asociaciones Estratégicas**, puedes usar:

```bash
docker-compose --profile db_asociaciones_estrategicas up
```

---

## 📌 3. Funcionalidad del BFF

El microservicio de **Asociaciones Estratégicas** expone **5 endpoints REST principales**:

1. `POST /asociaciones` → Crear Asociación  
2. `GET /asociaciones/{id}` → Obtener Asociación por ID  
3. `GET /asociaciones/marca/{id_marca}` → Obtener Asociaciones por Marca  
4. `GET /asociaciones` (con filtros) → Listar Asociaciones  
5. `GET /asociaciones/analitica` → Obtener Analítica de Asociaciones  

### 🎯 Rol del BFF
El **BFF** actúa como una capa intermedia entre la **UI** y el **microservicio de Asociaciones**.  
De los 5 endpoints disponibles, el **BFF** implementa y expone únicamente **2 funcionalidades clave**:

- **Registro de Asociación**:  
   Utiliza el endpoint `POST /asociaciones` del microservicio, pero lo expone a la UI como una **mutación GraphQL** (`crearAsociacion`).

- **Consulta de Asociaciones por Marca**:  
   Utiliza el endpoint `GET /asociaciones/marca/{id_marca}`, pero lo expone a la UI como una **query GraphQL** (`asociacionesPorMarca`).

Una vez levantado el BFF (expuesto en `http://localhost:8003/v1`), se puede interactuar con el servicio mediante consultas y mutaciones GraphQL.

### 馃敼 Mutation: Crear Asociaci贸n
```graphql
mutation {
  crearAsociacion(
    input: {
      idMarca: "111e4567-e89b-12d3-a456-426614174100"
      idSocio: "222e4567-e89b-12d3-a456-426614174100"
      tipo: "campania"
      descripcion: "Alianza principal para afiliados"
      vigencia: {
        fechaInicio: "2023-09-01T00:00:00"
        fechaFin: "2025-12-31T23:59:59"
      }
    }
  ) {
    codigo
    mensaje
  }
}
```

### 馃敼 Query: Consultar Asociaciones por Marca
```graphql
query {
  asociacionesPorMarca(idMarca: "111e4567-e89b-12d3-a456-426614174100") {
    id
    idMarca
    idSocio
    tipo
    descripcion
    vigencia { 
      fechaInicio 
      fechaFin 
    }
    fechaCreacion
    fechaActualizacion
  }
}
```

De esta forma, el BFF **simplifica** y **adapta** la comunicación de la UI con el backend, reduciendo la complejidad de llamadas REST y entregando solo la información que necesita el frontend.

---

## ✅ Conclusión

- El levantamiento completo de las aplicaciones se logra con el comando que combina perfiles (`asociaciones_estrategicas`, `pulsar` y `bff`).  
- El BFF no expone todos los endpoints del microservicio, sino que selecciona los más relevantes para la experiencia de usuario: **registro** y **consulta por marca**.  
- Esto permite tener una arquitectura más limpia y enfocada en las necesidades del **frontend**.
