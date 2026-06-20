"# Proyecto Final de Automatización

## Propósito del proyecto

Este proyecto implementa una suite de automatización que cubre pruebas de interfaz de usuario (UI) y pruebas de API para validar durante el desarrollo:

- flujos de compra completos en la aplicación de demostración de Sauce Labs,
- navegación y manejo de carrito,
- validaciones de login y checkout,
- operaciones REST básicas contra el servicio público `reqres.in`.

El objetivo es demostrar una arquitectura organizada de pruebas automatizadas con `pytest`, `Selenium` y `requests`.

## Tecnologías utilizadas

- Python
- `pytest` para ejecución de pruebas y marcadores personalizados
- `pytest-html` para generar reportes HTML
- `Selenium` para pruebas de interfaz de usuario en navegador Edge
- `webdriver-manager` para administrar el driver del navegador automáticamente
- `requests` para pruebas de API REST
- `python-dotenv` para manejo de configuración en entorno (aunque no se usa directamente en los tests actuales)

## Estructura del proyecto

La estructura del proyecto incluye carpetas de datos, páginas de prueba, casos de prueba, utilidades y reportes.

```
automatizacion proyecto final/
├─ data/
│  ├─ checkout_flows.json
│  ├─ users.csv
│  └─ users.json
├─ pages/
│  ├─ api/
│  │  ├─ api_client.py
│  │  └─ api_user.py
│  └─ ui/
│     ├─ __init__.py
│     ├─ base_page.py
│     ├─ cart_page.py
│     ├─ checkout_page.py
│     ├─ login_page.py
│     └─ products_page.py
├─ tests/
│  ├─ api/
│  │  ├─ conftest.py
│  │  └─ test_api.py
│  ├─ ui/
│  │  ├─ conftest.py
│  │  ├─ test_cart.py
│  │  ├─ test_checkout.py
│  │  ├─ test_e2e.py
│  │  ├─ test_negative.py
│  │  └─ test_page.py
│  └─ conftest.py
├─ utils/
│  ├─ data_loader.py
│  └─ driver_factory.py
├─ reports/
│  ├─ report.html
│  ├─ logs/
│  └─ screenshots/
├─ requirements.txt
└─ pytest.ini
```

- `data/`: datos de prueba y escenarios parametrizados.
- `pages/api/`: cliente API y capa de acciones para las pruebas de API.
- `pages/ui/`: modelo de objetos de página para las pruebas de UI.
- `tests/api/`: pruebas de integración con servicios REST.
- `tests/ui/`: pruebas end-to-end y pruebas de validación de la interfaz.
- `tests/conftest.py`: configuración global de pytest, fixtures y hooks.
- `utils/`: utilidades compartidas para gestión de webdriver y carga de datos.
- `reports/`: reportes de prueba, logs y capturas de pantalla.
- `requirements.txt`: dependencias del proyecto.
- `pytest.ini`: configuración de pytest y reporte HTML.

## Cómo instalar las dependencias

1. Crear un entorno virtual (recomendado):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar las dependencias:

```powershell
pip install -r requirements.txt
```

## Cómo ejecutar las pruebas

Desde la raíz del proyecto:

- Ejecutar todas las pruebas:

```powershell
pytest
```

- Ejecutar solo pruebas UI y usar el modo headless:

```powershell
pytest -m "not api" --headless
```

- Ejecutar solo pruebas API:

```powershell
pytest -m api
```

- Ejecutar una prueba específica:

```powershell
pytest tests/ui/test_e2e.py::test_end_to_end_purchase_flow
```

## Cómo interpretar los reportes generados

Al ejecutar `pytest`, se genera automáticamente un reporte HTML en:

- `reports/report.html`

Elementos importantes del reporte:

- `Passed`, `Failed`, `Skipped`: resumen del estado de cada prueba
- `Duration`: tiempo consumido por cada prueba
- `Logs`: se incluyen registros de UI y API cuando están disponibles
- `Screenshot`: si una prueba UI falla, se adjunta una captura de pantalla en el reporte

Adicionalmente, el proyecto mantiene:

- `reports/logs/`: archivos de log por prueba
- `reports/screenshots/`: capturas de pantalla de fallos UI

> Nota: el reporte HTML es `self-contained`, por lo que puede abrirse directamente en el navegador sin dependencias adicionales.
" 
