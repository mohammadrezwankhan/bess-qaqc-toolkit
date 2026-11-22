# Synthetic telemetry export context

The interactive lab exports its existing CSV and a matching `.metadata.json` sidecar. Export the CSV first; the adjacent context button starts disabled and then downloads metadata for the last CSV exported. If you change any inputs, export a new CSV before downloading its context JSON. Keep the matching pair together when sharing or archiving the data.

The CSV keeps its established header and column order. The sidecar records the matching CSV filename, ordered header, delimiter and line ending, sample count, unit for each column, selected model, current input values, assumptions, calibration status, and synthetic provenance. Its `schema_version` identifies the context contract; the CSV columns remain unchanged for existing readers.

Units come from the selected model specification and describe its synthetic quantities. They do not imply measured values, empirical calibration, or physical validation. The source package revision in the sidecar identifies the browser-lab package snapshot; it is not the deployed Pages revision. This lab does not parse project records, establish evidence acceptance, run the native toolkit, or authorize operations.

Automated export assertions exercise the same serializer used by the page and verify that the 241-row fourth-module preset remains byte-for-byte compatible with its captured production export (SHA-256 `d7312e007935f8f3daa85445dea55cbda1f61c2f62f270a23634424c49348ab7`). That fixture is not the default scenario. Independent live-browser verification also confirmed that the current default CSV matches its earlier bytes (SHA-256 `3e4be8207d9b05208817267d0bdbb7a651450c64e1b5360ab9b8b07e50622ff1`) and that the downloaded context matches the CSV exported before inputs were changed.
