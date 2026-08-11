STRATEGIES = {
    "Balanced": {"work": 52, "break": 17},
    "Classic": {"work": 25, "break": 5},
    "Deep": {"work": 90, "break": 20}
}

def create_plan(total_minutes, strategy, custom_work = None, custom_break = None):
    if strategy == "custom":
        work_time = custom_work
        break_time = custom_break
    else:
        work_time = STRATEGIES[strategy]["work"]
        break_time = STRATEGIES[strategy]["break"]

    plan = []
    remaining = total_minutes
    while remaining > 0:
        current_work = min(work_time, remaining)
        plan.append(("work", current_work))
        remaining -= current_work

        if remaining > 0:
            current_break = min(break_time, remaining)

        plan.append(("break", current_break))
        remaining -= current_break
    return plan
        

