# 20 Questions AI Demo

## Requirements
- Python 3.8+
- pyswip (and SWI-Prolog installed if using Prolog bridge)
- requests (optional if using live DBpedia)

## How to run
1. Ensure all files are in the same folder.
2. Run:
   python controller.py
3. Answer the questions (yes/no/unknown) and see the AI guess the person.

## Notes
- Currently uses offline sample data from `sample_data.py`.
- To integrate live DBpedia, modify `sparql_module.py` with SPARQL queries.
- Prolog questions are defined in `questions.pl`.
- IG calculations are in `ig_module.py`.
