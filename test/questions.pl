    % Dynamic predicates
    :- dynamic asked/2.

    % Define question templates for each property
    question_template(gender, male, 'Is the person male?').
    question_template(gender, female, 'Is the person female?').
    question_template(occupation, physicist, 'Is the person a physicist?').
    question_template(occupation, engineer, 'Is the person an engineer?').
    question_template(nationality, german, 'Is the person German?').
    question_template(nationality, polish, 'Is the person Polish?').
    question_template(nationality, british, 'Is the person British?').
    question_template(nationality, serbian, 'Is the person Serbian?').
    question_template(known_for, 'theory of relativity', 'Is the person known for the theory of relativity?').
    question_template(known_for, radioactivity, 'Is the person known for radioactivity?').
    question_template(known_for, 'laws of motion', 'Is the person known for the laws of motion?').
    question_template(known_for, 'alternating current', 'Is the person known for alternating current?').

    % Select next question based on unasked templates
    next_question(Prop, Val, Text) :-
        question_template(Prop, Val, Text),
        \+ asked(Prop, Val),
        assertz(asked(Prop, Val)).
