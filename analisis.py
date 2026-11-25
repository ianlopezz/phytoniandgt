"""Carga, filtra y resume los microdatos de accidentes."""
from pathlib import Path
import pandas as pd

CSV_PATH = Path(__file__).parent / "data" / "accidentes_2024.csv"
DIAS = ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES", "SÁBADO", "DOMINGO"]
MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]


def cargar_datos():
    df = pd.read_csv(CSV_PATH)
    for col in ["mes", "hora", "victimas", "fallecidos", "heridos_hospitalizados", "heridos_no_hospitalizados"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)
    df["mes_nombre"] = df["mes"].map(lambda x: MESES[x - 1] if 1 <= x <= 12 else "Sin dato")
    df["gravedad"] = df.apply(lambda r: "Con fallecidos" if r.fallecidos > 0 else ("Con heridos hospitalizados" if r.heridos_hospitalizados > 0 else "Sin hospitalizados"), axis=1)
    return df


def filtrar(df, filtros):
    out = df
    for key, col in [("provincia", "provincia"), ("zona", "zona"), ("tipo_via", "tipo_via"), ("gravedad", "gravedad")]:
        if filtros.get(key):
            out = out[out[col] == filtros[key]]
    if filtros.get("mes"):
        out = out[out.mes == int(filtros["mes"])]
    if filtros.get("busqueda"):
        q = filtros["busqueda"].strip().casefold()
        out = out[out["tipo_accidente"].str.casefold().str.contains(q, na=False) | out["provincia"].str.casefold().str.contains(q, na=False) | out["tipo_via"].str.casefold().str.contains(q, na=False)]
    return out


def ordenar(df, campo, direccion):
    permitidos = {"mes", "dia_semana", "hora", "provincia", "zona", "tipo_via", "tipo_accidente", "victimas", "fallecidos", "gravedad"}
    campo = campo if campo in permitidos else "victimas"
    return df.sort_values(campo, ascending=direccion != "desc", kind="stable")


def opciones(df):
    return {"provincias": sorted(df.provincia.unique()), "zonas": sorted(df.zona.unique()), "vias": sorted(df.tipo_via.unique()), "gravedades": ["Con fallecidos", "Con heridos hospitalizados", "Sin hospitalizados"]}


def indicadores(df):
    return {"accidentes": len(df), "victimas": int(df.victimas.sum()), "fallecidos": int(df.fallecidos.sum()), "con_victimas": int((df.victimas > 0).sum())}


def resumen(df):
    if df.empty:
        return "No hay accidentes que coincidan con esos filtros."
    dia = df.dia_semana.value_counts().idxmax()
    hora = int(df.hora.value_counts().idxmax())
    provincia = df.provincia.value_counts().idxmax()
    return f"En esta selección, el día con más registros es {dia.lower()}, la hora más frecuente es {hora:02d}:00 y la provincia con más accidentes es {provincia}. Son recuentos de accidentes con víctimas, no tasas ajustadas por tráfico."
