are_different([]).
are_different([Var | Remaining_Var]):-
    not(member(Var, Remaining_Var)),
    are_different(Remaining_Var).

mini_kakuro_3(Row1Sum, Row2Sum, Row3Sum, Col1Sum, Col2Sum, Col3Sum, 
              A, B, C, D, E, F, G, H, I) :-

    between(1, 9, A), between(1, 9, B), between(1, 9, C),
    between(1, 9, D), between(1, 9, E), between(1, 9, F),
    between(1, 9, G), between(1, 9, H), between(1, 9, I),
    A + B + C =:= Row1Sum,
    D + E + F =:= Row2Sum,
    G + H + I =:= Row3Sum,
    A + D + G =:= Col1Sum,
    B + E + H =:= Col2Sum,
    C + F + I =:= Col3Sum,
    are_different([A, B, C]),
    are_different([D, E, F]),
    are_different([G, H, I]),
    are_different([A, D, G]),
    are_different([B, E, H]),
    are_different([C, F, I]).
