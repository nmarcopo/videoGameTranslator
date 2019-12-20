# Using the NMT service


## NMT Client

```bash
python translation_client.py
```

Brings up interactive session where you can input Japanese from stdin and the system outputs English on stdout


## Getting BLEU score

```
   ./multi-bleu-detok.perl -lc [reference] < [prediction]
```
