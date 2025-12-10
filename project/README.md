# 20 Questions AI (DBpedia + Prolog + Python IG)

This project plays a 20-questions-style game to guess a famous personality. It uses:
- Python for the controller, information gain (IG), and SPARQL queries.
- Prolog (SWI) for question selection and guessing logic.
- `pyswip` as the Python–Prolog bridge.
- DBpedia (online mode) or an offline sample dataset (demo mode).

## Files
- `controller.py` — main game loop.
- `state_manager.py` — properties and initial candidates.
- `ig_module.py` — information gain computation.
- `sparql_module.py` — DBpedia SPARQL and offline filtering.
- `prolog_bridge.py` — Python ↔ Prolog bridge.
- `questions.pl` — Prolog logic for question selection and guessing.
- `sample_data.py` — offline demo candidates.
- `requirements.txt` — Python dependencies.

## Setup

### Python
```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### Prolog
Install SWI-Prolog and ensure it’s on PATH (required for pyswip).
- macOS: `brew install swi-prolog`
- Ubuntu: `sudo apt-get install swi-prolog`
- Windows: download from [https://www.swi-prolog.org/Download.html](https://www.swi-prolog.org/Download.html)

### pyswip notes
If pyswip cannot find SWI-Prolog, set `SWI_HOME_DIR` or consult pyswip docs. In worst case, the bridge falls back to a Python-only question selector.

## Running
Demo (offline, no network):
```bash
python controller.py --mode demo
```

Online (DBpedia; needs internet):
```bash
python controller.py --mode online
```

## How it works
1. Start with a candidate set (offline sample or DBpedia seed).
2. Compute IG per property over remaining candidates.
3. Prolog selects the highest-IG unasked question (tracks `asked/1`).
4. User answers yes/no/unknown.
5. Candidates are filtered (offline or via SPARQL).
6. Guess triggers if only one candidate remains or IG exceeds threshold.

## Demo Transcript (sample)
```
$ python controller.py --mode demo
Starting 20 Questions AI (mode=demo)
Think of a famous personality (real or fictional). I will try to guess!
Question: Does the person have property 'field'?
Your answer (yes/no/unknown): yes
Question: Does the person have property 'fictional'?
Your answer (yes/no/unknown): no
Question: Does the person have property 'occupation'?
Your answer (yes/no/unknown): yes
Question: Does the person have property 'gender'?
Your answer (yes/no/unknown): no
Question: Does the person have property 'nationality'?
Your answer (yes/no/unknown): polish
My guess is: Marie Curie
Am I correct? (yes/no): yes
Great! Thanks for playing.
Session ended.
```

## Design notes
- IG is computed on categorical properties; entropy-based.
- Prolog chooses unasked questions with highest IG.
- `maybe_guess/4` in Prolog uses IG threshold or single remaining candidate.
- Offline filtering is simple exact/boolean matching.
- Online mode builds a basic SPARQL; you may need to adapt predicates to real DBpedia schemas.

## Future improvements
- Richer property mapping to actual DBpedia predicates.
- Better natural-language question templates per property/value.
- Learning step: accept a DBpedia URI on failure and persist locally.
- More robust SPARQL query construction (e.g., occupations, genders, nationalities).