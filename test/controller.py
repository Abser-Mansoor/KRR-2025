from ig_module import get_best_question
from prolog_bridge import load_prolog_file, reset_prolog, get_next_question
from sparql_module import execute_sparql
from sample_data import candidates, properties

def main():
    print("=== 20 Questions AI Demo ===")
    load_prolog_file()
    reset_prolog()
    answers = {}  # { (prop, val): yes/no }
    remaining_candidates = candidates.copy()

    while len(remaining_candidates) > 1:
        # Get best question
        best_q = get_best_question(remaining_candidates, properties, answers)
        if not best_q:
            print("No more questions to ask!")
            break
        prop, val = best_q
        # Ask user
        print(f"Question: {prop} = {val}? (yes/no)")
        user_input = input("Answer: ").strip().lower()
        if user_input in ["yes", "y"]:
            ans = "yes"
        elif user_input in ["no", "n"]:
            ans = "no"
        else:
            ans = "unknown"
        answers[(prop, val)] = ans
        # Filter candidates
        filters = {}
        for (p, v), a in answers.items():
            if a == "yes":
                filters[p] = v
        remaining_candidates = execute_sparql(filters)
        print(f"Remaining candidates: {remaining_candidates}")

    if remaining_candidates:
        print(f"My guess: {remaining_candidates[0]}")
    else:
        print("I couldn't guess the person!")

if __name__ == "__main__":
    main()
