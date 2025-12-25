"""
Bridge between Python and Prolog using pyswip.
Provides next question selection and guessing via Prolog predicates.
"""

from collections import Counter

try:
    from pyswip import Prolog
except Exception:
    Prolog = None


class PrologBridge:
    def __init__(self, prolog_file="questions.pl"):
        self.enabled = Prolog is not None
        if self.enabled:
            try:
                self.prolog = Prolog()
                self.prolog.consult(prolog_file)
            except Exception:
                self.enabled = False
        else:
            self.prolog = None

    def reset_history(self):
        if not self.enabled:
            return
        list(self.prolog.query("reset_history."))

    def _generate_natural_question(self, key, candidates, answers=None):
        """Generate a natural language question for a property."""
        answers = answers or {}
        noise = ["unknown", "none", "n/a", "none recorded", "", "null"]
        
        # Track already asked/rejected values
        invalid_values = set()
        ans_val = answers.get(key)
        if isinstance(ans_val, list):
            for item in ans_val:
                if isinstance(item, tuple) and item[0] == 'NOT':
                    invalid_values.add(str(item[1]).lower())
                else:
                    invalid_values.add(str(item).lower())
        elif isinstance(ans_val, tuple) and ans_val[0] == 'NOT':
            invalid_values.add(str(ans_val[1]).lower())
        elif ans_val is not None:
            invalid_values.add(str(ans_val).lower())

        # Collect valid values from candidates
        values = []
        for c in candidates:
            val = c.get(key)
            if val is not None:
                v_str = str(val).strip().lower()
                if v_str not in noise and v_str not in invalid_values and len(v_str) < 50:
                    values.append(val)
        
        if not values:
            if key in answers and answers[key] != "unknown":
                return {"repeat": True, "key": key}
            
            # Generic fallback
            generic_map = {
                "award": "Has the person won any major awards?",
                "notable_work": "Is the person known for any notable works?",
                "occupation": "Does the person have a known occupation?",
                "nationality": "Do we know the person's nationality?"
            }
            q_text = generic_map.get(key, f"Is there anything notable about the person's {key.replace('_', ' ')}?")
            return {"text": q_text, "key": key}
        
        most_common_val, _ = Counter(values).most_common(1)[0]
        disp_val = str(most_common_val)
        if "," in disp_val and len(disp_val) > 30:
            disp_val = disp_val.split(",")[0].strip()

        # Question templates
        mapping = {
            "gender": f"Is the person {disp_val}?",
            "occupation": f"Is their occupation {disp_val}?",
            "nationality": f"Is their nationality {disp_val}?",
            "field": f"Was the person's field {disp_val}?",
            "continent": f"Was the person born in {disp_val}?",
            "country": f"Was the person born in {disp_val}?",
            "born_in": f"Was the person born in {disp_val}?",
            "notable_work": f"Is the person known for '{disp_val}'?",
            "award": f"Has the person won the {disp_val} award?",
            "known_for": f"Is the person known for {disp_val}?",
        }

        q_text = mapping.get(key, f"Is the {key.replace('_', ' ')} related to '{disp_val}'?")
        v_guess = most_common_val
        
        # Special handling for boolean properties
        if key == "alive":
            q_text = "Is the person alive?" if most_common_val is True else "Is the person deceased?"
            v_guess = most_common_val
        elif key == "fictional":
            q_text = "Is the person fictional?" if most_common_val is True else "Is the person real (non-fictional)?"
            v_guess = most_common_val

        return {"text": q_text, "key": key, "value_guess": v_guess}

    def get_next_question(self, candidates, answers, ig_map, num_asked=0):
        """Select the next question based on Information Gain."""
        # If only one candidate, guess it
        if len(candidates) == 1:
            return {"guess": candidates[0]["name"]}
        
        if not candidates:
            return {"guess": "unknown"}
        
        # Find unanswered properties with positive IG
        unanswered_items = []
        for k, v in ig_map.items():
            if v <= 0.05:
                continue
            # Skip already answered boolean properties
            if k in ["alive", "fictional", "gender"] and k in answers:
                continue
            unanswered_items.append((k, v))

        if not unanswered_items:
            return {"guess": candidates[0]["name"]}

        # Sort by IG (highest first)
        unanswered_items.sort(key=lambda x: x[1], reverse=True)

        # Try to generate a non-repeat question
        for best_prop, _ in unanswered_items:
            q = self._generate_natural_question(best_prop, candidates, answers)
            if q.get("repeat"):
                continue
            return q

        # Fallback: guess the top candidate
        return {"guess": candidates[0]["name"]}