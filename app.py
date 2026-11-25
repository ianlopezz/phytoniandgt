"""Rutas del dashboard. La lógica está en analisis.py y graficos.py."""
from flask import Flask, render_template, request
from analisis import cargar_datos, filtrar, ordenar, opciones, indicadores, resumen
from graficos import generar_graficos

app = Flask(__name__)
DATOS = cargar_datos()


@app.get("/")
def inicio():
    filtros = {k: request.args.get(k, "") for k in ["provincia", "zona", "tipo_via", "gravedad", "mes", "busqueda"]}
    datos = ordenar(filtrar(DATOS, filtros), request.args.get("orden", "victimas"), request.args.get("direccion", "desc"))
    try:
        pagina = max(1, int(request.args.get("pagina", 1)))
    except ValueError:
        pagina = 1
    try:
        tamano = int(request.args.get("por_pagina", 25))
    except ValueError:
        tamano = 25
    if tamano not in (10, 25, 50, 100):
        tamano = 25
    total_paginas = max(1, (len(datos) + tamano - 1) // tamano)
    pagina = min(pagina, total_paginas)
    tabla = datos.iloc[(pagina - 1) * tamano:pagina * tamano].to_dict("records")
    return render_template("index.html", filtros=filtros, opciones=opciones(DATOS), kpis=indicadores(datos),
        explicacion=resumen(datos), charts=generar_graficos(datos), filas=tabla, pagina=pagina,
        total_paginas=total_paginas, total_registros=len(datos), orden=request.args.get("orden", "victimas"),
        direccion=request.args.get("direccion", "desc"), por_pagina=tamano, tamanos_pagina=(10, 25, 50, 100),
        meses=list(enumerate(__import__("analisis").MESES, 1)))


if __name__ == "__main__":
    app.run(debug=True)
