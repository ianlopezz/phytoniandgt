# Observatorio de accidentes con víctimas — España, 2024

Dashboard académico con Flask, Jinja, pandas y Matplotlib. Las filas corresponden a accidentes con víctimas notificadas, no al total de siniestros de tráfico.

## Puesta en marcha

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python convertir_datos.py
python app.py
```

Después, abre http://127.0.0.1:5000.

El libro XLSX oficial y el diccionario se guardan en `data/`. El CSV simplificado del dashboard se regenera con `convertir_datos.py`.

## Estructura

- `app.py`: únicamente rutas y coordinación de vistas.
- `analisis.py`: lectura, filtros, ordenación e indicadores.
- `graficos.py`: gráficos Matplotlib.
- `templates/index.html`: interfaz Jinja.
- `static/styles.css`: estilos adaptables.
- `data/`: dataset fuente, diccionario y CSV derivado.

## Fuente y limitaciones

Dirección General de Tráfico, microdatos de accidentes con víctimas de 2024, publicados en [datos.gob.es](https://datos.gob.es/es/catalogo/e00130502-ficheros-de-microdatos-de-accidentes-con-victimas-2024). Los datos incluyen vías urbanas e interurbanas de España. La tabla agrupa accidentes con víctimas y no aporta denominadores de exposición al tráfico; por ello, los gráficos muestran recuentos, no riesgos relativos ni causalidad.
