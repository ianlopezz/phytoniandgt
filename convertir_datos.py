"""Convierte el XLSX oficial de la DGT a un CSV reducido y legible."""
import csv
from pathlib import Path
from openpyxl import load_workbook

BASE = Path(__file__).parent
DATA = BASE / "data"


def labels(workbook, sheet):
    ws = workbook[sheet]
    return {row[0]: str(row[1]).strip() for row in ws.iter_rows(min_row=3, values_only=True) if row[0] is not None and row[1] is not None}


def main():
    dic = load_workbook(DATA / "diccionario.xlsx", read_only=True, data_only=True)
    maps = {name: labels(dic, name) for name in ["DIA_SEMANA", "COD_PROVINCIA", "ZONA_AGRUPADA", "TIPO_VIA", "TIPO_ACCIDENTE"]}
    source = load_workbook(DATA / "accidentes_2024.xlsx", read_only=True, data_only=True)["ACCIDENTES_24"]
    rows = source.iter_rows(values_only=True)
    header = next(rows)
    ix = {name: header.index(name) for name in ["ID_ACCIDENTE", "MES", "DIA_SEMANA", "HORA", "COD_PROVINCIA", "ZONA_AGRUPADA", "TIPO_VIA", "TIPO_ACCIDENTE", "TOTAL_VICTIMAS_30DF", "TOTAL_MU30DF", "TOTAL_HG30DF", "TOTAL_HL30DF"]}
    cols = ["id", "mes", "dia_semana", "hora", "provincia", "zona", "tipo_via", "tipo_accidente", "victimas", "fallecidos", "heridos_hospitalizados", "heridos_no_hospitalizados"]
    def val(row, key):
        return row[ix[key]]
    with (DATA / "accidentes_2024.csv").open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(cols)
        for r in rows:
            writer.writerow([
                val(r, "ID_ACCIDENTE"), val(r, "MES"), maps["DIA_SEMANA"].get(val(r, "DIA_SEMANA"), "Sin dato"),
                val(r, "HORA"), maps["COD_PROVINCIA"].get(val(r, "COD_PROVINCIA"), "Sin dato"),
                maps["ZONA_AGRUPADA"].get(val(r, "ZONA_AGRUPADA"), "Sin dato"),
                maps["TIPO_VIA"].get(val(r, "TIPO_VIA"), "Sin dato"), maps["TIPO_ACCIDENTE"].get(val(r, "TIPO_ACCIDENTE"), "Sin dato"),
                val(r, "TOTAL_VICTIMAS_30DF"), val(r, "TOTAL_MU30DF"), val(r, "TOTAL_HG30DF"), val(r, "TOTAL_HL30DF")
            ])
    print(f"CSV generado: {DATA / 'accidentes_2024.csv'}")


if __name__ == "__main__":
    main()
