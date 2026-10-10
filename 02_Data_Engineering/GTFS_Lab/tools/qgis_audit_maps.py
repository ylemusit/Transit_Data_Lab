"""Render the commercial atlas with the installed QGIS Python (offline).

Run with python-qgis.bat, not the laboratory virtualenv. No GUI or network layers.
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

from qgis.core import (Qgis, QgsApplication, QgsCategorizedSymbolRenderer, QgsCoordinateReferenceSystem,
                       QgsCoordinateTransform, QgsMapRendererParallelJob, QgsMapSettings, QgsProject,
                       QgsRectangle, QgsRendererCategory, QgsSymbol, QgsVectorLayer,
                       QgsPalLayerSettings, QgsTextFormat, QgsTextBufferSettings, QgsVectorLayerSimpleLabeling)
from qgis.PyQt.QtCore import QSize, Qt
from qgis.PyQt.QtGui import QColor, QFont, QFontDatabase, QImage, QPainter, QPen

FONT_FAMILY='Arial'


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def load(path, name, color, width=None):
    layer=QgsVectorLayer(str(path),name,'ogr')
    if not layer.isValid(): raise RuntimeError('Invalid GIS layer: '+str(path))
    symbol=QgsSymbol.defaultSymbol(layer.geometryType())
    symbol.setColor(QColor(color))
    if width is not None: symbol.setWidth(width)
    layer.renderer().setSymbol(symbol)
    return layer


def render(layers, bounds, destination, label, notes, crs, size=(2100,600)):
    settings=QgsMapSettings()
    settings.setDestinationCrs(crs)
    settings.setLayers(layers)
    settings.setBackgroundColor(QColor('#F7FAFB'))
    settings.setOutputSize(QSize(*size))
    settings.setOutputDpi(300)
    rect=QgsRectangle(bounds)
    if rect.width()<25 or rect.height()<25:
        center=rect.center()
        rect=QgsRectangle(center.x()-max(25,rect.width()/2),center.y()-max(25,rect.height()/2),
                          center.x()+max(25,rect.width()/2),center.y()+max(25,rect.height()/2))
    rect.scale(1.13)
    settings.setExtent(rect)
    job=QgsMapRendererParallelJob(settings)
    job.start();job.waitForFinished()
    errors=[e.message for e in job.errors()]
    if errors: raise RuntimeError('Map renderer: '+'; '.join(errors))
    rendered=job.renderedImage()
    image=QImage(size[0],size[1]+120,QImage.Format.Format_ARGB32)
    image.fill(QColor('white'))
    painter=QPainter(image)
    painter.drawImage(0,0,rendered)
    painter.setPen(QColor('#143747'))
    painter.setFont(QFont(FONT_FAMILY,24))
    painter.drawText(28,size[1]+40,label)
    painter.setFont(QFont(FONT_FAMILY,23))
    painter.drawText(28,size[1]+78,notes)
    # Metric scale, derived from actual adjusted map extent; no fixed guessed scale.
    visible=settings.visibleExtent()
    m_per_pixel=visible.width()/size[0]
    target=m_per_pixel*260
    base=10**math.floor(math.log10(target))
    bar=max(v for v in (base,2*base,5*base,10*base) if v<=target)
    pixels=bar/m_per_pixel
    x,y=size[0]-360,size[1]-30
    painter.setPen(QPen(QColor('#143747'),5))
    painter.drawLine(int(x),y,int(x+pixels),y)
    painter.drawLine(int(x),y-12,int(x),y+12)
    painter.drawLine(int(x+pixels),y-12,int(x+pixels),y+12)
    painter.setFont(QFont(FONT_FAMILY,24))
    painter.drawText(int(x),y-20,(f'{bar/1000:g} km' if bar>=1000 else f'{bar:g} m'))
    painter.drawText(size[0]-90,48,'N')
    painter.drawLine(size[0]-75,60,size[0]-75,100)
    painter.drawLine(size[0]-75,60,size[0]-86,76)
    painter.drawLine(size[0]-75,60,size[0]-64,76)
    painter.end()
    destination.parent.mkdir(parents=True,exist_ok=True)
    if not image.save(str(destination),'PNG'):raise RuntimeError('Cannot save map')
    return dict(file=destination.name,width=image.width(),height=image.height(),
                extent=[visible.xMinimum(),visible.yMinimum(),visible.xMaximum(),visible.yMaximum()],
                crs=crs.authid(),scale_bar_m=bar,metres_per_pixel=m_per_pixel)


def main(output, details_only=False):
    global FONT_FAMILY
    app=QgsApplication([],False)
    app.initQgis()
    font_id=QFontDatabase.addApplicationFont('C:/Windows/Fonts/arial.ttf')
    if font_id<0:raise RuntimeError('Cannot load Arial for headless map labels')
    FONT_FAMILY=QFontDatabase.applicationFontFamilies(font_id)[0]
    project=QgsProject.instance()
    results=output/'01_RESULTADOS';gis=results/'gis';maps=results/'mapas'
    atlas=json.loads((output/'02_EVIDENCIAS/ATLAS_MODEL.json').read_text(encoding='utf-8'))
    context=load(gis/'lineas.geojson','Red de contexto','#D4DFE3',0.25)
    routes=load(gis/'lineas.geojson','Itinerarios de las líneas','#1D6985',0.85)
    incidents=load(gis/'incidencias.geojson','Incidencias cartográficas','#CC392F')
    categories=[]
    for cid,color,label in [('PAL-G07-DUP','#C53A32','Puntos coincidentes y distancia repetida'),
                            ('PAL-G07-EQUAL','#E28B18','Puntos distintos y distancia repetida')]:
        symbol=QgsSymbol.defaultSymbol(incidents.geometryType())
        symbol.setColor(QColor(color));symbol.setSize(2.6)
        categories.append(QgsRendererCategory(cid,symbol,label))
    incidents.setRenderer(QgsCategorizedSymbolRenderer('case_id',categories))
    crs=QgsCoordinateReferenceSystem('EPSG:25831')
    project.setCrs(crs)
    transform=QgsCoordinateTransform(routes.crs(),crs,project)
    for layer in [context,routes,incidents]:project.addMapLayer(layer)
    receipts=[]
    if details_only:
        prior=json.loads((output/'02_EVIDENCIAS/QGIS_RECEIPT.json').read_text(encoding='utf-8'))
        receipts=[r for r in prior['maps'] if not r['file'].startswith('ejemplo_')]
    for route in ([] if details_only else atlas['routes']):
        rid=route['route_id']
        expression='"route_id" = \''+rid.replace("'","''")+'\''
        if not routes.setSubsetString(expression) or not incidents.setSubsetString(expression):raise RuntimeError('Cannot filter route')
        routes.updateExtents()
        bounds=transform.transformBoundingBox(routes.extent())
        receipts.append(render([incidents,routes,context],bounds,results/route['image'],
                        'Línea '+route['label']+' | '+rid,
                        'Azul: línea | Rojo/naranja: incidencias | Fuente: GTFS',crs))
        print('Rendered '+rid,flush=True)
    for item in ([] if details_only else atlas['unassigned_shapes']):
        sid=item['shape_id'];expression='"shape_id" = \''+sid.replace("'","''")+'\''
        routes.setSubsetString(expression);incidents.setSubsetString(expression);routes.updateExtents()
        receipts.append(render([incidents,routes,context],transform.transformBoundingBox(routes.extent()),results/item['image'],
                        'Trazado '+sid+' | Sin viaje vinculado',
                        'Línea no determinada | Fuente: GTFS',crs))
    examples=[]
    for detail in atlas['case_details']:
        if not detail['case_id'].startswith('PAL-G07'):continue
        ex=detail['example'];a,b=ex['previous']['values'],ex['values']
        for label,row in [('Anterior',a),('Actual',b)]:
            examples.append(dict(type='Feature',geometry=dict(type='Point',coordinates=[float(row['shape_pt_lon']),float(row['shape_pt_lat'])]),
                                 properties=dict(case_id=detail['case_id'],position=label,sequence=row['shape_pt_sequence'],distance=row['shape_dist_traveled'])))
        if ex['coordinate_pair_equal']:
            examples.pop()
            examples[-1]['properties'].update(position='Anterior y actual',sequence=a['shape_pt_sequence']+' / '+b['shape_pt_sequence'])
    write(gis/'ejemplos.geojson',dict(type='FeatureCollection',features=examples))
    example_layer=load(gis/'ejemplos.geojson','Pares de vértices de los ejemplos','#763399')
    example_layer.renderer().symbol().setSize(3.3)
    label_settings=QgsPalLayerSettings()
    label_settings.fieldName='"position" || \' - punto \' || "sequence"'
    label_settings.isExpression=True
    text_format=QgsTextFormat();text_format.setFont(QFont(FONT_FAMILY));text_format.setSize(9)
    text_format.setColor(QColor('#48236C'))
    buffer=QgsTextBufferSettings();buffer.setEnabled(True);buffer.setSize(0.8);buffer.setColor(QColor('white'))
    text_format.setBuffer(buffer);label_settings.setFormat(text_format)
    example_layer.setLabeling(QgsVectorLayerSimpleLabeling(label_settings));example_layer.setLabelsEnabled(True)
    project.addMapLayer(example_layer)
    for detail in atlas['case_details']:
        if not detail['case_id'].startswith('PAL-G07'):continue
        cid=detail['case_id'];ex=detail['example'];sid=ex['values']['shape_id']
        example_layer.setSubsetString('"case_id" = \''+cid+'\'')
        example_layer.updateExtents()
        routes.setSubsetString('"shape_id" = \''+sid.replace("'","''")+'\'')
        incidents.setSubsetString('"case_id" = \''+cid+'\' AND "data_row" = '+str(ex['data_row']))
        bounds=transform.transformBoundingBox(example_layer.extent())
        before=ex['previous']['values'];after=ex['values']
        receipts.append(render([example_layer,incidents,routes,context],bounds,maps/('ejemplo_'+cid+'.png'),
                         cid+' | Trazado '+sid,
                         'Vértices '+before['shape_pt_sequence']+' y '+after['shape_pt_sequence']+' | Distancia: '+before['shape_dist_traveled']+' / '+after['shape_dist_traveled']+' | Unidades a confirmar',
                         crs,size=(2100,1300)))
    for layer in [routes,incidents,example_layer]:layer.setSubsetString('')
    project.setFilePathStorage(Qgis.FilePathType.Relative)
    project.viewSettings().setDefaultViewExtent(QgsReferencedRectangle(transform.transformBoundingBox(routes.extent()),crs))
    # Hide the examples by default; users can toggle them for the detailed inspection.
    project.layerTreeRoot().findLayer(example_layer.id()).setItemVisibilityChecked(False)
    if not project.write(str(gis/'Auditoria_Palma_R4.qgz')):raise RuntimeError('Cannot write QGIS project')
    project.clear()
    if not project.read(str(gis/'Auditoria_Palma_R4.qgz')):raise RuntimeError('Cannot reopen QGIS project')
    if any(not l.isValid() for l in project.mapLayers().values()):raise RuntimeError('Reopened project has invalid layers')
    write(output/'02_EVIDENCIAS/QGIS_RECEIPT.json',dict(qgis_version=Qgis.QGIS_VERSION,renderer='QgsMapRendererParallelJob',
          source_coordinates=True,external_basemap=False,headless=True,project_reopened=True,
          project_valid_layers=len(project.mapLayers()),font_family=FONT_FAMILY,maps=receipts,interactive_navigation='NOT_TESTED'))
    print(json.dumps(dict(status='PASS',maps=len(receipts),qgis=Qgis.QGIS_VERSION)),flush=True)
    project.clear()
    app.exitQgis()


if __name__=='__main__':
    from qgis.core import QgsReferencedRectangle
    main(Path(sys.argv[1]),details_only='--details-only' in sys.argv[2:])
