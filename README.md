# Taller Docker Compose - Basado en el parcial del segundo corte

Este documento explica cómo ejecutar el proyecto, ejecutar pruebas, usar Docker y Docker Compose

## 1. Qué contiene este proyecto

- `src/api.py`: FastAPI con los siguientes endpoints:
  - `GET /health` - verifica que el servicio está vivo.
  - `GET /recarga` - calcula el bono de una recarga según monto y si es premium.
  - `POST /recarga` - hace lo mismo usando payload JSON.
  - `POST /recargas` - crea un registro de recarga en la base de datos.
  - `GET /recargas` - lista las recargas almacenadas.
- `src/db.py`: configuración de SQLAlchemy.
- `src/models.py`: modelo `RecargaRecord` para persistencia.
- `src/recarga.py`: lógica de negocio de cálculo de bonos.
- `Dockerfile`: construye la imagen de la aplicación.
- `docker-compose.yml`: levanta la app y PostgreSQL.
- `requirements.txt`: dependencias Python.
- `test/test_api.py`: pruebas unitarias para endpoints y persistencia.

## 2. Preparar el entorno local

1. Abrir terminal en `d:\Parcial-2corte-Pruebas`.
2. Instalar dependencias:

```powershell
python -m pip install -r requirements.txt
```

## 3. Ejecutar pruebas localmente

```powershell
python -m pytest -q
```

Si todas las pruebas pasan, el proyecto está correcto.

## 4. Construir la imagen Docker

```powershell
docker build -t mi-app:v1 .
```

Verificar que la imagen exista:

```powershell
docker images
```

## 5. Levantar los servicios con Docker Compose

```powershell
docker compose up -d
```

Esto levanta:
- `db`: PostgreSQL 16 con volumen persistente.
- `app`: la aplicación FastAPI construida desde `Dockerfile`.

## 6. Verificar que ambos servicios estén corriendo

```powershell
docker compose ps
```

Debe aparecer `recargaya_db` y `recargaya_app` con estado `running`.

## 7. Probar que la aplicación responde

¿

en PowerShell:

```powershell
Invoke-WebRequest http://localhost:8000/health | Select-Object -ExpandProperty Content
```

También puedes probar el endpoint de recarga:

```powershell
curl "http://localhost:8000/recarga?monto=10000&es_premium=false"
```

## 8. Ejecutar pruebas dentro del contenedor de la aplicación

```powershell
docker compose exec app python -m pytest -q
```

## 9. Ejecutar pruebas usando un contenedor temporal

```powershell
docker compose run --rm app python -m pytest -q
```

## 10. Modificar la aplicación y reconstruir solo el servicio de app

Si agregas un endpoint o cambias la aplicación, usa:

```powershell
docker compose up -d --build app
```

## 11. Notas importantes

- En Docker Compose la aplicación recibe la variable `DATABASE_URL` para conectarse a PostgreSQL.
- El servicio `db` tiene volumen persistente `db_data` para que los datos sobrevivan reinicios.
- El proyecto fue adaptado a los requisitos del taller usando la base del parcial del segundo corte, con lógica de negocio libre y endpoints de creación/listado.

---

### Resultado esperado

- `docker compose ps` muestra ambos servicios.
- Las pruebas dentro del contenedor pasan.
- El nuevo endpoint `POST /recargas` y `GET /recargas` están presentes.

