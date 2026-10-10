"""Render every new PDF page and verify text geometry/identity with PyMuPDF."""
import argparse
import json
from pathlib import Path
import pymupdf as fitz
from PIL import Image, ImageDraw


def inspect(package, output):
    output.mkdir(parents=True, exist_ok=False)
    model = json.loads((package / "02_MODELO/REPORT_MODEL.json").read_text(encoding="utf-8"))
    results = []
    for relative in ("01_DIRECCION/Informe_direccion.pdf", "02_TECNICO/Informe_tecnico.pdf"):
        document = fitz.open(package / relative)
        if document.metadata["subject"] != "TDL semantic SHA-256 " + model["semantic_sha256"]:
            raise ValueError("PDF metadata differs")
        pages = []; texts = []
        for i, page in enumerate(document):
            text = page.get_text(); texts.append(text)
            if len(text.strip()) < 100: raise ValueError("Blank or nearly blank page")
            for block in page.get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    for span in line["spans"]:
                        x0, y0, x1, y1 = span["bbox"]
                        if x0 < 0 or y0 < 0 or x1 > page.rect.width+.5 or y1 > page.rect.height+.5:
                            raise ValueError("Text outside PDF page: " + relative)
            target = output / (relative.split("/")[0] + f"_{i+1:02d}.png")
            page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False).save(target)
            pages.append(target.name)
        alltext = "\n".join(texts)
        for case in model["cases"]:
            e = case["exposure"]
            value = f"{e['affected_count']:,}".replace(",", ".") + " de " + f"{e['eligible_count']:,}".replace(",", ".")
            if value not in alltext: raise ValueError("Case exposure missing from PDF: " + value)
            if relative.startswith("02_TECNICO") and case["case_id"] not in alltext: raise ValueError("Case ID missing")
        results.append({"path": relative, "pages": len(document), "rendered_pages": pages, "geometry": "PASS", "exposures": "PASS"})
    # Contact sheets supplement the full-resolution images; every page remains available.
    names = [name for row in results for name in row["rendered_pages"]]
    for offset in range(0, len(names), 4):
        canvas = Image.new("RGB", (1800, 2540), "#d9e2e8"); draw = ImageDraw.Draw(canvas)
        for j, name in enumerate(names[offset:offset+4]):
            img = Image.open(output / name); img.thumbnail((850, 1200))
            x = 25 + (j%2)*900; y = 35 + (j//2)*1270
            canvas.paste(img, (x,y)); draw.text((x,y-20), name, fill="black")
        canvas.save(output / f"contact_{offset//4+1:02d}.png")
    value = {"package": str(package), "checks": results, "human_visual_review": "PENDING"}
    (output / "QA.json").write_text(json.dumps(value, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    return value


if __name__ == "__main__":
    parser = argparse.ArgumentParser(); parser.add_argument("--package", type=Path, required=True); parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(); print(json.dumps(inspect(args.package, args.output), ensure_ascii=False))
