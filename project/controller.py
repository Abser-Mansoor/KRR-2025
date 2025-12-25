import sys
import argparse
from state_manager import GameState
from ig_module import InformationGain
from sparql_module import SparqlClient
from prolog_bridge import PrologBridge

class GameController:
    def __init__(self, mode="demo"):
        self.mode = mode
        self.state = GameState()
        self.ig = InformationGain()
        self.sparql = SparqlClient(mode=mode)
        self.prolog = PrologBridge(self.state.kb_path)
        
    def _try_expand(self, answers, current_candidates):
        """Attempt to expand the candidate pool from DBpedia."""
        if self.mode != "online":
            return current_candidates
        
        print("DEBUG: Triggering expansion...")
        expanded = self.sparql.expand_search(answers, self.state.properties)
        
        if not expanded:
            print("DEBUG: Expansion returned nothing")
            return current_candidates
        
        print(f"DEBUG: Expansion returned {len(expanded)} candidates")
        
        # Merge and deduplicate
        seen = {c['name'].lower() for c in current_candidates}
        for e in expanded:
            if e['name'].lower() not in seen:
                current_candidates.append(e)
                seen.add(e['name'].lower())
        
        # Sort by popularity
        current_candidates.sort(key=lambda x: x.get("popularity", 0), reverse=True)
        return current_candidates
        
    def run(self):
        print(f"Starting 20 Questions AI (mode={self.mode})")
        print("Think of a famous personality (real or fictional). I will try to guess!")
        
        candidates = self.state.get_initial_candidates()
        answers = {}
        asked_metadata = set()
        
        turn_count = 0
        while turn_count < 20:
            # EXPANSION CHECK: If pool is too small, try to expand
            if len(candidates) < 3 and self.mode == "online" and turn_count >= 2:
                print(f"DEBUG: Pool size = {len(candidates)}, triggering expansion")
                candidates = self._try_expand(answers, candidates)
            
            # End game if truly out of candidates
            if not candidates:
                print("I'm sorry, I've run out of candidates. You stumped me!")
                break

            # Compute IG map
            ig_map = self.ig.compute(candidates, self.state.properties)
            
            # Get next question from bridge
            q = self.prolog.get_next_question(
                candidates=candidates,
                answers=answers,
                ig_map=ig_map,
                num_asked=turn_count
            )

            # Hard Repeat Guard
            q_meta = (q.get("key"), str(q.get("value_guess")).lower())
            if q_meta in asked_metadata and not q.get("guess"):
                ig_map[q["key"]] = 0
                q = self.prolog.get_next_question(candidates, answers, ig_map, turn_count)
            
            if not q.get("guess"):
                asked_metadata.add((q.get("key"), str(q.get("value_guess")).lower()))

            # Handle guessing
            if q.get("guess"):
                guess_name = q["guess"]
                print(f"My guess is: {guess_name}")
                user_feedback = input("Am I correct? (yes/no): ").strip().lower()
                if user_feedback in ["yes", "y"]:
                    print("Great! Thanks for playing.")
                    break
                else:
                    # Remove the incorrect guess
                    candidates = [c for c in candidates if c.get("name") != guess_name]
                    print("Hmm, let me think more...")
                    
                    # IMMEDIATE EXPANSION after wrong guess if pool is depleted
                    if len(candidates) < 3 and self.mode == "online":
                        candidates = self._try_expand(answers, candidates)
                    
                    turn_count += 1
                    continue

            question_text = q["text"]
            question_key = q["key"]
            value_guess = q.get("value_guess")

            print(f"[{turn_count + 1}/20] Question: {question_text}")
            user_answer = input("Your answer (yes/no/unknown): ").strip().lower()
            turn_count += 1

            if user_answer in ["yes", "y"]:
                if value_guess is not None:
                    if isinstance(value_guess, bool):
                         answers[question_key] = value_guess
                    else:
                         answers[question_key] = str(value_guess).strip()
                else:
                    answers[question_key] = True
            elif user_answer in ["no", "n"]:
                if value_guess is not None:
                     if isinstance(value_guess, bool):
                          answers[question_key] = not value_guess
                     else:
                          v_guess = str(value_guess).strip()
                          current = answers.get(question_key, "unknown")
                          if current == "unknown":
                              answers[question_key] = [('NOT', v_guess)]
                          elif isinstance(current, list):
                              if not any(isinstance(x, tuple) and x[1] == v_guess for x in current):
                                  current.append(('NOT', v_guess))
                          else:
                              answers[question_key] = [current, ('NOT', v_guess)]
                else:
                    answers[question_key] = False
            else:
                answers[question_key] = "unknown"

            # Filter candidates
            candidates = self.sparql.filter_candidates(candidates, answers, properties=self.state.properties)
            candidates.sort(key=lambda x: x.get("popularity", 0), reverse=True)

        # End of game
        if turn_count >= 20 and candidates:
            best_guess = candidates[0]["name"]
            print(f"I've asked 20 questions. My final guess is: {best_guess}")
            feedback = input("Am I correct? (yes/no): ").strip().lower()
            if feedback in ["yes", "y"]:
                print("Great! Thanks for playing.")
            else:
                print("You stumped me! Well played.")
        
        print("Session ended.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["demo", "online"], default="demo")
    args = parser.parse_args()
    
    ctrl = GameController(mode=args.mode)
    ctrl.run()