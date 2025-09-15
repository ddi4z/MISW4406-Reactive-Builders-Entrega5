# Microservicio de Pagos

## Pasos de ejecución

### Inicializar el proyecto

**1.** Crear el entorno virtual

```bash
python -m venv venv

# Si el launcher es py en vez de python
py -m venv venv
```

**2.** Activar el entorno virtual

- En **Linux / macOS**:

```bash
source venv/bin/activate
```

- En **Windows PowerShell**:

```powershell
venv\Scripts\Activate.ps1
```

- En **Windows CMD**:

```cmd
venv\Scripts\activate.bat
```

**3.** Instalar las dependencias

```bash
pip install -r pagos-requirements.txt
```

### Crear base de datos Postgres

1. Se crea la base de datos con Docker Compose

```bash
docker-compose --profile db up
```

2. Puede conectarse a la base de datos con los siguientes parámetros:

**Host:** 127.0.0.1 (localhost)

**Port:** 5433

**Database:** alpespartners

**Username:** admin

**Password:** admin

Para esto, puede usar extensiones de VS Code como Database Client, que también permiten visualizar las tablas.

### Ejecutar Aplicación

Desde el directorio `src` ejecute el siguiente comando

```bash
uvicorn pagos.main:app --host localhost --port 8001 --reload
```
