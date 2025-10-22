translate(0, null). % Helper translation
translate(1, i).
translate(5, v).
translate(10, x).
translate(50, l).
translate(100, c).
translate(500, d).
translate(1000, m).

rom_to_dec([], Acc, Acc, _, _, _).

rom_to_dec(L1, Dec):-
    rom_to_dec(L1, 0, Dec, 'null', 'null', 'null').

rom_to_dec([H1|T1], Acc, Dec, Prev_Symbol, Prev_Prev_Symbol, Prev_Prev_Prev_Symbol):-
    translate(X, Prev_Symbol),
    translate(Y, H1),
    translate(Z, Prev_Prev_Symbol),
    translate(A, Prev_Prev_Prev_Symbol),
    \+((X == Y, X == Z, X == A)),
    X >= Y,
    NewAcc is Acc + Y,
    rom_to_dec(T1, NewAcc, Dec, H1, Prev_Symbol, Prev_Prev_Symbol).

rom_to_dec([H1|T1], Acc, Dec, Prev_Symbol, Prev_Prev_Symbol, Prev_Prev_Prev_Symbol):-
    translate(X, Prev_Symbol),
    translate(Y, H1),
    translate(Z, Prev_Prev_Symbol),
    translate(A, Prev_Prev_Prev_Symbol),
    \+((X == Y, X == Z, X == A)),
    Y > X,
    NewAcc is Acc + Y,
    NewerAcc is NewAcc - X*2,
    rom_to_dec(T1, NewerAcc, Dec, H1, Prev_Symbol, Prev_Prev_Symbol).
