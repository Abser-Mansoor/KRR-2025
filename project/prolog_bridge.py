"""
Bridge between Python and Prolog using pyswip.
Provides next question selection and guessing via Prolog predicates.
"""

import json

try:
    from pyswip import Prolog, Functor, Variable, Query
except Exception:
    Prolog = None  # Fallback if pyswip isn't installed


class PrologBridge:
    def __init__(self, prolog_file="questions.pl"):
        self.enabled = Prolog is not None
        if self.enabled:
            self.prolog = Prolog()
            self.prolog.consult(prolog_file)
        else:
            self.prolog = None

    def reset_history(self):
        if not self.enabled:
            return
        list(self.prolog.query("reset_history."))

    def get_next_question(self, candidates, answers, ig_map):
        """
        Returns dict {text: ..., key: ...} or {guess: ...}
        """
        if not self.enabled:
            # Fallback: pick max IG property not yet answered
            unanswered = [k for k in ig_map.keys() if k not in answers]
            if not unanswered:
                return {"guess": candidates[0]["name"] if candidates else "unknown"}
            best = max(unanswered, key=lambda k: ig_map[k])
            return {
                "text": f"Does the person have property '{best}'?",
                "key": best,
            }

        cand_json = json.dumps(candidates)
        ans_json = json.dumps(answers)
        ig_json = json.dumps(ig_map)
        res = list(self.prolog.query(f"next_question('{cand_json}', '{ans_json}', '{ig_json}', R)."))
        if not res:
            return {"guess": candidates[0]["name"] if candidates else "unknown"}
        out = res[0]["R"]
        return json.loads(out)

    def maybe_guess(self, candidates, ig_map, threshold):
        if not self.enabled:
            if len(candidates) == 1:
                return {"guess": candidates[0]["name"]}
            top_ig = max(ig_map.values()) if ig_map else 0
            if top_ig >= threshold and candidates:
                return {"guess": candidates[0]["name"]}
            return {}
        cand_json = json.dumps(candidates)
        ig_json = json.dumps(ig_map)
        res = list(self.prolog.query(f"maybe_guess('{cand_json}', '{ig_json}', {threshold}, R)."))
        if not res:
            return {}
        return json.loads(res[0]["R"])