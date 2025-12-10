"""
Main game controller for 20-Questions AI with DBpedia integration.
Run: python controller.py --mode demo
Modes:
  demo   : offline sample data (no network).
  online : uses DBpedia SPARQL (requires internet).
"""

import argparse
import json
from state_manager import StateManager
from ig_module import InformationGain
from sparql_module import SparqlClient
from prolog_bridge import PrologBridge


class GameController:
    def __init__(self, mode: str = "demo", ig_threshold: float = 0.8, max_conflicts: int = 10):
        self.mode = mode
        self.ig_threshold = ig_threshold
        self.max_conflicts = max_conflicts
        self.state = StateManager(mode=mode)
        self.ig = InformationGain()
        self.sparql = SparqlClient(mode=mode)
        self.prolog = PrologBridge()
        self.prolog.reset_history()
        self.conflict_counter = 0

    def run(self):
        print(f"Starting 20 Questions AI (mode={self.mode})")
        print("Think of a famous personality (real or fictional). I will try to guess!")
        candidates = self.state.get_initial_candidates()
        answers = {}

        while True:
            if len(candidates) == 0:
                print("I have no candidates left. You stumped me!")
                break

            # Compute IG map for remaining candidates
            ig_map = self.ig.compute(candidates, self.state.properties)

            # Ask Prolog for next question (text + key)
            q = self.prolog.get_next_question(
                candidates=candidates,
                answers=answers,
                ig_map=ig_map
            )

            if q.get("guess"):
                print(f"My guess is: {q['guess']}")
                user_feedback = input("Am I correct? (yes/no): ").strip().lower()
                if user_feedback in ["yes", "y"]:
                    print("Great! Thanks for playing.")
                    break
                else:
                    print("Oops, I was wrong. I'll try to learn from this.")
                    # Optional learning hook: ask for DBpedia URI, not implemented for brevity
                    break

            question_text = q["text"]
            question_key = q["key"]
            print(f"Question: {question_text}")
            user_answer = input("Your answer (yes/no/unknown): ").strip().lower()

            # Normalize answer to boolean/unknown
            if user_answer in ["yes", "y"]:
                answers[question_key] = True
            elif user_answer in ["no", "n"]:
                answers[question_key] = False
            else:
                answers[question_key] = "unknown"

            # Filter candidates using SPARQL (or offline filter)
            candidates = self.sparql.filter_candidates(candidates, answers)

            # Guessing conditions in Python (fallback):
            top_ig = max(ig_map.values()) if ig_map else 0
            if len(candidates) == 1 or top_ig >= self.ig_threshold:
                # Ask Prolog if it wants to guess
                g = self.prolog.maybe_guess(candidates, ig_map, self.ig_threshold)
                if g.get("guess"):
                    print(f"My guess is: {g['guess']}")
                    feedback = input("Am I correct? (yes/no): ").strip().lower()
                    if feedback in ["yes", "y"]:
                        print("Great! Thanks for playing.")
                        break
                    else:
                        self.conflict_counter += 1
                        if self.conflict_counter >= self.max_conflicts:
                            print("Too many conflicts. I give up!")
                            break

        print("Session ended.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["demo", "online"], default="demo", help="demo uses offline data; online queries DBpedia")
    args = parser.parse_args()
    GameController(mode=args.mode).run()


if __name__ == "__main__":
    main()