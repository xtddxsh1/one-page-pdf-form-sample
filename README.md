# One-page PDF form production sample

This is an original, fictional production sample by Tong Xiao. It is not client work.

- [Download the interactive PDF](fillable-sample.pdf)
- [Original static PDF](source-static.pdf)
- [Saved test values](saved-values-check.pdf)
- [Preview of saved values](saved-values-check.png)
- [Verification results](test-results.json)

The workflow adds nine AcroForm fields to an existing one-page static PDF while retaining its original page content: six short text fields, two checkboxes and one multiline field. All example names and contact details are fictional.

## Verified on 28 September 2026

The files were generated with ReportLab 4.4.9 and pypdf 6.9.2. Tests reopened the saved PDF and checked all nine values in both the canonical field tree and page widgets, unique field names, appearance streams, page count and unchanged extracted static text. Blank and filled versions were rendered with Poppler 26.07.0 and visually reviewed.

This verifies this small sample. It does not claim universal PDF-viewer compatibility, Adobe Acrobat UI testing, PDF/UA accessibility certification or digital-signature support. A customer project requires its source file and target viewer before scope is confirmed.

## Reproduce

Install the free Python packages listed in requirements.txt, then run:

```text
python build_sample.py
pdftoppm -png -singlefile saved-values-check.pdf saved-values-check
```

The PDF can be filled in a compatible PDF viewer. Download it first; GitHub's document preview is not an interactive form editor.

## Pilot scope

Proposed price: USD 15 for one supplied, unsigned English PDF page with up to ten ordinary text or checkbox fields, preserving the existing wording and layout. Deliverables: interactive PDF, a field map and a saved test copy. One consolidated revision within that scope.

Timing: first version within two business days of a mutually agreed start, after the source, fields, target viewer, authorized workflow and payment arrangement are confirmed. The proposed fee is payable after written acceptance; payment date, method, currency and fees must be agreed before work begins.

Translation, document certification, signatures, calculations, OCR and native Word/InDesign/AutoCAD source editing require a separate scope and are not included.

All public files here are the same reusable sample. No customer files are published.

