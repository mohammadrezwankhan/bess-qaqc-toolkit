'use strict';

const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const { buildTelemetryExport, createTelemetryExportActions } = require('../docs/telemetry-export.js');

const root = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'docs', 'index.html'), 'utf8');
const configMatch = html.match(/<script id="lab-config" type="application\/json">([\s\S]*?)<\/script>/);
assert.ok(configMatch, 'the production page exposes its embedded lesson configuration');
const config = JSON.parse(configMatch[1]);

const securityAssumptions = [
  'Synthetic alert counts model staffing and defensive workflow capacity.',
  'Automatic resolution is assumed correct; precision, recall, false positives, and severity are not modeled.',
  'All analysts have the same throughput and begin with an empty queue.'
];
const parameters = {
  alertRate: 20,
  analystCount: 3,
  reviewRate: 4,
  automationPct: 40
};
const series = [
  { time: 0, backlog: 0, coveragePct: 100, reviewedAlerts: 0, workloadPct: 100 },
  { time: 60, backlog: 0, coveragePct: 100, reviewedAlerts: 1200, workloadPct: 100 }
];

const output = buildTelemetryExport({
  fileName: `${config.repository.slug}-synthetic-telemetry.csv`,
  repository: config.repository,
  source: config.source,
  model: {
    ...config.model,
    title: config.model.title,
    timeUnit: config.model.timeUnit,
    horizon: config.model.horizon,
    assumptions: [...securityAssumptions, ...config.model.assumptions]
  },
  parameterSpecs: config.model.parameters,
  metrics: config.model.metrics,
  params: parameters,
  series
});

const expectedHeader = 'model_time_min,backlog,coveragePct,reviewedAlerts,workloadPct,input_alertRate,input_analystCount,input_reviewRate,input_automationPct';
const csvLines = output.csv.trimEnd().split('\r\n');
assert.equal(output.csvFileName, 'bess-qaqc-toolkit-synthetic-telemetry.csv');
assert.equal(output.contextFileName, 'bess-qaqc-toolkit-synthetic-telemetry.metadata.json');
assert.equal(csvLines[0], expectedHeader, 'the established CSV header and column order remain stable');
assert.equal(csvLines.length, 3, 'one header and each supplied sample are serialized');
assert.equal(csvLines[1], '0.00000000000,0.00000000000,100.000000000,0.00000000000,100.000000000,20.0000000000,3.00000000000,4.00000000000,40.0000000000');
assert.equal(csvLines[2], '60.0000000000,0.00000000000,100.000000000,1200.00000000,100.000000000,20.0000000000,3.00000000000,4.00000000000,40.0000000000');

const metadata = JSON.parse(output.contextJson);
assert.equal(metadata.schema_version, '1.0');
assert.equal(metadata.artifact.csv_file, output.csvFileName);
assert.equal(metadata.artifact.sample_count, 2);
assert.equal(metadata.export_contract.delimiter, ',');
assert.equal(metadata.export_contract.line_ending, 'CRLF');
assert.deepEqual(metadata.export_contract.header, expectedHeader.split(','));
assert.deepEqual(metadata.columns.map(column => column.name), expectedHeader.split(','));
assert.equal(metadata.provenance.classification, 'synthetic');
assert.equal(metadata.provenance.model_kind, 'security');
assert.equal(metadata.provenance.calibration_status, 'Uncalibrated synthetic teaching proxy');
assert.equal(metadata.provenance.source_package_revision, 'b025120d9d317df682d48b4ad3ccb88acf3875e9');
assert.match(metadata.provenance.revision_semantics, /package source/i);
assert.equal(metadata.columns[0].unit, 'min');
assert.equal(metadata.columns.find(column => column.name === 'coveragePct').unit, '%');
assert.equal(metadata.columns.find(column => column.name === 'backlog').unit, 'findings');
assert.equal(metadata.scenario.parameters.find(parameter => parameter.key === 'automationPct').value, 40);
assert.ok(metadata.assumptions.includes(securityAssumptions[1]));
assert.ok(metadata.assumptions.includes('A cleared queue cannot substitute for evidence traceability, valid calibration periods, signed residual-risk acceptance, or energization authorization.'));
assert.ok(metadata.limitations.some(limit => /not measured telemetry, project evidence, or operational records/i.test(limit)));

const modelScriptMatch = html.match(/<script>(\/\* Offline teaching models[\s\S]*?)<\/script>/);
assert.ok(modelScriptMatch, 'the production page embeds its deterministic teaching model');
const modelSandbox = {};
vm.runInNewContext(modelScriptMatch[1], modelSandbox);
const modelApi = modelSandbox.LabSimulation;
const fullSeries = Array.from({ length: 241 }, (_, index) => {
  const time = config.model.horizon * index / 240;
  return { time, ...modelApi.evaluateModel(config.model.kind, parameters, time) };
});
const fullOutput = buildTelemetryExport({
  fileName: `${config.repository.slug}-synthetic-telemetry.csv`,
  repository: config.repository,
  source: config.source,
  model: { ...config.model, assumptions: [...securityAssumptions, ...config.model.assumptions] },
  parameterSpecs: config.model.parameters,
  metrics: config.model.metrics,
  params: parameters,
  series: fullSeries
});
assert.equal(fullOutput.csv.split('\r\n').length, 243, 'the complete 241-sample model remains one header plus 241 rows');
assert.equal(crypto.createHash('sha256').update(fullOutput.csv, 'utf8').digest('hex'), 'd7312e007935f8f3daa85445dea55cbda1f61c2f62f270a23634424c49348ab7', 'the fourth-module preset bytes remain backwards compatible');

const buildForInputs = currentParams => buildTelemetryExport({
  fileName: `${config.repository.slug}-synthetic-telemetry.csv`,
  repository: config.repository,
  source: config.source,
  model: { ...config.model, assumptions: [...securityAssumptions, ...config.model.assumptions] },
  parameterSpecs: config.model.parameters,
  metrics: config.model.metrics,
  params: currentParams,
  series: Array.from({ length: 241 }, (_, index) => {
    const time = config.model.horizon * index / 240;
    return { time, ...modelApi.evaluateModel(config.model.kind, currentParams, time) };
  })
});
let activeParams = { ...parameters };
const downloads = [];
const actions = createTelemetryExportActions(
  () => buildForInputs(activeParams),
  (name, contents, mediaType) => downloads.push({ name, contents, mediaType })
);
assert.equal(actions.hasExportedCsv(), false, 'context is unavailable until a CSV has been exported');
assert.equal(actions.exportContext(), null, 'an initial context click cannot create unpaired metadata');
const firstExport = actions.exportCsv();
assert.equal(actions.hasExportedCsv(), true);
activeParams = { ...activeParams, automationPct: 80 };
const changedScenario = buildForInputs(activeParams);
assert.notEqual(changedScenario.contextJson, firstExport.contextJson);
const pairedContext = actions.exportContext();
assert.equal(pairedContext.contextJson, firstExport.contextJson, 'context after changing inputs still describes the last CSV');
assert.equal(downloads[1].name, firstExport.contextFileName);
assert.equal(JSON.parse(downloads[1].contents).scenario.parameters.find(parameter => parameter.key === 'automationPct').value, 40);
const secondExport = actions.exportCsv();
actions.exportContext();
assert.equal(JSON.parse(downloads[3].contents).scenario.parameters.find(parameter => parameter.key === 'automationPct').value, 80, 'a fresh CSV refreshes the matching context');
assert.equal(downloads[2].contents, secondExport.csv);

process.stdout.write('Telemetry CSV and context contract assertions passed.\n');
