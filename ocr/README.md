# Using the OCR service


## OCR Screenshot Client

```bash
python run_on_screenshots.py
```

This script will detect any new screenshots and attempt to run trained OCR on it. Modify the global variables as appropriate to your system for this to work properly. Can switch between our local translation model or Google Translate. Requires Imagemagick.

To train the OCR language, use JackyFont from fonts/ and follow the instructions located at https://github.com/tesseract-ocr/tesseract/wiki/TrainingTesseract-4.00

## OCR Metrics

```bash
python test_tesseract.py
```

This script will return the CER for the games we've labeled.