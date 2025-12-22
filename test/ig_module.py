from collections import Counter
import math

def calculate_information_gain(candidates, prop, val, properties):
    yes_count = sum(1 for c in candidates if properties.get(c, {}).get(prop, None) == val)
    no_count = len(candidates) - yes_count
    total = yes_count + no_count
    if total == 0:
        return 0
    # Entropy formula for binary split
    def entropy(n, total):
        if n == 0:
            return 0.0
        p = n / total
        return -p * math.log(p, 2)
    entropy_after = entropy(yes_count, total) + entropy(no_count, total)
    # Use 1 - entropy_after as a heuristic score
    ig = 1 - entropy_after
    return ig

def get_best_question(candidates, properties, asked_questions):
    # Generate all possible property-value pairs
    prop_vals = set()
    for c in candidates:
        props = properties.get(c, {})
        for prop, val in props.items():
            if (prop, val) not in asked_questions:
                prop_vals.add((prop, val))
    # Compute IG for each pair
    scored = [ (calculate_information_gain(candidates, p, v, properties), (p, v)) for p, v in prop_vals ]
    if not scored:
        return None
    scored.sort(reverse=True, key=lambda x: x[0])
    return scored[0][1]  # (prop, val)
