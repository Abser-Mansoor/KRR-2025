member(X, [X|_]).
member(X, [_|Tail]):-
  member(X, Tail).

set_member(X, List):-
  setify(List, Set),
  member(X, Set).

set_union([], L2, RL):-
  RL = L2.

set_union([H1|L1], L2, L3):-
  set_member(H1, L2),
  set_union(L1, L2, L3).

set_union([H1|L1], L2, [H1|L3]):-
  not(set_member(H1,L2)),
  set_union(L1,L2,L3).

set_intersection([], _, []).
set_intersection(_, [], []).

set_intersection([H1|L1], L2, [H1|L3]):-
  set_member(H1, L2),
  set_intersection(L1, L2, L3).

set_intersection([H1|L1], L2, L3):-
  not(set_member(H1, L2)),
  set_intersection(L1, L2, L3).

reverse(L1, Reversed):-
  reverse(L1, [], Reversed).

reverse([], Accumulated, Accumulated).

reverse([H1|L1], Acc, Reversed):-
  reverse(L1, [H1|Acc], Reversed).

setify(L1, Set):-
  setify(L1, [], Reversed),
  reverse(Reversed, Set).

setify([], Accumulated, Accumulated).

setify([H1|L1], Acc, Set):-
  set_member(H1, Acc),
  setify(L1, Acc, Set).

setify([H1|L1], Acc, Set):-
  not(set_member(H1, Acc)),
  setify(L1, [H1|Acc], Set).

set_cardinality(L1, Card):-
  setify(L1, X),
  set_cardinality(X, 0, Card).

set_cardinality([], Acc, Acc).

set_cardinality([H1|L1], Acc, Card):-
  New_Acc is Acc + 1,
  set_cardinality(L1, New_Acc, Card).

set_difference([], _, []).

set_difference([H1|L1], L2, [H1|RL]):-
  not(set_member(H1, L2)),
  set_difference(L1, L2, RL).

set_difference([H1|L1], L2, RL):-
  set_member(H1,L2),
  set_difference(L1, L2, RL).

%Operator Overloadings
:- op(600, xfx, u).
:- op(800, xfx, equals).

A u B  equals RL :- set_union(A, B, RL).

:- op(500, xfx, n).

A n B equals RL :- set_intersection(A, B, RL).

:- op(400, xfx, power).

power_set([], [[]]).

power_set([X|XT], Power_Set):-
  power_set(XT, Power),
  add_element(X, Power, With_X),
  append(Power, With_X, Power_Set).

add_element(_, [], []).
add_element(X, [H1|T1], [[X|H1] | RL]) :-
  add_element(X, T1, RL).

A power B :- power_set(A, B).
