#!/usr/bin/env python3
"""Elige uno o varios mini-descansos al azar del catálogo de la skill.

Uso:
    python3 mini_descanso.py [--contexto oficina|remoto|cualquiera]
                             [--minutos N] [--tipo social|movimiento|sentidos|cualquiera]
                             [-n N] [--excluir id1,id2] [--semilla N] [--json]

Los descansos sociales pesan el doble al sortear: el objetivo principal de la
skill es que la persona hable con gente real. Si ningún descanso cumple los
filtros, se relajan en orden (duración, tipo, contexto) y se avisa por stderr.
Solo usa la biblioteca estándar.
"""

import argparse
import json
import random
import sys
from pathlib import Path

CATALOGO = Path(__file__).resolve().parent.parent / "assets" / "mini_descansos.json"
PESO_SOCIAL = 2
TIPOS = ("social", "movimiento", "sentidos")


def cargar(ruta=CATALOGO):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)["descansos"]


def filtrar(descansos, contexto, minutos, tipo, excluir):
    resultado = []
    for d in descansos:
        if d["id"] in excluir:
            continue
        if contexto != "cualquiera" and d["contexto"] not in (contexto, "ambos"):
            continue
        if minutos is not None and d["minutos"] > minutos:
            continue
        if tipo != "cualquiera" and d["tipo"] != tipo:
            continue
        resultado.append(d)
    return resultado


def buscar_candidatos(descansos, contexto, minutos, tipo, excluir):
    """Aplica los filtros y, si no queda nada, los relaja de uno en uno."""
    intentos = [
        (contexto, minutos, tipo, None),
        (contexto, None, tipo, "sin límite de duración"),
        (contexto, None, "cualquiera", "sin límite de duración ni de tipo"),
        ("cualquiera", None, "cualquiera", "sin filtros"),
    ]
    for ctx, mins, tp, aviso in intentos:
        candidatos = filtrar(descansos, ctx, mins, tp, excluir)
        if candidatos:
            if aviso:
                print(f"Aviso: ningún descanso cumplía los filtros; elegido {aviso}.", file=sys.stderr)
            return candidatos
    return []


def sortear(candidatos, n, rng):
    """Muestreo ponderado sin reemplazo."""
    restantes = list(candidatos)
    elegidos = []
    while restantes and len(elegidos) < n:
        pesos = [PESO_SOCIAL if d["tipo"] == "social" else 1 for d in restantes]
        d = rng.choices(restantes, weights=pesos, k=1)[0]
        elegidos.append(d)
        restantes.remove(d)
    return elegidos


def formatear(d):
    return f"Mini-descanso · {d['minutos']} min · {d['tipo']} [{d['id']}]\n{d['actividad']}"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Elige un mini-descanso lejos de la pantalla.")
    parser.add_argument("--contexto", choices=("oficina", "remoto", "cualquiera"), default="cualquiera")
    parser.add_argument("--minutos", type=int, default=None, help="duración máxima en minutos")
    parser.add_argument("--tipo", choices=TIPOS + ("cualquiera",), default="cualquiera")
    parser.add_argument("-n", type=int, default=1, help="cuántas opciones devolver")
    parser.add_argument("--excluir", default="", help="ids ya usados, separados por comas")
    parser.add_argument("--semilla", type=int, default=None, help="para resultados reproducibles")
    parser.add_argument("--json", action="store_true", help="salida en JSON")
    args = parser.parse_args(argv)

    excluir = {x.strip() for x in args.excluir.split(",") if x.strip()}
    candidatos = buscar_candidatos(cargar(), args.contexto, args.minutos, args.tipo, excluir)
    if not candidatos:
        print("No quedan descansos disponibles con esas exclusiones.", file=sys.stderr)
        return 1

    elegidos = sortear(candidatos, max(1, args.n), random.Random(args.semilla))
    if args.json:
        print(json.dumps(elegidos, ensure_ascii=False, indent=2))
    else:
        print("\n\n".join(formatear(d) for d in elegidos))
    return 0


if __name__ == "__main__":
    sys.exit(main())
