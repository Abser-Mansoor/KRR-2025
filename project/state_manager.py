"""
State manager: properties, initial candidates (demo/offline), and simple helpers.
"""

from sample_data import SAMPLE_CANDIDATES


class StateManager:
    def __init__(self, mode: str = "demo"):
        self.mode = mode
        # Define properties we might ask about
        self.properties = [
            "gender",
            "occupation",
            "nationality",
            "field",
            "fictional",
            "alive",
        ]

    def get_initial_candidates(self):
        if self.mode == "demo":
            return SAMPLE_CANDIDATES
        # For online mode, start broad; you could fetch an initial set from DBpedia.
        # For simplicity, reuse sample data as seed; SPARQL filters will refine.
        return SAMPLE_CANDIDATES.copy()