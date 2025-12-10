:- module(questions, [reset_history/0, next_question/4, maybe_guess/4]).
:- use_module(library(http/json)).

:- dynamic asked/1.

reset_history :-
    retractall(asked(_)).

% next_question(+CandidatesJSON, +AnswersJSON, +IGJSON, -ResultJSON)
% ResultJSON is {"text":..., "key":...} or {"guess":...}
next_question(CandJSON, AnsJSON, IGJSON, ResultJSON) :-
    atom_json_dict(CandJSON, Candidates, []),
    atom_json_dict(AnsJSON, Answers, []),
    atom_json_dict(IGJSON, IGMap, []),
    (   Candidates = [] ->
        atom_json_dict(ResultJSON, _{guess:"unknown"}, [])
    ;   best_unasked_question(IGMap, Answers, Key) ->
        format(string(Txt), "Does the person have property '~w'?", [Key]),
        atom_json_dict(ResultJSON, _{text:Txt, key:Key}, [])
    ;   Candidates = [C|_] ->
        Name = C.get(name),
        atom_json_dict(ResultJSON, _{guess:Name}, [])
    ).

best_unasked_question(IGMap, Answers, BestKey) :-
    findall(K,
        ( get_dict(K, IGMap, _),
          \+ get_dict(K, Answers, _),
          \+ asked(K)
        ),
        Keys),
    Keys \= [],
    % Build pairs IG-Prop, sort descending by IG
    findall(IG-K, (member(K, Keys), get_dict(K, IGMap, IG)), Pairs),
    keysort(Pairs, Asc),
    reverse(Asc, Desc),
    Desc = [_IG-BestKey|_],
    assertz(asked(BestKey)).

% maybe_guess(+CandidatesJSON, +IGJSON, +Threshold, -ResultJSON)
maybe_guess(CandJSON, IGJSON, Threshold, ResultJSON) :-
    atom_json_dict(CandJSON, Candidates, []),
    atom_json_dict(IGJSON, IGMap, []),
    (   Candidates = [C|[]] ->
        Name = C.get(name),
        atom_json_dict(ResultJSON, _{guess:Name}, [])
    ;   max_ig(IGMap, Max), Max >= Threshold, Candidates = [C|_] ->
        Name = C.get(name),
        atom_json_dict(ResultJSON, _{guess:Name}, [])
    ;   atom_json_dict(ResultJSON, _{}, [])
    ).

max_ig(IGMap, Max) :-
    dict_pairs(IGMap, _, Pairs),
    pairs_values(Pairs, Vs),
    max_list(Vs, Max).