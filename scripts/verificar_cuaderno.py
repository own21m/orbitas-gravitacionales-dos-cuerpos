"""Verifica la copia histórica mediante lectura, sin ejecutar ninguna celda."""

import ast
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "orbitas-gravitacionales-dos-cuerpos.ipynb"
EXPECTED_SHA256 = "1256acb84d382c48b0c2d7ba02d9a24e79cd65919212a06dc60a07dbef6d3d73"


def main():
    """Comprueba integridad, estructura y sintaxis usando solo la biblioteca estándar."""
    raw = NOTEBOOK.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit("La copia del cuaderno difiere del original respaldado.")

    notebook = json.loads(raw)
    if notebook.get("nbformat") != 4 or not isinstance(notebook.get("cells"), list):
        raise SystemExit("El archivo no contiene la estructura esperada de notebook 4.")

    code_cells = 0
    outputs = 0
    for index, cell in enumerate(notebook["cells"]):
        if cell.get("cell_type") == "code":
            # ast.parse no importa módulos, integra ecuaciones ni ejecuta instrucciones.
            source = cell.get("source", "")
            if isinstance(source, list):
                source = "".join(source)
            ast.parse(source, filename=f"celda-{index}")
            code_cells += 1
            outputs += len(cell.get("outputs", []))

    print("Integridad SHA256: correcta")
    print(f"Celdas de código: {code_cells}; salidas guardadas: {outputs}")
    print("Sintaxis Python: correcta; ninguna celda fue ejecutada")


if __name__ == "__main__":
    main()
