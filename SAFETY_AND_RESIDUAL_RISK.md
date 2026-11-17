# BESS QA/QC Toolkit — Safety and Residual Risk Specification

**Document Class:** Engineering Governance & Safety Boundary Notice  
**Scope:** BESS QA/QC Toolkit (Software, Scripts, and Templates)  
**Evaluation Date:** 2026-11-17  

---

## 1. Non-Negotiable Safety Boundary

> [!CAUTION]
> **This software toolkit is an engineering documentation, evidence traceability, and decision-support system. It is NOT an engineering authority, an automated energization permit, an interlock bypass mechanism, or a certified safety system.**

### Boundary Rules
1. **No Automated Permission to Energize:** Under no circumstances shall an automated software "PASS" result from `audit_readiness.py`, `audit_punch_list.py`, or any other script be interpreted, cited, or utilized as authority to energize electrical equipment, close breakers, operate high-voltage circuits, or declare a BESS commercially operational.
2. **Authorized Human Engineering Sign-off Required:** All physical testing, switching, energization, commissioning, and handover activities require formal, documented sign-off by appropriately licensed, accredited, and authorized human engineering and safety professionals (e.g., Professional Engineers, Site Safety Officers, Commissioning Managers, Utility Interconnection Leads).
3. **Traceability, Not Invention:** The toolkit verifies the presence, consistency, structure, and traceability of documented approval records. The toolkit and automated agents must never fabricate approvals, invent witness signatures, or synthesize test results.

---

## 2. Invariant Rules for Software Readiness Decisions

The following invariants are implemented and enforced across all toolkit scripts:

- **Invariant 1 — Fail Closed on Safety-Critical Prerequisites:**  
  Missing, ambiguous, malformed, or contradictory safety-critical evidence (e.g. fire alarm interface, emergency shutdown, protection settings, calibration certificates) causes an immediate failure of the automated gate.
- **Invariant 2 — Separate Software Validation from Operational Approval:**  
  A software report indicates only that documented policy criteria were satisfied. It cannot grant operational authorization.
- **Invariant 3 — Critical Defects Remain Blocking:**  
  Critical defects affecting personnel safety, electrical protection, fire safety, or grid compliance can never be made non-blocking through routine deferral or status reassignment.
- **Invariant 4 — Closed Means Independently Verified:**  
  Owner self-acknowledgment (e.g., "completed", "done", "fixed") is insufficient to close a defect. Independent retest, witness sign-off, or approved verification evidence is mandatory.
- **Invariant 5 — Deferred Means Explicitly Risk-Accepted:**  
  A deferred defect requires an authorized residual-risk acceptance record with an identified owner, technical justification, interim controls, and target close date.
- **Invariant 6 — Preserve Evidence Provenance:**  
  All policy outcomes are traced directly to controlled document IDs, revisions, dates, and locations.
- **Invariant 7 — Unknown is Not Pass:**  
  Unverifiable links, missing certificates, or unconfirmed signatures are treated as unverified, never as passing.
- **Invariant 8 — Deterministic Acceptance Decisions:**  
  Identical controlled inputs, policies, and evaluation dates must produce bit-identical audit outputs.
- **Invariant 9 — Maintain Source and Policy Compatibility:**  
  Policy rules are explicit and auditable; existing records are not silently reinterpreted.
- **Invariant 10 — Never Fabricate Engineering Records:**  
  Synthetic test results, signatures, measurements, or logs must never be represented as genuine site acceptance records.

---

## 3. Real-World Engineering Considerations & Operational Residual Risks

Software validation checks evidence structure, but cannot independently inspect physical reality. The following operational considerations require on-site engineering verification:

### 3.1 Arc Flash and High-Voltage Electrical Safety
- Physical verification of personal protective equipment (PPE) compliance, arc-flash boundary markings, lockout/tagout (LOTO) execution, and voltage-detection procedures before equipment contact.
- Inspection of torque marks, cable bend radii, insulation resistance, and ground-fault interrupters.

### 3.2 Fire Detection, Suppression, and Thermal Runaway Interfaces
- Physical verification of gaseous suppression cylinder weights, agent release nozzles, pressure relief dampers, and air intake shutdown dampers.
- Witnessing of cause-and-effect interlocks between battery management system (BMS) cell temperature thresholds, off-gas detection, fire alarm control panels (FACP), ventilation controls, and shunt-trip breakers.

### 3.3 Protection Coordination and Relay Settings
- Injection testing of protective relays using calibrated secondary injection test sets (e.g., Omicron) to verify pickup thresholds, clearing times, and instantaneous overcurrent/ground fault curves against approved protection coordination studies.
- Verification that relay firmware versions and uploaded setting files match the stamped engineering study.

### 3.4 Grid Interconnection and Interoperability
- Verification of utility witness testing, anti-islanding protection, low-voltage ride-through (LVRT), high-voltage ride-through (HVRT), frequency response, and active/reactive power ramp limits under local grid-code rules.
- Confirmation of revenue metering accuracy, instrument transformer (CT/VT) ratios, and polarity checks.

### 3.5 Cyber Asset and Communication Handover
- Verification of network segmentation, firewall rules, default password retirement, encrypted telemetry (e.g., DNP3 Secure, IEC 61850), and backup restoration before handover.

---

## 4. Responsibility Matrix

| Responsibility | Toolkit Software Scope | Authorized Engineering Role Scope |
|---|---|---|
| Evidence Format & Structure Validation | **Responsible** (Automated checks) | Reviewer |
| Cross-Register Traceability Verification | **Responsible** (Automated checks) | Reviewer |
| Deadline & Expiry Checking | **Responsible** (Automated checks) | Reviewer |
| Physical Installation Inspection | Out of Scope | **Responsible** (Field QA/QC Inspector) |
| Electrical Test Execution & Measurement | Out of Scope | **Responsible** (Commissioning Technician) |
| Protection Setting Approval | Out of Scope | **Responsible** (Lead Protection Engineer) |
| Energization Permission | Out of Scope | **Responsible** (Authorized Switching Director) |
| Commercial Handover Acceptance | Out of Scope | **Responsible** (Asset Owner / Offtaker Representative) |
