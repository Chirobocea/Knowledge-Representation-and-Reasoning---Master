kb1([
    [not(a), b],
    [c, d],
    [not(d), b],
    [not(c), b],
    [not(b)],
    [e],
    [a, b, not(f), f]
]).

kb0([
    [green(a)],
    [on(a,b)],
    [on(b,c)],
    [not(green(c))],
    [not(on(X,Y)), not(green(X), not(green(Y)))]
]).

kb2([
    [not(b), a],
    [not(a), b, e],
    [a, not(e)],
    [not(a)],
    [e]
]).

kb3([
    [not(a), b],
    [c, f],
    [not(c)],
    [not(f), b],
    [not(c), b]
]).

kb4([
    [a, b], 
    [not(a), not(b)],
    [c]
]).


kb_own([
    [not(travelTo(X, Z)), not(travelWith(Y, X)), travelTo(Y, Z)],
    [not(rich(X)), travelWith(X, skolem_travel(Y))],
    [not(rich(X)), marriedTo(X, skolem_married(Y))],
    [not(travelWith(X, Y)), not(marriedTo(X, Y)), happy(X)],
    [marriedTo(emma, robert)],
    [rich(robert)],
    [not(marriedTo(X, Y)), marriedTo(Y, X)],
    [not(travelWith(X, Y)), travelWith(Y, X)]
]).




find_clause_with_literal([], _, []).
find_clause_with_literal([Clause|_], Literal, Clause) :- 
    member(Literal, Clause).
find_clause_with_literal([_|Rest], Literal, Clause) :- 
    find_clause_with_literal(Rest, Literal, Clause).




find_clause_with_neg_literal([], _, []).
find_clause_with_neg_literal([Clause|_], Literal, Clause) :- 
    member(not(Literal), Clause).
find_clause_with_neg_literal([_|Rest], Literal, Clause) :- 
    find_clause_with_neg_literal(Rest, Literal, Clause).




resolve_clauses(ComplementaryLiteral, [not(ComplementaryLiteral)], ComplementaryLiteral, []).
resolve_clauses(List1, List2, Literal, Resolved) :- 
    delete(List1, Literal, Reduced1), 
    delete(List2, not(Literal), Reduced2), 
    union(Reduced1, Reduced2, Resolved).




remove_duplicates([], []).
remove_duplicates([Head|Tail], [Head|UniqueTail]) :- 
    delete(Tail, Head, TailWithoutHead), 
    remove_duplicates(TailWithoutHead, UniqueTail).





extract_literals([], []).
extract_literals([not(Literal)|Literals], [Literal|Remaining]) :- 
    extract_literals(Literals, Remaining), 
    !.
extract_literals([Literal|Literals], [Literal|Remaining]) :- 
    extract_literals(Literals, Remaining).

extract_unique_literals(Clauses, UniqueLiterals) :- 
    flatten(Clauses, FlatLiterals), 
    extract_literals(FlatLiterals, LiteralList), 
    remove_duplicates(LiteralList, UniqueLiterals).




resolve(KB, 'Unsatisfiable') :- 
    member([], KB), 
    !.

resolve(KB, Status) :- 
    extract_unique_literals(KB, Literals), 
    member(CurrentLiteral, Literals), 
    find_clause_with_literal(KB, CurrentLiteral, PositiveClause), 
    find_clause_with_neg_literal(KB, CurrentLiteral, NegativeClause),
    PositiveClause \= [], 
    NegativeClause \= [], 
    resolve_clauses(PositiveClause, NegativeClause, CurrentLiteral, ResolvedClause), 
    \+ member(ResolvedClause, KB), 
    union(KB, [ResolvedClause], UpdatedKB), 
    resolve(UpdatedKB, Status), 
    !.

resolve(KB, 'Satisfiable') :- 
    extract_unique_literals(KB, Literals), 
    member(CurrentLiteral, Literals), 
    find_clause_with_literal(KB, CurrentLiteral, PositiveClause), 
    find_clause_with_neg_literal(KB, CurrentLiteral, NegativeClause),
    PositiveClause \= [], 
    NegativeClause \= [], 
    resolve_clauses(PositiveClause, NegativeClause, CurrentLiteral, ResolvedClause), 
    member(ResolvedClause, KB), 
    !.

resolve(KB, 'Satisfiable') :- 
    extract_unique_literals(KB, Literals), 
    member(CurrentLiteral, Literals), 
    find_clause_with_literal(KB, CurrentLiteral, PositiveClause),
    PositiveClause == [].

resolve(KB, 'Satisfiable') :- 
    extract_unique_literals(KB, Literals), 
    member(CurrentLiteral, Literals), 
    find_clause_with_neg_literal(KB, CurrentLiteral, NegativeClause),
    NegativeClause == [].




add_negated_to_kb(KB, Literals, Result) :-
    append(KB, [NegatedLiterals], NewKB),
    resolve(NewKB, Result).




test1 :- 
    kb1(KB), 
    resolve(KB, Status), 
    format('Knowledge Base 1 Status: ~w~n', [Status]).

test2 :- 
    kb2(KB), 
    resolve(KB, Status), 
    format('Knowledge Base 2 Status: ~w~n', [Status]).

test3 :- 
    kb3(KB), 
    resolve(KB, Status), 
    format('Knowledge Base 3 Status: ~w~n', [Status]).

test4 :- 
    kb4(KB), 
    resolve(KB, Status), 
    format('Knowledge Base 4 Status: ~w~n', [Status]).

test_kb_default :- 
    kb_own(KB),
    Literals=[not(happy(emma))],
    add_negated_to_kb(KB, Literals, Result),
    format('Test Default KB query: ~w~n', [Result]).

test_own_query(Literals) :-
    kb_own(KB),
    add_negated_to_kb(KB, Literals, Result),
    format('Query Result: ~w~n', [Result]).

test0 :- 
    kb0(KB), 
    resolve(KB, Status), 
    format('Knowledge Base 1 Status: ~w~n', [Status]).