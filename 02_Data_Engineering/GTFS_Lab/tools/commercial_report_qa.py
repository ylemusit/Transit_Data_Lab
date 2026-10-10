"""Render every page and check geometry/text/inventory; visual acceptance is separate.

Requires PyMuPDF and Pillow in the QA Python, not in the frozen audit runtime.
"""
import argparse
import json
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw


def main(package, previews):
    pdf=package/'01_RESULTADOS/Informe_comercial_transporte.pdf'
    previews.mkdir(parents=True,exist_ok=True)
    document=pymupdf.open(pdf)
    evidence=package/'02_EVIDENCIAS'
    atlas=json.loads((evidence/'ATLAS_MODEL.json').read_text(encoding='utf-8'))
    checks=json.loads((evidence/'VALIDATIONS.json').read_text(encoding='utf-8'))
    regulatory=json.loads((evidence/'REGULATORY_REVIEW.json').read_text(encoding='utf-8'))
    full_text='\n'.join(page.get_text() for page in document)
    problems=[];page_rows=[]
    for i,page in enumerate(document):
        if abs(page.rect.width-595.276)>1 or abs(page.rect.height-841.89)>1:problems.append(f'Page {i+1}: not A4')
        spans=[s for b in page.get_text('dict')['blocks'] if b['type']==0 for line in b['lines'] for s in line['spans']]
        for span in spans:
            box=pymupdf.Rect(span['bbox'])
            if box.x0<0 or box.y0<0 or box.x1>page.rect.width+1 or box.y1>page.rect.height+1:problems.append(f'Page {i+1}: text outside page')
            if any(c in span['text'] for c in ('\ufffd','\u25a0')):problems.append(f'Page {i+1}: replacement glyph')
        text=page.get_text()
        if len(text)<100:problems.append(f'Page {i+1}: almost empty')
        image_rectangles=[page.get_image_rects(img[0])[0] for img in page.get_images()]
        for rect in image_rectangles:
            if rect.y1>788:problems.append(f'Page {i+1}: image in footer')
        page_rows.append(dict(page=i+1,text_characters=len(text),image_count=len(image_rectangles),
                              atlas_page='Atlas · líneas con incidencias cartográficas' in text))
        page.get_pixmap(matrix=pymupdf.Matrix(1.1,1.1)).save(previews/f'page_{i+1:02d}.png')
    for check in checks:
        if check['rule_id'] not in full_text:problems.append('Missing check: '+check['rule_id'])
    for req in regulatory['catalogue']:
        if req['requirement_id'] not in full_text:problems.append('Missing catalogue row: '+req['requirement_id'])
    for detail in atlas['case_details']:
        if detail['case_id'] not in full_text:problems.append('Missing case: '+detail['case_id'])
    if not document.get_toc():problems.append('Missing PDF bookmarks')
    for route in atlas['routes']:
        with Image.open(package/'01_RESULTADOS'/route['image']) as im:
            if im.size!=(2100,720):problems.append('Unexpected route map aspect ratio: '+route['route_id'])
    # Six-page sheets permit a complete visual scan; retain full-resolution pages too.
    for offset in range(0,len(document),6):
        sheet=Image.new('RGB',(1320,2850),'#D7E1E5');draw=ImageDraw.Draw(sheet)
        for j,i in enumerate(range(offset,min(offset+6,len(document)))):
            im=Image.open(previews/f'page_{i+1:02d}.png').convert('RGB')
            im.thumbnail((640,920))
            x=(j%2)*660+10;y=(j//2)*950+25
            sheet.paste(im,(x,y));draw.text((x,y-18),f'PAGE {i+1}',fill='#143747')
        sheet.save(previews/f'sheet_{offset//6+1:02d}.png')
    result=dict(status='PASS' if not problems else 'FAIL',pdf_pages=len(document),format='A4',
                route_maps=len(atlas['routes']),unassigned_shape_maps=len(atlas['unassigned_shapes']),
                detail_maps=2,unique_validations=len(checks),catalogue_requirements=len(regulatory['catalogue']),
                bookmarks=len(document.get_toc()),pages_rendered=len(document),problems=problems,pages=page_rows,
                visual_inspection='PENDING',interactive_QGIS_navigation='NOT_TESTED')
    (evidence/'REPORT_QA.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='pages'},ensure_ascii=False))
    if problems:raise SystemExit(1)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--package',type=Path,required=True);parser.add_argument('--previews',type=Path,required=True)
    args=parser.parse_args();main(args.package,args.previews)
