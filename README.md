# On the Links Public Claim-to-Evidence Evaluation OS

[![Machine Verification](https://github.com/GhostDriftTheory/onzalinx-evaluation-os/actions/workflows/verify-and-pages.yml/badge.svg?branch=main)](https://github.com/GhostDriftTheory/onzalinx-evaluation-os/actions/workflows/verify-and-pages.yml)

> ### ▶ [View the Evaluation Summary](https://ghostdrifttheory.github.io/onzalinx-evaluation-os/)
>
> **ROBUST / PUBLIC_ALIGNMENT_ESTABLISHED — Guaranteed Lower Bound: 70.0**

This repository provides a public implementation for evaluating the **alignment between the publicly stated principles and publicly observable actions of On the Links Co., Ltd.**

The evaluation combines fixed investigation obligations, source-bound evidence intervals, multiple admissible evaluation conditions, cryptographic hash binding, and certificate-based semantic replay.

The case-study reports are currently provided in Japanese. The implementation itself is fully reproducible with Python 3.11+ using only the standard library.

## Result

* Decision: **ROBUST / PUBLIC_ALIGNMENT_ESTABLISHED**
* Score Envelope: **70.0–88.6875**
* Strict Establishment Line: **68.0**
* Guaranteed Lower Bound: **70.0**
* Evaluation Families: **60**
* Investigation Gate: **32 / 32 CLOSED**

This does **not** mean that On the Links is “a 70-point company.”

It means that, within the explicitly declared evaluation universe, the conclusion that its **publicly stated principles and publicly observable actions are aligned does not reverse** when admissible evidence interpretations, criterion weights, decision thresholds, and interval uncertainty are varied.

## Relationship Between Evaluator and Evaluated Entity

GhostDrift Mathematical Institute, which designed and conducted this evaluation, is a **strategic partner of On the Links and a party to their joint AI-assurance implementation activities**.

This evaluation is therefore **not an independent third-party audit**.

Rather than concealing that relationship, the implementation places the basis for trust in explicit and reproducible controls:

1. Human-authored evidence intervals are disclosed together with their sources, descriptions, independence classifications, and limitations.
2. The fixed evaluation universe is cryptographically bound so that input substitution can be detected.
3. Numerical finality is blocked unless the investigation gate—including uncontrolled-source review and adverse-evidence candidate disposition—has been closed.
4. Once the inputs are fixed, all admissible mappings, criterion weights, thresholds, reference frames, and interval completions are evaluated.
5. The investigation gate and numerical evaluation can be fully recomputed from the generated certificate.

## Evidence Intervals

Evidence intervals are **not machine-generated objective scores**.

They are human-authored **integer ordinal intervals from 0 to 4**, assigned after reviewing public sources against the dimension anchors defined in the implementation.

Evaluation OS does not claim that each interval is the uniquely correct interpretation.

Instead, it makes those judgments explicit and machine-checkable. The implementation rejects evidence intervals without sources, intervals without stated limitations, and non-integer interval boundaries.

Any change to an evidence interval changes the Fixed Evaluation Universe Hash and the generated certificate, requiring the entire evaluation-family universe to be recomputed.

## Public Artifacts

The public deliverables are intentionally limited to three core artifacts:

| File                            | Purpose                                                                                                        |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `①評価OS評価レポートまとめ（オンザリンクス社）.html` | Human-readable evaluation summary and GitHub Pages landing page                                                |
| `②評価OS詳細レポート（オンザリンクス社）.md`      | Authoritative report covering methodology, evidence, results, evaluator relationship, and assurance boundaries |
| `③評価OS実施コード（オンザリンクス社）.py`       | Evaluation OS 1.2.0-final implementation, certificate generation, and semantic replay                          |

Repository-operation files are also intentionally minimal: `README.md`, `.gitignore`, and a single GitHub Actions workflow.

Generated certificate JSON files and duplicate reports are not committed to the repository.

## Local Reproduction

Requires Python 3.11+ and uses only the Python standard library.

```bash
python -S "③評価OS実施コード（オンザリンクス社）.py" evaluate
python -S "③評価OS実施コード（オンザリンクス社）.py" self-test
python -S "③評価OS実施コード（オンザリンクス社）.py" certificate > certificate.json
python -S "③評価OS実施コード（オンザリンクス社）.py" verify certificate.json
python -S "③評価OS実施コード（オンザリンクス社）.py" freeze
```

## Machine Verification in CI

`.github/workflows/verify-and-pages.yml` runs on pushes to `main`, pull requests, and manual execution.

It verifies:

* **23 built-in self-tests**
* Byte-for-byte determinism across two independently generated certificates
* Certificate Payload Hash and Semantic Replay
* Engine Version, Schema, and Python code SHA-256
* Fixed Evaluation Universe, Investigation Template, Source Register, Review Records, and Prospective Charter hashes
* Core results including 60 evaluation families, Guaranteed Lower Bound 70.0, passage of the Strict 68.0 line, and Investigation Gate 32 / 32 closure
* Machine-readable disclosure of the evaluator relationship and the fact that this is not an independent third-party audit
* The policy that evidence intervals are human-authored, source-bound, and integer-valued from 0 to 4
* Consistency of displayed hashes, versions, results, and disclosures across the Markdown report and HTML summary

Only after successful machine verification are the HTML summary, detailed report, implementation code, CI-generated certificate, and SHA-256 manifest assembled into the GitHub Pages artifact.

## Minimal Publication Procedure

Create an empty public GitHub repository and push the complete `onzalinx-evaluation-os` directory as provided.

```bash
git init
git add .
git commit -m "Publish On the Links Evaluation OS 1.2"
git branch -M main
git remote add origin <YOUR_REPOSITORY_URL>
git push -u origin main
```

## GitHub Pages

After creating the repository, go to:

**Settings → Pages → Build and deployment → Source**

and select:

**GitHub Actions**

A push to `main` will publish the HTML evaluation summary only after machine verification succeeds.

## Recommended Repository Protection

Protect `main` using a GitHub Ruleset or branch-protection rule and require successful `Machine verification` before merge.

This prevents isolated changes to the code, report, or displayed evaluation result from entering `main` without the corresponding cryptographic and semantic consistency checks passing.

## Assurance Boundary

This evaluation is a `RETROSPECTIVE_TRANSPARENT_PILOT`.

It does **not** guarantee:

* That each evidence interval is the uniquely correct interpretation
* Independent third-party auditing or evaluator neutrality
* The truth of the underlying public statements themselves
* Exhaustive coverage of the entire Web, private information, deleted information, or unindexed information
* Prospective Temporal Blind Commitment for this retrospective run
* Trusted external timestamps, signer identity, or non-repudiation
* Population-wide customer outcomes, realized ROI, internalization rates, workplace conditions, or commercial-scale adoption

The evaluation instead provides a transparent and reproducible answer to a narrower question:

> **Given the declared public-evidence universe and explicitly bounded human judgments, does the evaluation conclusion remain invariant across all admissible evaluation conditions?**

For this case study, the answer is **ROBUST**.

## Rights and Patent Notice

Copyright © 2026 GhostDrift Mathematical Institute. All rights reserved.

**No open-source license is granted for the source code or other materials in this repository.**

Public availability for inspection, reproducibility, and technical verification does not grant permission to reproduce, redistribute, modify, incorporate the materials into other products or services, or use them commercially.

Any such use requires prior written permission from the rights holder.

This repository implements techniques related to **Japanese Patent Application No. 2026-190686**, filed August 20, 2026.

**No patent license is granted by publication of this repository.**
