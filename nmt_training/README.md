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

1. Download the data from JESC website [here](https://nlp.stanford.edu/projects/jesc/data/split.tar.gz)

2. Train sentencepiece model on the training set
```bash
python sp_trainer.py --input-file train.<language> --model-name sp.<language>
```

3. Use this command to run OpenNMT on custom configuration
```bash
onmt-main --model transformer_custom.py --config config.yml train --with_eval
```
This will save all the training files and the models under model directory `train_transfomer_relative/`

4. Run prediction using the trained model
```bash
onmt-main --model_type transformer_custom.py --config config.yml --checkpoint_path train_transfomer_relative/ infer --features_file test.jp --predictions_file pred.en.txt
```

This will use the most recent model on the model directory and save the prediction text as pred.en.txt