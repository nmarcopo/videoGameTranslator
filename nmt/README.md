# Using the NMT service

## Setup

- Install requirements as in the main README
- Download models as in the main README

## NMT Client

```bash
python translation_client.py <path_to_translation_model_directory>
```

Brings up interactive session where you can input Japanese from stdin and the system outputs English on stdout


## Getting BLEU score

```
./multi-bleu-detok.perl -lc [reference] < [prediction]
```
