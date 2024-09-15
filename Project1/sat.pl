kb1([
    [toddler],
    [\+toddler, child],
    [\+child, \+male, boy],
    [\+infant, child], 
    [\+child, \+female, girl], 
    [female], 
    [girl]
]).

kb2([
    [toddler],
    [\+toddler, child],
    [\+child, \+male, boy],
    [\+infant, child], 
    [\+child, \+female, girl], 
    [female], 
    [\+girl]
]).

kb3([
    [\+a, b],
    [c, d],
    [\+d, b],
    [\+c, b],
    [\+b],
    [e],
    [a, b, \+f, f]
]).

kb4([
    [\+b, a],
    [\+a, b, e],
    [e],
    [a, \+e],
    [\+a]
]).

kb5([
    [\+a, \+e, b],
    [\+d, e, \+b],
    [\+e, f, \+b],
    [f, \+a, e],
    [e, f, \+b]
]).

kb6([
    [a, b],
    [\+a, \+b],
    [\+a, b],
    [a, \+b]
]).




count_occurrences(_, [], 0).

count_occurrences(Literal, [Clause | Rest], Count) :-
    (member(Literal, Clause); member(\+Literal, Clause)),
    count_occurrences(Literal, Rest, RestCount),
    Count is RestCount + 1.

count_occurrences(Literal, [Clause | Rest], Count) :-
    \+member(Literal, Clause),
    \+member(\+Literal, Clause),
    count_occurrences(Literal, Rest, Count).




statistics([], [], []).

statistics([Clause | Rest], Literals, Stats) :-
    statistics(Rest, RestLiterals, _),
    findall(Literal, (member(Literal, Clause); member(\+Literal, Clause)), ClauseLiterals),
    union(RestLiterals, ClauseLiterals, Literals),
    findall(Literal-PosCount-NegCount, (
        member(Literal, Literals),
        count_occurrences(Literal, [Clause | Rest], PosCount),
        count_occurrences(\+Literal, [Clause | Rest], NegCount)
    ), Stats).




most_frequent(Literal, Clauses) :-
    sort(Clauses, ClausesSorted),
    statistics(ClausesSorted, _, Stats),
    max_member(_-Literal, Stats).


most_balanced(Literal, Clauses) :-
    sort(Clauses, ClausesSorted),
    statistics(ClausesSorted, _, Stats),
    maplist(balance_metric, Stats, Balances),
    min_member(_-Literal, Balances).

balance_metric(Literal-PosCount-NegCount, Balance-Literal) :-
    Balance is abs(PosCount - NegCount).






remove_literal([], _, []).

remove_literal([Clause | RestClauses], Literal, [NewClause | NewRest]) :-
    member(Literal, Clause),
    subtract(Clause, [Literal], NewClause),
    remove_literal(RestClauses, Literal, NewRest).

remove_literal([Clause | RestClauses], Literal, [Clause | NewRest]) :-
    \+member(Literal, Clause),
    remove_literal(RestClauses, Literal, NewRest).





resolve_clauses(Clauses, Literal, Result) :-
    findall(C, (member(C, Clauses), \+member(Literal, C), member(\+Literal, C)), NegativeClauses),
    findall(C, (member(C, Clauses), \+member(Literal, C), \+member(\+Literal, C)), PositiveClauses),  
    remove_literal(NegativeClauses, \+Literal, CleanNegativeClauses),
    append(PositiveClauses, CleanNegativeClauses, Result).






davis_putnam_solver([], Assignment, _, _) :-
    writeln('YES'),
    format('Solution: ~w~n', [Assignment]),
    !.

davis_putnam_solver(Clauses, _, _, _) :-
    member([], Clauses),
    writeln('NO'),
    !.

davis_putnam_solver(Clauses, Assignment, Strategy, Conflict) :-
    (Strategy = most_frequent -> most_frequent(Literal, Clauses);
     Strategy = most_balanced -> most_balanced(Literal, Clauses)),

    (member(Literal = true, Assignment) -> \+member(\+Literal = true, Assignment), !;
     member(\+Literal = true, Assignment) -> \+member(Literal = true, Assignment), !;
     resolve_clauses(Clauses, Literal, ResolvedClauses),
     davis_putnam_solver(ResolvedClauses, [Literal = true | Assignment], Strategy, Conflict)),

    (member(Literal = false, Assignment) -> \+member(\+Literal = false, Assignment), !;
     member(\+Literal = false, Assignment) -> \+member(Literal = false, Assignment), !;
     resolve_clauses(Clauses, \+Literal, ResolvedClauses),
     davis_putnam_solver(ResolvedClauses, [Literal = false | Assignment], Strategy, Conflict)).





test1_mostbalanced :- kb1(Clauses), davis_putnam_solver(Clauses, [], most_balanced, _).
test2_mostbalanced :- kb2(Clauses), davis_putnam_solver(Clauses, [], most_balanced, _).
test3_mostbalanced :- kb3(Clauses), davis_putnam_solver(Clauses, [], most_balanced, _).
test4_mostbalanced :- kb4(Clauses), davis_putnam_solver(Clauses, [], most_balanced, _).
test5_mostbalanced :- kb5(Clauses), davis_putnam_solver(Clauses, [], most_balanced, _).
test6_mostbalanced :- kb6(Clauses), davis_putnam_solver(Clauses, [], most_balanced, _).

test1_mostfrequent :- kb1(Clauses), davis_putnam_solver(Clauses, [], most_frequent, _).
test2_mostfrequent :- kb2(Clauses), davis_putnam_solver(Clauses, [], most_frequent, _).
test3_mostfrequent :- kb3(Clauses), davis_putnam_solver(Clauses, [], most_frequent, _).
test4_mostfrequent :- kb4(Clauses), davis_putnam_solver(Clauses, [], most_frequent, _).
test5_mostfrequent :- kb5(Clauses), davis_putnam_solver(Clauses, [], most_frequent, _).
test6_mostfrequent :- kb6(Clauses), davis_putnam_solver(Clauses, [], most_frequent, _).