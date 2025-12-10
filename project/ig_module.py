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
        """
        ig_map = {}
        # Base entropy on remaining candidates
        base_entropy = self.entropy([1] * len(candidates))

        for prop in properties:
            # Partition candidates by prop value
            buckets = defaultdict(list)
            for c in candidates:
                v = c.get(prop, "unknown")
                buckets[v].append(c)

            # Weighted entropy after split
            total = len(candidates)
            post_entropy = 0.0
            for bucket in buckets.values():
                weight = len(bucket) / total
                post_entropy += weight * self.entropy([1] * len(bucket))

            ig = base_entropy - post_entropy
            ig_map[prop] = ig

        return ig_map