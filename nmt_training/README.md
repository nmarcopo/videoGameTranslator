# NMT Training

## Requirements

This part has a different requirements from rest of the system since it's used to train the model

Requires:
- Python >= 3.6
- Opennmt toolkit
```bash
pip install OpenNMT-tf
pip install sentencepiece
```

## Replicate the Training
 
1. Download the data from JESC website [here](https://nlp.stanford.edu/projects/jesc/data/split.tar.gz) and unzip the contents into this folder 
 
2. Download FastText Pre-trained Embedding [Japanese](https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.ja.300.vec.gz), [English](https://dl.fbaipublicfiles.com/fasttext/vectors-crawl/cc.en.300.vec.gz) and unzip the contents into this folder


3. split the data into language pairs

```bash
python split.py
```

This will create 6 files {train|dev|test}.{jpn|eng}

4. Train sentencepiece model on the training set for Japanese and English
```bash
python sp_trainer.py --input-file train.<language> --model-name sp.<language>
```

5. Use this command to run OpenNMT on custom configuration
```bash
onmt-main --config config.yml --model transformer_custom.py train --with_eval
```
This will save all the training files and the models under model directory `train_transfomer_relative/`

6. Run prediction using the trained model
```bash
onmt-main --model transformer_custom.py --config config.yml --checkpoint_path train_transfomer_relative/ infer --features_file test.jp --predictions_file pred.en.txt
```

This will use the most recent model on the model directory and save the prediction text as pred.en.txt
