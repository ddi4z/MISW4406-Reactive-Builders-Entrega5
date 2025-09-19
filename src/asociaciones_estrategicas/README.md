# 🏗️ Microservicio de Asociaciones Estratégicas

## 👥 Integrantes - Reactive Builders

| Nombre | Correo |
| :--- | :--- |
| Orlando Giovanny Solarte Delgado | o.solarte@uniandes.edu.co |
| Martín Flores Arango | r.floresa@uniandes.edu.co |
| Sara Sofía Cárdenas Rodríguez | ss.cardenas@uniandes.edu.co |
| Daniel Felipe Díaz Moreno | d.diazm@uniandes.edu.co |

---

## 🚀 Ejecución del microservicio

### 1. Levantar con Docker Compose

**Microservicio + Pulsar**
```bash
docker compose --profile asociaciones_estrategicas --profile pulsar up --force-recreate --build
```

**Base de datos**
```bash
docker-compose --profile db_asociaciones_estrategicas up
```

**Broker de eventos**
```bash
docker-compose --profile pulsar up
```

**Aplicación Flask**
```bash
flask --app src/asociaciones_estrategicas/api --debug run --host=0.0.0.0 --port=5000
```

📌 **Nota:** Como se usa **Event Sourcing**, se configuró Pulsar con **retención infinita (-1)** en los tópicos para permitir el *replay* de eventos y reconstrucción de proyecciones:
```bash
./bin/pulsar-admin namespaces set-retention public/default --size -1 --time -1
```

---

## 🗂️ Modelo de dominio

El microservicio gestiona la creación, cancelación y finalización de **asociaciones estratégicas** entre marcas y socios.  

Tipos de asociación disponibles (`TipoAsociacion`):  
- `PROGRAMA_AFILIADOS`  
- `COLABORACION_DIRECTA`  
- `CAMPANIA`  
- `PROGRAMA_LEALTAD`  
- `ALIANZA_B2B`  

Cada asociación estratégica se representa como una **agregación raíz** en el dominio.

---

## 📡 Comunicación basada en eventos

Este microservicio sigue un patrón **Event-Driven Architecture (EDA)** usando **Apache Pulsar** como broker.  
Los mensajes usan **Avro** como esquema y se dividen en **eventos** y **comandos**.

### 🔔 Eventos de integración

**Tópico:** `public/default/eventos-asociacion`

- **EventoAsociacionCreada**
```python
class AsociacionCreadaPayload(Record):
    id_asociacion = String()
    id_marca = String()
    id_socio = String()
    tipo = String()
    descripcion = String()
    fecha_inicio = Long()
    fecha_fin = Long()
    fecha_creacion = Long()
```

- **EventoAsociacionFinalizada**
```python
class AsociacionFinalizadaPayload(Record):
    id_asociacion = String()
    fecha_actualizacion = Long()
```

---

### 📩 Comandos

1. **Crear asociación estratégica**  
   - **Tópico:** `comandos-asociaciones.crear_asociacion`  
   - **Payload:**
```python
class ComandoCrearAsociacionEstrategicaPayload(ComandoIntegracion):
    id_usuario = String()
    id_marca = String()
    id_socio = String()
    tipo = String()
    descripcion = String()
    fecha_inicio = String()
    fecha_fin = String()
```

2. **Iniciar tracking**  
   - **Tópico:** `comandos-eventos_y_atribucion.iniciar_tracking`  
   - **Payload:**
```python
class ComandoIniciarTrackingPayload(Record):
    id_asociacion_estrategica = String()
    id_marca = String()
    id_socio = String()
    tipo = String()
```

---

## 📜 Comandos y Eventos de la Saga

La saga de asociaciones estratégicas coordina la creación y cancelación de asociaciones, garantizando consistencia mediante eventos de compensación.

### 📩 Comandos de la saga

1. **Cancelar asociación estratégica**  
   - **Tópico:** `comandos-asociaciones.cancelar_asociacion`  
   - **Payload:**
   ```python
   class ComandoCancelarAsociacionEstrategicaPayload(ComandoIntegracion):
       id_correlacion = String()
       id_asociacion = String()
       motivo = String()
   ```

---

### 🔔 Eventos de la saga

1. **OnboardingIniciado**  
   - Se emite al crear una nueva asociación.  
   - **Payload:**
   ```python
   class OnboardingIniciadoPayload(Record):
       id_asociacion = String()
       id_marca = String()
       id_socio = String()
       tipo = String()
       descripcion = String()
       fecha_inicio = Long()
       fecha_fin = Long()
       fecha_creacion = Long()
   ```

2. **OnboardingCancelado**  
   - Se emite al cancelar una asociación ya creada.  
   - **Payload:**
   ```python
   class OnboardingCanceladoPayload(Record):
       id_asociacion = String()
       id_correlacion = String()
       motivo = String()
       fecha_cancelacion = Long()
   ```

3. **OnboardingFallido**  
   - Se emite si ocurre un error en la creación o validación de la asociación.  
   - **Payload:**
   ```python
   class OnboardingFallidoPayload(Record):
       id_asociacion = String()
       id_correlacion = String()
       motivo = String()
       fecha_evento = Long()
   ```

---

## 👂 Consumir mensajes manualmente

Se pueden escuchar los tópicos directamente en el contenedor de Pulsar:

```bash
docker exec -it broker bash

./bin/pulsar-client consume -s "sub-datos" public/default/eventos-asociacion -n 0
./bin/pulsar-client consume -s "sub-datos" comandos-eventos_y_atribucion.iniciar_tracking -n 0
./bin/pulsar-client consume -s "sub-datos" comandos-asociaciones.crear_asociacion -n 0
./bin/pulsar-client consume -s "sub-datos" comandos-asociaciones.cancelar_asociacion -n 0
```

---

## 🧩 Decisiones de diseño

- **CQRS + Event Sourcing**:  
  Escrituras manejadas por comandos → generan eventos → aplicados en proyecciones.  
  Lecturas van directo a proyecciones materializadas (listas y analíticas).  

- **Unidad de Trabajo (UoW híbrida)**:  
  Coordina en una sola transacción lógica la persistencia en BD y la publicación de eventos en el broker.  
  Asegura consistencia y evita inconsistencias.  

- **Eventos gordos de integración**:  
  Los eventos incluyen toda la información relevante, evitando dependencias adicionales entre microservicios.  

- **Persistencia de eventos en Pulsar**:  
  Configuración de retención infinita permite reprocesar eventos y reconstruir proyecciones.  

- **Autonomía de microservicios**:  
  Cada servicio mantiene su propia BD y proyecciones → resiliencia ante fallos.  

- **Evolución de esquemas (Avro)**:  
  Los mensajes están versionados y validados en tiempo de ejecución.  

- **Escalabilidad y resiliencia en el consumo**:  
  Uso de suscripción `Shared` en Pulsar permite que múltiples instancias procesen mensajes en paralelo.  

- **Consistencia eventual en proyecciones**:  
  Las proyecciones (analítica y lista) se actualizan de manera asíncrona, lo que garantiza resiliencia aunque pueda haber ligeros retrasos.

---

## 🛠️ Endpoints principales

- **Crear asociación estratégica**  
  `POST /asociaciones`  

- **Cancelar asociación estratégica**  
  `POST /asociaciones/cancelar`  

- **Obtener asociación por id**  
  `GET /asociaciones/<id>`  

- **Listar asociaciones con filtros**  
  `GET /asociaciones/lista?id_marca=...&id_socio=...&tipo=...`  

- **Analítica de asociaciones (proyección)**  
  `GET /asociaciones/analitica`  

---

## 📽️ Demo

Se incluyó un video de ejecución en el repositorio (`videoFinalMicroAsociaciones.mp4`).

---
