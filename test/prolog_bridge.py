# Prolog bridge using pyswip.
# Requires pyswip and SWI-Prolog installed on the system.
from pyswip import Prolog

prolog = Prolog()

def load_prolog_file(file='questions.pl'):
    prolog.consult(file)

def reset_prolog():
    # retract all asked facts if present
    try:
        prolog.retractall('asked(_,_)')
    except Exception:
        pass

def get_next_question(candidates, answers, ig_map):
    """Calls Prolog to get the next question.
    For this demo, Prolog does not consume candidates/ig_map directly;
    the simple questions.pl returns the next unasked question.
    """
    query = list(prolog.query('next_question(Prop, Val, Text)'))
    if not query:
        return None
    result = query[0]
    return {'prop': result['Prop'], 'val': result['Val'], 'text': result['Text']}
