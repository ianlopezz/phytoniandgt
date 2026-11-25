"""Gráficos PNG generados en servidor con Matplotlib."""
import base64
from io import BytesIO
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PALETTE = ["#0b6b5d", "#d58b42", "#d76050", "#5979a8", "#8c6aa8", "#76a69a"]


def _img(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png", dpi=135, bbox_inches="tight", facecolor="#ffffff")
    plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode("ascii")


def generar_graficos(df):
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.spines.top": False, "axes.spines.right": False})
    fig, ax = plt.subplots(figsize=(8, 3.4))
    horas = df.groupby("hora").size().reindex(range(24), fill_value=0)
    ax.bar(horas.index, horas.values, color=PALETTE[0], width=.72)
    ax.set(title="Accidentes registrados por hora", xlabel="Hora del día", ylabel="Accidentes")
    ax.set_xticks(range(0, 24, 2)); ax.grid(axis="y", alpha=.18)
    hora = _img(fig)

    fig, ax = plt.subplots(figsize=(8, 3.4))
    zonas = df.groupby("zona").agg(accidentes=("id", "count"), fallecidos=("fallecidos", "sum"))
    zonas = zonas.sort_values("accidentes", ascending=True)
    if not zonas.empty:
        ax.barh(zonas.index, zonas.accidentes, label="Accidentes", color=PALETTE[3])
        ax.set_xlabel("Accidentes")
    ax.set_title("Accidentes por tipo de zona")
    ax.grid(axis="x", alpha=.18)
    zona = _img(fig)

    fig, ax = plt.subplots(figsize=(8, 3.5))
    top = df.groupby("tipo_accidente").size().sort_values(ascending=False).head(8).sort_values()
    if not top.empty:
        ax.barh(top.index, top.values, color=PALETTE[1])
    ax.set(title="Tipos de accidente más frecuentes", xlabel="Accidentes")
    ax.grid(axis="x", alpha=.18)
    tipos = _img(fig)
    return {"hora": hora, "zona": zona, "tipos": tipos}
