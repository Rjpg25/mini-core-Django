# Mini Core — Gestión de Ventas y Comisiones

Aplicación web desarrollada con Django y Bootstrap para registrar ventas, administrar sus datos y calcular comisiones por vendedor dentro de un periodo seleccionado.

Proyecto académico desarrollado por Ricardo Piñango, estudiante de Ingeniería en Software de la Universidad de las Américas (UDLA), Ecuador.

## Estado del proyecto

Funcionalidad local implementada y comprobada manualmente.

Despliegue público y video de demostración pendientes.

## Funcionalidades

- Registrar ventas asociadas a un vendedor.
- Consultar el listado de ventas.
- Editar y eliminar ventas con confirmación.
- Filtrar ventas por vendedor y fechas.
- Consultar cantidad de ventas y monto vendido.
- Mostrar reglas de comisión activas.
- Calcular comisiones por rango de fechas.
- Consultar el resumen de comisiones por vendedor.
- Mostrar el detalle de la comisión de cada venta.
- Administrar vendedores, reglas y ventas desde Django Admin.
- Validar montos positivos y rangos de fechas.
- Proteger los formularios de modificación mediante tokens CSRF.

## Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python | Lenguaje de programación |
| Django 5.2 | Modelos, formularios, vistas y rutas |
| Bootstrap 5.3.3 | Estilos e interfaz responsive |
| HTML y CSS | Plantillas y personalización visual |
| SQLite | Base de datos local |
| PostgreSQL | Base de datos prevista para Render |
| Gunicorn | Servidor de aplicación para el despliegue |
| WhiteNoise | Archivos estáticos en producción |
| DJ-Database-URL | Configuración de la conexión a PostgreSQL |
| Psycopg | Adaptador de PostgreSQL |
| Git y GitHub | Control de versiones y repositorio |

Las versiones exactas de las dependencias Python están en `requirements.txt`.

Bootstrap se carga mediante CDN, por lo que requiere conexión a internet.

## Arquitectura

El proyecto utiliza el patrón MTV de Django:

- **Model:** `ventas/models.py` define vendedores, reglas y ventas.
- **Template:** `ventas/templates/ventas/` contiene las páginas HTML con Bootstrap.
- **View:** `ventas/views.py` procesa solicitudes y prepara los resultados.

Los archivos `urls.py` relacionan las direcciones del sitio con sus vistas.

En la comparación con MVC, los modelos representan los datos, las plantillas cumplen la función de presentación y las vistas de Django participan en el control de las solicitudes.

## Reglas de negocio

Cada venta pertenece a un vendedor y debe tener un monto positivo.

La comisión se calcula utilizando la regla activa con el mayor monto mínimo que alcance la venta.

Si ninguna regla aplica, la comisión es cero.

El porcentaje se almacena en formato decimal: `0.08` representa el 8 %.

### Ejemplos con las reglas de prueba

| Monto mínimo | Porcentaje |
|---:|---:|
| $500 | 8 % |
| $600 | 6 % |
| $800 | 10 % |

| Venta | Porcentaje aplicado | Comisión |
|---:|---:|---:|
| $400 | 0 % | $0 |
| $500 | 8 % | $40 |
| $600 | 6 % | $36 |
| $900 | 10 % | $90 |

Una venta de $600 aplica la regla del 6 %, porque tiene el mayor monto mínimo aplicable.

El cálculo por periodo incluye tanto la fecha inicial como la final.

Los resultados se calculan con las reglas actualmente activas; no se almacenan como un historial independiente de comisiones.

## Estructura del proyecto

```text
mini_core_Django/
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── ventas/
│   ├── migrations/
│   ├── templates/
│   │   └── ventas/
│   │       ├── base.html
│   │       ├── lista.html
│   │       ├── formulario.html
│   │       ├── conf_eliminacion.html
│   │       └── comisiones.html
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── .gitignore
├── build.sh
├── manage.py
├── README.md
└── requirements.txt
```

El entorno `.venv`, la base `db.sqlite3` y la carpeta `staticfiles` se generan localmente y no se incluyen en el repositorio.

## Instalación y ejecución local

### Requisitos

- Python 3.14, versión utilizada en el desarrollo.
- Git para clonar el repositorio.
- VS Code o un editor de código.
- Conexión a internet para instalar dependencias y cargar Bootstrap.

### 1. Obtener el proyecto

Clonar el repositorio desde GitHub o descargar y extraer su ZIP.

Abrir la carpeta principal en VS Code y una terminal PowerShell.

### 2. Crear el entorno virtual

```powershell
py -3.14 -m venv .venv
```

### 3. Instalar las dependencias

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
```

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Crear las tablas

```powershell
.\.venv\Scripts\python.exe manage.py migrate
```

### 5. Crear un administrador

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

### 6. Comprobar la configuración

```powershell
.\.venv\Scripts\python.exe manage.py check
```

### 7. Ejecutar el servidor

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Aplicación:

http://127.0.0.1:8000/

Administrador:

http://127.0.0.1:8000/admin/

Para detener el servidor, pulsar `Ctrl + C`.

## Datos iniciales

La instalación crea una base vacía. Los datos iniciales deben registrarse desde Django Admin.

1. Crear vendedores.
2. Crear reglas de comisión activas.
3. Registrar ventas desde la interfaz principal.

Los ejemplos de este README utilizan reglas de 8 % desde $500, 6 % desde $600 y 10 % desde $800.

## Rutas principales

| Ruta | Función |
|---|---|
| `/` | Listado y filtros de ventas |
| `/nueva/` | Registrar venta |
| `/<id>/editar/` | Editar venta |
| `/<id>/eliminar/` | Confirmar eliminación |
| `/comisiones/` | Calcular comisiones por periodo |
| `/admin/` | Administración de Django |

## Validación manual

Se comprobaron las siguientes operaciones durante el desarrollo:

- Registro, edición y eliminación de ventas.
- Filtros por vendedor y fechas.
- Limpieza de filtros.
- Cálculo de comisiones por periodo.
- Resumen por vendedor y detalle por venta.

Para comprobar las reglas de ejemplo, cuatro ventas de $400, $500, $600 y $900 deben producir $166 de comisiones.

Los cálculos utilizan `Decimal`; los importes se muestran con dos decimales.

## Despliegue en Render

Configuración preparada para utilizar un Web Service de Python y PostgreSQL.

### Comando de construcción

```bash
bash build.sh
```

### Comando de inicio

```bash
python -m gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
```

### Variables de entorno

| Variable | Uso |
|---|---|
| `SECRET_KEY` | Clave secreta generada para producción |
| `DATABASE_URL` | Conexión a PostgreSQL |

Render proporciona las variables `RENDER` y `RENDER_EXTERNAL_HOSTNAME`, utilizadas para reconocer el entorno de producción y configurar el dominio permitido.

En Render se desactiva `DEBUG`, se habilitan cookies seguras y se sirven los archivos estáticos con WhiteNoise.

El script `build.sh` instala dependencias, recoge archivos estáticos y aplica migraciones.

La base PostgreSQL es independiente de SQLite: los datos locales no se transfieren automáticamente.

**URL pública:** pendiente de añadir después del despliegue.

## Acceso a la aplicación

Las páginas de ventas y comisiones no requieren login.

Django Admin requiere una cuenta de administrador.

La versión actual está destinada a demostración académica con datos de prueba.

## Video de demostración

**Enlace:** pendiente de añadir después de grabar el video.

El video mostrará la configuración del despliegue, el acceso a la URL pública y las funcionalidades principales.

## Autor

**Ricardo Piñango**

Ingeniería en Software — Universidad de las Américas, Ecuador.

GitHub: https://github.com/Rjpg25

## Referencia del proyecto

Este proyecto replica la funcionalidad del Mini Core de ventas y comisiones proporcionado como material de referencia.

La implementación utiliza Django Templates y Bootstrap para la interfaz.