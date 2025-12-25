"""
Information Gain calculation over categorical properties.
"""

import math
from collections import Counter, defaultdict


class InformationGain:
    @staticmethod
    def entropy(counts):
        total = sum(counts)
        if total == 0:
            return 0.0
        ent = 0.0
        for c in counts:
            if c == 0:
                continue
            p = c / total
            ent -= p * math.log2(p)
        return ent

    def compute(self, candidates, properties):
        """
        Returns dict: property -> IG score
        Calculates Binary Information Gain for the most common value of each property.
        """
        ig_map = {}
        total = len(candidates)
        if total <= 1:
            return {p: 0.0 for p in properties}

        # Base entropy is constant for all properties in one turn
        base_entropy = self.entropy([1] * total)

        for prop in properties:
            # We only ask questions about the most common non-unknown/non-noise value
            noise = ["unknown", "none", "n/a", "none recorded", "", "null"]
            values = [str(c.get(prop, "unknown")).lower() for c in candidates]
            filtered_values = [v for v in values if v not in noise]
            
            if not filtered_values:
                ig_map[prop] = 0.0
                continue
            
            most_common_val, count = Counter(filtered_values).most_common(1)[0]
            
            # Binary split: Matches most_common_val (Yes) vs Doesn't match (No)
            yes_count = count
            no_count = total - yes_count
            
            if yes_count == 0 or no_count == 0:
                ig_map[prop] = 0.0
                continue

            # Information Gain = Parent Entropy - (p(yes)*Entropy(yes) + p(no)*Entropy(no))
            # Entropy(S) = log2(|S|) for uniform distribution over candidates
            post_entropy = (yes_count / total) * math.log2(yes_count) + (no_count / total) * math.log2(no_count)
            
            ig = base_entropy - post_entropy
            ig_map[prop] = ig

        return ig_map