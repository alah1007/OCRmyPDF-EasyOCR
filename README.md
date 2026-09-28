# OCRmyPDF-EasyOCR: searchable PDFs

This project integrates [EasyOCR](https://github.com/JaidedAI/EasyOCR) with OCRmyPDF and provides a simple command, `pdf-ocr`, for making scanned PDFs searchable. English (`eng`) is the default OCR language. Choose other languages with `--languages`; for example, `eng+fra` for English and French.

The integration is experimental. EasyOCR handles OCR, while OCRmyPDF builds the searchable PDF. Tesseract is still required for some OCRmyPDF operations, including page-orientation detection; this plugin uses OpenCV for deskewing.

## Install

Install [PyTorch for your operating system and hardware](https://pytorch.org/) first. Then install OCRmyPDF-EasyOCR into that same Python environment:

```bash
pip install git+https://github.com/alah1007/OCRmyPDF-EasyOCR.git
```

The `pdf-ocr` command uses CPU by default so it also works without a supported GPU. EasyOCR's PyTorch models may be downloaded the first time it runs.

## Use

Create an English-searchable PDF:

```bash
pdf-ocr scan.pdf searchable.pdf
```

Choose another language, save the recognized text to a UTF-8 sidecar, and optionally correct skew or page orientation:

```bash
pdf-ocr scan.pdf searchable.pdf --languages eng+fra --sidecar recognized.txt --deskew --rotate-pages
```

To enable EasyOCR GPU mode, add `--gpu` (install a compatible PyTorch/CUDA setup first). Page-orientation detection relies on Tesseract; deskewing uses OpenCV. For advanced OCRmyPDF options, the equivalent direct command is:

```bash
ocrmypdf --plugin ocrmypdf_easyocr --output-type pdf -l eng --easyocr-no-gpu scan.pdf searchable.pdf
```

If [Celery multiprocessing](https://docs.celeryq.dev/en/stable/getting-started/introduction.html) is installed in the environment, the plugin uses it instead of standard Python multiprocessing; this supports deployments such as paperless-ngx.

## Troubleshooting

- If the `ocrmypdf` command is missing, install OCRmyPDF in the same environment.
- EasyOCR model files are downloaded on first use; allow network access for that first run or install the model files in EasyOCR's configured model directory.
- The plugin is experimental and does not yet match every OCRmyPDF/Tesseract feature. Review OCR output, especially reading order and text extraction.

## Development

Install the `test` extra and run `pytest`. CLI tests verify command construction and error handling; they do not measure recognition accuracy on real-world scans.
