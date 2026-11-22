# Synthetic telemetry export context

The interactive lab exports its existing CSV and a matching `.metadata.json` sidecar. Export the CSV first; the adjacent context button starts disabled and then downloads metadata for the last CSV exported. If you change any inputs, export a new CSV before downloading its context JSON. Keep the matching pair together when sharing or archiving the data.

The CSV keeps its established header and column order. The sidecar records the matching CSV filename, ordered header, delimiter and line ending, sample count, unit for each column, selected model, current input values, assumptions, calibration status, and synthetic provenance. Its `schema_version` identifies the context contract; the CSV columns remain unchanged for existing readers.

Units come from the selected model specification and describe its synthetic quantities. They do not imply measured values, empirical calibration, or physical validation. The source package revision in the sidecar identifies the browser-lab package snapshot; it is not the deployed Pages revision. This lab does not parse project records, establish evidence acceptance, run the native toolkit, or authorize operations.

Automated export assertions exercise the same serializer used by the page and verify that the current default CSV remains byte-for-byte compatible with the captured production export.
