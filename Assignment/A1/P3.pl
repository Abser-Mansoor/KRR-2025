search_islands(Grid, Count) :-
    length(Grid, Rows),
    (Rows > 0 -> nth0(0, Grid, First_Row), length(First_Row, Cols); Cols = 0),
    search(Grid, [], Rows, Cols, 0, 0, Count).

search(_, _, Rows, _, Row, Count, Count) :-
    Row >= Rows.

search(Grid, Visited, Rows, Cols, Row, Curr_Count, Final_Count) :-
    Row < Rows,
    search_in_row(Grid, Visited, Row, Cols, 0, Curr_Count, New_Count, New_Visited),
    NextRow is Row + 1,
    search(Grid, New_Visited, Rows, Cols, NextRow, New_Count, Final_Count).

search_in_row(_, Visited, _, Cols, Col, Count, Count, Visited) :-
    Col >= Cols.

search_in_row(Grid, Visited, Row, Cols, Col, Curr_Count, Final_Count, Final_Visited) :-
    Col < Cols,
    nth0(Row, Grid, GridRow),
    nth0(Col, GridRow, CellValue),
    (   CellValue =:= 1, 
        not(member(cell(Row, Col), Visited))
    ->  
        mark_island(Grid, Visited, Row, Col, Updated_Visited),
        New_Count is Curr_Count + 1,
        Next_Col is Col + 1
    ;   
        Updated_Visited = Visited,
        New_Count = Curr_Count,
        Next_Col is Col + 1
    ),
    search_in_row(Grid, Updated_Visited, Row, Cols, Next_Col, New_Count, Final_Count, Final_Visited).

mark_island(Grid, Visited, Row, Col, Final_Visited) :-
    (   member(cell(Row, Col), Visited)
    ->  Final_Visited = Visited
    ;   search_neighbours(Grid, [cell(Row, Col) | Visited], Row, Col, [(0,1), (1,0), (0,-1), (-1,0)], Final_Visited)
    ).

search_neighbours(_, Visited, _, _, [], Visited).

search_neighbours(Grid, Visited, Row, Col, [(DR, DC)|Directions], Final_Visited) :-
    Neighbour_Row is Row + DR,
    Neighbour_Col is Col + DC,
    (   valid_pos(Grid, Neighbour_Row, Neighbour_Col),
        nth0(Neighbour_Row, Grid, Neighbour_RowList),
        nth0(Neighbour_Col, Neighbour_RowList, 1), 
        not(member(cell(Neighbour_Row, Neighbour_Col), Visited))
    ->  
        mark_island(Grid, Visited, Neighbour_Row, Neighbour_Col, Updated_Visited),
        search_neighbours(Grid, Updated_Visited, Row, Col, Directions, Final_Visited)
    ;  
        search_neighbours(Grid, Visited, Row, Col, Directions, Final_Visited)
    ).

valid_pos(Grid, Row, Col) :-
    length(Grid, Rows),
    nth0(0, Grid, First_Row),
    length(First_Row, Cols),
    Row >= 0,
    Row < Rows,
    Col >= 0,
    Col < Cols.
