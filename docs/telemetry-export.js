(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.BessTelemetryExport = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  function buildTelemetryExport({ fileName, repository, source, model, parameterSpecs, metrics, params, series }) {
    if (typeof fileName !== 'string' || !fileName.endsWith('.csv')) throw new TypeError('fileName must end in .csv');
    if (!Array.isArray(parameterSpecs) || !Array.isArray(metrics) || !Array.isArray(series)) {
      throw new TypeError('parameterSpecs, metrics, and series must be arrays');
    }

    const timeUnit = model.timeUnit;
    const header = ['model_time_' + timeUnit, ...metrics.map(metric => metric.key), ...parameterSpecs.map(parameter => 'input_' + parameter.key)];
    const lines = [header.join(',')];
    series.forEach(sample => {
      lines.push([sample.time, ...metrics.map(metric => sample[metric.key]), ...parameterSpecs.map(parameter => params[parameter.key])]
        .map(value => Number(value).toPrecision(12))
        .join(','));
    });
    const csv = lines.join('\r\n') + '\r\n';

    const columns = [
      { name: header[0], role: 'model_time', label: 'Model time', unit: timeUnit },
      ...metrics.map(metric => ({ name: metric.key, role: 'model_metric', label: metric.label, unit: metric.unit })),
      ...parameterSpecs.map(parameter => ({ name: 'input_' + parameter.key, role: 'scenario_input', label: parameter.label, unit: parameter.unit }))
    ];
    const contextFileName = fileName.replace(/\.csv$/i, '.metadata.json');
    const context = {
      format: 'bess-synthetic-telemetry-context',
      schema_version: '1.0',
      artifact: {
        csv_file: fileName,
        media_type: 'text/csv;charset=utf-8',
        sample_count: series.length
      },
      export_contract: {
        version: '1.0',
        delimiter: ',',
        line_ending: 'CRLF',
        numeric_representation: 'JavaScript Number.toPrecision(12)',
        header
      },
      columns,
      provenance: {
        classification: 'synthetic',
        deterministic: true,
        model_kind: model.kind,
        model_title: model.title,
        calibration_status: model.calibration_status || 'Uncalibrated synthetic teaching proxy',
        source_package_revision: source.commit,
        source_package_url: source.url,
        source_package_calibration_status: source.calibration_status,
        source_package_scope: source.scope,
        revision_semantics: 'source_package_revision identifies the reconciled browser-lab package source; it is not the deployed site revision.'
      },
      scenario: {
        time_unit: timeUnit,
        horizon: model.horizon,
        parameters: parameterSpecs.map(parameter => ({
          key: parameter.key,
          label: parameter.label,
          value: params[parameter.key],
          unit: parameter.unit
        }))
      },
      assumptions: Array.from(new Set(model.assumptions || [])),
      interpretation: model.introduction || 'Synthetic browser teaching output; see the model assumptions below.',
      limitations: [
        'Values are deterministic synthetic teaching output, not measured telemetry, project evidence, or operational records.',
        'The browser lab does not execute the repository native engine, validate project evidence, establish acceptance, or authorize operations.',
        'Declared units describe model quantities; they do not establish empirical calibration or physical validation.'
      ],
      repository: {
        name: repository.name || repository.slug,
        url: repository.url
      }
    };

    return {
      csvFileName: fileName,
      csv,
      contextFileName,
      contextJson: JSON.stringify(context, null, 2) + '\n'
    };
  }

  function createTelemetryExportActions(buildExport, download) {
    if (typeof buildExport !== 'function' || typeof download !== 'function') {
      throw new TypeError('buildExport and download must be functions');
    }
    let lastExport = null;
    return Object.freeze({
      hasExportedCsv: () => lastExport !== null,
      exportCsv: () => {
        lastExport = buildExport();
        download(lastExport.csvFileName, lastExport.csv, 'text/csv;charset=utf-8');
        return lastExport;
      },
      exportContext: () => {
        if (!lastExport) return null;
        download(lastExport.contextFileName, lastExport.contextJson, 'application/json;charset=utf-8');
        return lastExport;
      }
    });
  }

  return Object.freeze({ buildTelemetryExport, createTelemetryExportActions });
});
