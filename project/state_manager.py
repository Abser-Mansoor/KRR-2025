"""
State manager: properties, initial candidates (demo/offline), and simple helpers.
"""

from sample_data import SAMPLE_CANDIDATES


class GameState:
    def __init__(self, mode: str = "demo"):
        self.mode = mode
        self.kb_path = "questions.pl"
        # Expanded properties for 20-question depth
        self.properties = [
            "fictional", "alive", "gender", "occupation", "field", "nationality",
            "continent", "country", "born_in", "known_for", "notable_work", "award",
            "education", "alma_mater", "spouse", "religion", "movement", "genre",
            "office", "party", "notable_idea", "partner", "children",
            "residence", "ethnicity", "period", "website"
        ]

    def get_initial_candidates(self):
        if self.mode == "demo":
            return SAMPLE_CANDIDATES
        # For online mode, start broad; you could fetch an initial set from DBpedia.
        # For simplicity, reuse sample data as seed; SPARQL filters will refine.
        return SAMPLE_CANDIDATES.copy()