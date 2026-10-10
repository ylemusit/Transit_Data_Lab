#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import { SpreadsheetFile, Workbook } from '@oai/artifact-tool';

const NAVY = '#17324D';
const PALE = '#EAF2F6';
const MUTED = '#526575';
const HEADERS = { fill: NAVY, font: { bold: true, color: '#FFFFFF', size: 10 }, wrapText: true, verticalAlignment: 'center', rowHeight: 32 };
const TITLE = { fill: NAVY, font: { bold: true, color: '#FFFFFF', size: 16 }, verticalAlignment: 'center', rowHeight: 30 };

function safeText(value) {
  if (value === null || value === undefined) return '';
  const text = typeof value === 'string' ? value : (typeof value === 'object' ? JSON.stringify(value) : String(value));
  return /^[\s]*[=+@]/.test(text) || /^[\s]*-[^0-9.]/.test(text) ? `'${text}` : text;
}
function cellValue(value) {
  if (typeof value === 'number' && Number.isFinite(value)) return value;
  if (typeof value === 'boolean') return value;
  return safeText(value);
}
function textChunks(value) {
  const text = JSON.stringify(value);
  const pieces = [];
  for (let start = 0; start < text.length; start += 30000) pieces.push(text.slice(start, start + 30000));
  return pieces.length ? pieces : [''];
}
function colName(n) {
  let s = '';
  while (n > 0) { const r = (n - 1) % 26; s = String.fromCharCode(65 + r) + s; n = Math.floor((n - 1) / 26); }
  return s;
}
function rowsOf(value) { return Array.isArray(value) ? value : []; }
function readField(object, ...keys) {
  for (const key of keys) if (object?.[key] !== undefined) return object[key];
  return '';
}
function getOccurrences(item) {
  const occurrences = item?.occurrences;
  return Array.isArray(occurrences) ? occurrences : occurrences == null ? [] : [occurrences];
}
function setBlock(sheet, range, values, format) {
  const safeRows = values.map(row => row.map(cellValue));
  sheet.getRange(range).values = safeRows;
  if (format) sheet.getRange(range).format = format;
}
function estimateRowHeight(row, widths, minimum = 26) {
  let lineCount = 1;
  row.forEach((value, index) => {
    const text = value === null || value === undefined ? '' : String(value);
    const charsPerLine = Math.max(8, Math.floor((widths[index] ?? 24) * 1.05));
    const lines = text.split('\n').reduce((sum, line) => sum + Math.max(1, Math.ceil(line.length / charsPerLine)), 0);
    lineCount = Math.max(lineCount, lines);
  });
  return Math.min(400, Math.max(minimum, lineCount * 15 + 10));
}
function applyAdaptiveHeights(sheet, rows, widths, startRow = 2) {
  rows.forEach((row, index) => {
    const rowNumber = startRow + index;
    sheet.getRange(`A${rowNumber}:${colName(widths.length)}${rowNumber}`).format.rowHeight = estimateRowHeight(row, widths);
  });
}
function addIdentityColumns(headers, rows, identity) {
  const identityHeaders = ['ID auditoría', 'ID ejecución', 'SHA-256 origen', 'Revisión'];
  const identityValues = [identity.client_audit_id ?? '', identity.audit_execution_id ?? '', identity.source_sha256 ?? '', identity.revision ?? ''];
  return { headers: [...headers, ...identityHeaders], rows: rows.map(row => [...row, ...identityValues]) };
}
function addDataSheet(workbook, name, headers, rows, widths = []) {
  const sheet = workbook.worksheets.add(name);
  sheet.showGridLines = false;
  const endCol = colName(headers.length);
  setBlock(sheet, `A1:${endCol}1`, [headers], HEADERS);
  if (rows.length) {
    const endRow = rows.length + 1;
    setBlock(sheet, `A2:${endCol}${endRow}`, rows);
    sheet.getRange(`A2:${endCol}${endRow}`).format.wrapText = true;
    sheet.getRange(`A2:${endCol}${endRow}`).format.verticalAlignment = 'top';
    sheet.tables.add(`A1:${endCol}${endRow}`, true, `${name.replace(/[^A-Za-z0-9]/g, '')}Table`);
  }
  widths.forEach((width, index) => { sheet.getRange(`${colName(index + 1)}:${colName(index + 1)}`).format.columnWidth = width; });
  return sheet;
}
function flattenRecords(records, prefix = '') {
  if (!records.length) return [];
  const keys = [...new Set(records.flatMap(record => record && typeof record === 'object' && !Array.isArray(record) ? Object.keys(record) : []))];
  return keys.map(key => ({ key: prefix ? `${prefix}.${key}` : key, values: records.map(record => record?.[key]) }));
}
function recordRows(items) {
  const columns = flattenRecords(items);
  const serialized = items.map(textChunks);
  const chunkCount = Math.max(1, ...serialized.map(parts => parts.length));
  return {
    headers: ['Índice', ...columns.map(x => x.key), ...Array.from({ length: chunkCount }, (_, i) => `Registro íntegro (JSON)${chunkCount > 1 ? ` [parte ${i + 1}]` : ''}`)],
    rows: items.map((item, i) => [i + 1, ...columns.map(x => item?.[x.key]), ...Array.from({ length: chunkCount }, (_, p) => serialized[i][p] ?? '')]),
  };
}
function listText(value) { return Array.isArray(value) ? value.map(x => typeof x === 'string' ? x : JSON.stringify(x)).join('\n') : value; }
function matrixFieldLabel(key) {
  const labels = {
    coverage: 'Cobertura', coverage_status: 'Estado de cobertura', coverage_count: 'Recuento de cobertura',
    expected_count: 'Recuento esperado', actual_count: 'Recuento observado', observed_count: 'Recuento observado',
    missing_count: 'Recuento ausente', details: 'Detalle', description: 'Descripción',
  };
  return labels[key] ?? key.replaceAll('_', ' ').replace(/\b\p{L}/gu, c => c.toLocaleUpperCase('es-ES'));
}

async function main() {
  const args = process.argv.slice(2);
  if (args.length < 2 || args.length > 3 || args[0] === '--help' || args[0] === '-h') {
    console.error('Uso: node professional_workbook.mjs input_model.json output.xlsx [qa_dir]');
    process.exit(args[0] === '--help' || args[0] === '-h' ? 0 : 2);
  }
  const [inputPath, outputPath] = args.slice(0, 2).map(x => path.resolve(x));
  const qaDir = args[2] ? path.resolve(args[2]) : process.env.PROFESSIONAL_QA_DIR ? path.resolve(process.env.PROFESSIONAL_QA_DIR) : undefined;
  const model = JSON.parse((await fs.readFile(inputPath, 'utf8')).replace(/^\uFEFF/, ''));
  const candidateSidecar = model.case_contract ?? model.sidecar ?? model.audit_cases ?? model.audit_cases_sidecar ?? model.TDL_AUDIT_CASES_V1 ?? (Array.isArray(model.cases) ? { cases: model.cases } : {});
  const sidecar = Array.isArray(candidateSidecar.cases) ? candidateSidecar : candidateSidecar.case_contract ?? candidateSidecar.payload ?? candidateSidecar;
  const sourceCases = rowsOf(sidecar.cases);
  const clientCases = rowsOf(model.client_cases);
  const coverage = model.coverage ?? {};
  const wb = Workbook.create();

  const summary = wb.worksheets.add('Resumen');
  summary.showGridLines = false;
  setBlock(summary, 'A1:F1', [['Informe de auditoría GTFS', '', '', '', '', '']], TITLE);
  const identity = model.identity ?? {};
  const identityRows = [
    ['ID auditoría cliente', identity.client_audit_id], ['ID ejecución', identity.audit_execution_id],
    ['SHA-256 de origen', identity.source_sha256], ['Revisión', identity.revision],
  ];
  setBlock(summary, 'A3:B6', identityRows, { fill: PALE, wrapText: true, verticalAlignment: 'top' });
  summary.getRange('A3:A6').format.font = { bold: true, color: NAVY };
  setBlock(summary, 'D3:E8', [
    ['Cobertura', 'Recuento'], ['Registros fuente', coverage.source_record_count], ['Eventos reconciliados', coverage.reconciled_event_count],
    ['Referencias fuente duplicadas', coverage.duplicate_source_reference_count], ['Registros sin clasificar', coverage.unclassified_record_count], ['Registros sin reconciliar', coverage.accounting_gap],
  ]);
  summary.getRange('D3:E3').format = HEADERS;
  summary.getRange('E4:E8').format.numberFormat = '#,##0';
  summary.getRange('A:A').format.columnWidth = 24;
  summary.getRange('B:B').format.columnWidth = 44;
  summary.getRange('C:C').format.columnWidth = 40;
  summary.getRange('D:D').format.columnWidth = 30;
  summary.getRange('E:E').format.columnWidth = 32;
  summary.getRange('F:F').format.columnWidth = 4;
  const presentation = model.presentation ?? {};
  const prose = [
    ['Lectura técnica', presentation.technical_text ?? ''], ['Lectura para cliente', presentation.use_text ?? ''],
    ['Base del análisis', presentation.basis ?? ''],
  ];
  let row = 10;
  for (const [label, text] of prose) {
    summary.getRange(`A${row}`).values = [[cellValue(label)]];
    summary.getRange(`A${row}:A${row}`).format = { fill: PALE, font: { bold: true, color: NAVY }, verticalAlignment: 'top', wrapText: true };
    summary.getRange(`B${row}:E${row}`).merge();
    summary.getRange(`B${row}`).values = [[cellValue(text)]];
    summary.getRange(`B${row}:E${row}`).format = { wrapText: true, verticalAlignment: 'top' };
    summary.getRange(`A${row}:E${row}`).format.rowHeight = estimateRowHeight([label, text], [24, 150], 48);
    row++;
  }
  summary.getRange(`A${row}:E${row}`).merge();
  summary.getRange(`A${row}`).values = [['Pasos del análisis']];
  summary.getRange(`A${row}:E${row}`).format = { fill: PALE, font: { bold: true, color: NAVY }, verticalAlignment: 'center', rowHeight: 24 };
  row++;
  const steps = rowsOf(presentation.steps).map(step => [step.order ?? '', step.action ?? '', step.basis ?? '', listText(step.case_ids ?? []), listText(step.missing ?? [])]);
  setBlock(summary, `A${row}:E${row}`, [['Orden', 'Acción', 'Fundamento', 'Casos', 'Pendiente']], HEADERS);
  row++;
  if (steps.length) {
    setBlock(summary, `A${row}:E${row + steps.length - 1}`, steps);
    summary.getRange(`A${row}:E${row + steps.length - 1}`).format = { wrapText: true, verticalAlignment: 'top' };
    applyAdaptiveHeights(summary, steps, [12, 44, 40, 30, 32], row);
    row += steps.length;
  }
  row++;
  const limitations = listText(presentation.limitations ?? []);
  summary.getRange(`A${row}`).values = [['Limitaciones']];
  summary.getRange(`A${row}`).format = { fill: PALE, font: { bold: true, color: NAVY }, verticalAlignment: 'top', wrapText: true };
  summary.getRange(`B${row}:E${row}`).merge();
  summary.getRange(`B${row}`).values = [[cellValue(limitations)]];
  summary.getRange(`B${row}:E${row}`).format = { wrapText: true, verticalAlignment: 'top' };
  summary.getRange(`A${row}:E${row}`).format.rowHeight = estimateRowHeight(['Limitaciones', limitations], [24, 150], 48);
  row++;
  row += 2;
  const summaryLastRow = row;

  const caseRows = clientCases.map(c => [c.case_id, c.title, c.observation, c.criterion, c.action, c.closure_criteria, c.impact_known, c.impact_potential, listText(c.limitations), c.entities_text, c.disposition_text, c.priority_text, c.producer_text, c.reaudit_text]);
  const baseCaseHeaders = ['ID caso', 'Caso', 'Observación', 'Criterio', 'Acción propuesta', 'Criterio de cierre', 'Impacto conocido', 'Impacto potencial', 'Limitaciones', 'Entidades afectadas', 'Disposición fuente', 'Prioridad fuente', 'Productor fuente', 'Reauditoría fuente'];
  const caseWidths = [18, 28, 42, 34, 42, 36, 28, 28, 34, 30, 22, 18, 24, 26, 22, 22, 38, 16];
  const caseData = addIdentityColumns(baseCaseHeaders, caseRows, identity);
  const caseSheet = addDataSheet(wb, 'Casos', caseData.headers, caseData.rows, caseWidths);
  applyAdaptiveHeights(caseSheet, caseData.rows, caseWidths);

  const pending = rowsOf(model.pending_records);
  const sidecarMetadata = Object.fromEntries(Object.entries(sidecar).filter(([key]) => key !== 'cases'));
  const occurrenceRecords = [];
  for (const item of sourceCases) {
    const caseId = readField(item, 'case_id', 'id');
    getOccurrences(item).forEach((occurrence, index) => {
      const source = occurrence && typeof occurrence === 'object' && !Array.isArray(occurrence) ? occurrence : { occurrence };
      occurrenceRecords.push({ _record_type: 'Ocurrencia', _case_id: caseId, _occurrence_index: index + 1, ...source });
    });
  }
  const metadataRecords = [
    ...(Object.keys(sidecarMetadata).length ? [{ _record_type: 'Metadatos del contrato', _contract_metadata: sidecarMetadata }] : []),
    ...sourceCases.map(item => ({ _record_type: 'Metadatos del caso', ...Object.fromEntries(Object.entries(item ?? {}).filter(([key]) => key !== 'occurrences')) })),
  ];
  const pendingRecords = pending.map(item => ({ _record_type: 'Pendiente', ...(item && typeof item === 'object' && !Array.isArray(item) ? item : { source_record: item }) }));
  const occurrenceData = recordRows([...occurrenceRecords, ...metadataRecords, ...pendingRecords]);
  const occurrenceLabels = { 'Índice': 'N.º registro', '_record_type': 'Tipo de registro', '_case_id': 'ID caso', '_occurrence_index': 'N.º ocurrencia', '_contract_metadata': 'Metadatos del contrato (JSON)' };
  const occ = { ...occurrenceData, headers: occurrenceData.headers.map(header => occurrenceLabels[header] ?? (header === 'Registro íntegro (JSON)' ? 'Registro íntegro (JSON)' : matrixFieldLabel(header))) };
  const baseOccWidths = occ.headers.map((header, index) => header.includes('(JSON)') ? 60 : index === 0 ? 14 : 24);
  const occData = addIdentityColumns(occ.headers, occ.rows, identity);
  const occWidths = [...baseOccWidths, 22, 22, 38, 16];
  const occurrenceSheet = addDataSheet(wb, 'Ocurrencias', occData.headers, occData.rows, occWidths);
  if (occData.rows.length) applyAdaptiveHeights(occurrenceSheet, occData.rows, occWidths);

  const followRows = clientCases.map(c => [c.case_id, c.title, c.producer_text, '', '', '', c.reaudit_text, '', '']);
  const baseFollowHeaders = ['ID caso', 'Caso', 'Estado del productor registrado', 'Respuesta del productor (editable)', 'Estado del productor (editable)', 'Responsable productor (editable)', 'Estado de verificación registrado', 'Revisión del auditor (editable)', 'Estado auditor (editable)'];
  const followWidths = [18, 28, 28, 40, 24, 28, 28, 42, 24, 22, 22, 38, 16];
  const followData = addIdentityColumns(baseFollowHeaders, followRows, identity);
  const followSheet = addDataSheet(wb, 'Seguimiento', followData.headers, followData.rows, followWidths);
  applyAdaptiveHeights(followSheet, followData.rows, followWidths);

  const matrixInput = rowsOf(model.matrix);
  const objectMatrix = matrixInput.length > 0 && matrixInput.every(item => item && typeof item === 'object' && !Array.isArray(item));
  let matrixRows;
  let matrixHeaders;
  if (objectMatrix) {
    const detailKeys = [...new Set(matrixInput.flatMap(item => Object.keys(item).filter(key => !['rule_id', 'rule', 'stage', 'status'].includes(key))))];
    matrixHeaders = ['Regla', 'Etapa', 'Resultado', ...detailKeys.map(matrixFieldLabel), 'Detalles (JSON)'];
    matrixRows = matrixInput.map(item => [item.rule_id ?? item.rule ?? '', item.stage ?? '', item.status ?? '', ...detailKeys.map(key => item[key] ?? ''), JSON.stringify(item)]);
  } else {
    matrixRows = matrixInput.length && matrixInput.every(item => !Array.isArray(item))
      ? [matrixInput.map(cellValue)]
      : matrixInput.map(item => Array.isArray(item) ? item : [JSON.stringify(item)]);
    matrixHeaders = rowsOf(model.matrix_headers).length ? model.matrix_headers : (matrixRows[0]?.map((_, i) => `Campo ${i + 1}`) ?? ['Matriz']);
  }
  const baseMatrixWidths = matrixHeaders.map((header, index) => index === matrixHeaders.length - 1 ? 60 : index < 3 ? 24 : 30);
  const matrixWidths = [...baseMatrixWidths, 22, 22, 38, 16];
  const matrixData = addIdentityColumns(matrixHeaders, matrixRows, identity);
  const matrixSheet = addDataSheet(wb, 'Matriz', matrixData.headers, matrixData.rows, matrixWidths);
  applyAdaptiveHeights(matrixSheet, matrixData.rows, matrixWidths);

  const evidenceRows = [];
  for (const c of clientCases) for (const e of rowsOf(c.evidence)) {
    const evidenceText = typeof e === 'string' ? e : '';
    evidenceRows.push([c.case_id, c.title, readField(e, 'evidence_id', 'id'), typeof e === 'string' ? 'Evidencia' : readField(e, 'title', 'name'), evidenceText || readField(e, 'reference', 'path', 'uri'), typeof e === 'string' ? '' : readField(e, 'description', 'note'), JSON.stringify(e)]);
  }
  const evidenceWidths = [18, 28, 22, 34, 48, 48, 60];
  const evidenceData = addIdentityColumns(['ID caso', 'Caso', 'ID evidencia', 'Evidencia', 'Referencia', 'Descripción', 'Registro íntegro (JSON)'], evidenceRows, identity);
  const evidenceAllWidths = [...evidenceWidths, 22, 22, 38, 16];
  const evidenceSheet = addDataSheet(wb, 'Evidencias', evidenceData.headers, evidenceData.rows, evidenceAllWidths);
  applyAdaptiveHeights(evidenceSheet, evidenceData.rows, evidenceAllWidths);

  wb.recalculate();
  await fs.mkdir(path.dirname(outputPath), { recursive: true });
  const xlsx = await SpreadsheetFile.exportXlsx(wb);
  await xlsx.save(outputPath);

  if (qaDir) {
    await fs.mkdir(qaDir, { recursive: true });
    const renders = [
      ['Resumen', `A1:E${summaryLastRow}`],
      ['Ocurrencias', `A1:${colName(Math.min(8, occ.headers.length))}${Math.min(8, occ.rows.length + 1)}`],
      ['Seguimiento', `A1:I${Math.min(8, Math.max(2, followRows.length + 1))}`],
      ['Matriz', `A1:C${Math.min(13, Math.max(2, matrixRows.length + 1))}`],
      ['Evidencias', `A1:G${Math.min(8, Math.max(2, evidenceRows.length + 1))}`],
    ];
    for (const [sheetName, range] of renders) {
      const image = await wb.render({ sheet: sheetName, range, format: 'png', scale: 1.5 });
      await fs.writeFile(path.join(qaDir, `${sheetName}.png`), Buffer.from(await image.arrayBuffer()));
    }
    for (const [name, range] of [
      ['Casos_A-F.png', `A1:F${Math.min(8, Math.max(2, caseRows.length + 1))}`],
      ['Casos_G-N.png', `G1:N${Math.min(8, Math.max(2, caseRows.length + 1))}`],
      ['Matriz_A-C_14-25.png', `A14:C${Math.min(25, Math.max(14, matrixRows.length + 1))}`],
    ]) {
      const sheet = name.startsWith('Matriz_') ? 'Matriz' : 'Casos';
      const image = await wb.render({ sheet, range, format: 'png', scale: 1.5 });
      await fs.writeFile(path.join(qaDir, name), Buffer.from(await image.arrayBuffer()));
    }
  }
}

main().catch(error => { console.error(`Error: ${error?.stack ?? error}`); process.exitCode = 1; });
