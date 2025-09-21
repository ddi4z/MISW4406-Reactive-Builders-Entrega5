# 🏗️ Microservicio de eventos

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
docker compose --profile eventos --profile pulsar --profile db_eventos up --force-recreate --build
```

**Base de datos**
```bash
docker compose --profile db_eventos up -d
```

**Broker de eventos**
```bash
docker compose --profile pulsar up -d
```

**Aplicación Flask**
```bash
flask --app src/eventos/api --debug run --host=0.0.0.0 --port=5000
```

📌 **Nota:** Como se usa **Event Sourcing**, se configuró Pulsar con **retención infinita (-1)** en los tópicos para permitir el *replay* de eventos y reconstrucción de proyecciones:
```bash
./bin/pulsar-admin namespaces set-retention public/default --size -1 --time -1
```

---
