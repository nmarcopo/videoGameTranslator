# Video Game Real-time Translator
## Nicholas Marcopoli (nmarcopo), Chan Hee (Luke) Song (csong1)

## Requirements

- Python >= 3.6
- Imagemagick [Download Page](https://imagemagick.org/script/download.php)
- Tesseract >= 4.0.0 [Installation Guide](https://github.com/tesseract-ocr/tesseract/wiki)

For MAC (using homebrew):
```
brew install imagemagick
brew install tesseract
```

Install other requirements with `pip`:

```bash
pip install -r requirements.txt
```

Download translation model from 
[here](https://drive.google.com/file/d/1BtgfuH9MvbE3Fd4s-t6cgKTFwgAw4vHb/view?usp=sharing)

```
tar -xvf translation_model.tar.gz
mv translation_model videoGameTranslator/full_system/
```
 


## Full System

To run the full system:

Edit global variables in `full_system/scripts/run_on_screenshots.py`

1. change `tesseract_binary` to correctly point to your tesseract binary
  * For MAC, `which tesseract` will show you the path to tesseract binary

2. change `screenshot_dir` to the folder where your OS is saving screenshot
  * For MAC, it is usually `/Users/<Your OS Username>/Desktop/`

Once you are done...

```bash
cd full_system/scripts/
python3 run_on_screenshots.py
```

Start playing your selected game in an emulator and when you want to see a translation, just take a screenshot using your OS's screenshot functionality.

# References

Dataset: https://nlp.stanford.edu/projects/jesc/

BLEU scorer: https://github.com/moses-smt/mosesdecoder

OpenNMT-tf: https://github.com/OpenNMT/OpenNMT-tf

Sentencepeice: https://github.com/google/sentencepiece

JackeyFont: https://archive.org/details/jackeyfont

Tesseract: https://github.com/tesseract-ocr/tesseract/