task(Name, Priority, Duration, DeadlineDate).
priority_value(high, 3).
priority_value(medium, 2).
priority_value(low, 1).
compare_tasks(task(_, P1, _, _), task(_, P2, _, _)) :-
    priority_value(P1, V1),
    priority_value(P2, V2),
    V1 > V2.
sort_by_priority(SortedTasks) :-
    findall(task(Name, Priority, Duration, Deadline),
            task(Name, Priority, Duration, Deadline),
            Tasks),
    predsort(compare_by_priority, Tasks, SortedTasks).
next_task(Name) :-
    sort_by_priority([task(Name, _, _, _) | _]).
today_plan(Plan) :-
    findall(task(N,P,D,DL), (task(N,P,D,DL), task_fits(N)), Fittable),
    predsort(compare_by_priority, Fittable, Plan).

