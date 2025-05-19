import random
from datetime import datetime, timedelta

def generate_events(
    activities,
    object_types,
    start_date="1980-01-01",
    activity_constraints=None,
    object_constraints=None,
    object_mapping_constraints=None
):
    events = {}
    timestamp = datetime.fromisoformat(start_date)
    objects = {}
    object_pool = {}
    obj_counter = 1

    # Step 1: Generate object instances based on constraints
    for obj_type, schema in object_types.items():
        rule = object_constraints.get(obj_type, {})
        if "exact" in rule:
            count = rule["exact"]
        else:
            count = random.randint(rule.get("min", 1), rule.get("max", 5))

        object_pool[obj_type] = []
        for _ in range(count):
            obj_id = f"{obj_type[0]}{obj_counter}"
            obj_counter += 1
            ovmap = {}

            for attr, spec in schema.items():
                if spec["type"] == "enum":
                    ovmap[attr] = random.choice(spec["values"])
                elif spec["type"] == "num":
                    val = (
                        random.randint(spec["min"], spec["max"])
                        if spec["num_type"] == "int"
                        else round(random.uniform(spec["min"], spec["max"]), 2)
                    )
                    ovmap[attr] = val

            objects[obj_id] = {
                "ocel:type": obj_type,
                "ocel:ovmap": ovmap
            }
            object_pool[obj_type].append(obj_id)

    # Step 2: Plan activities based on constraints
    planned_activities = []
    for act, rule in (activity_constraints or {}).items():
        if "exact" in rule:
            planned_activities += [act] * rule["exact"]
        elif "min" in rule:
            planned_activities += [act] * rule["min"]

    # Optional: Add more activities if max not reached (based on "max" constraints only)
    max_total = sum([rule.get("max", 0) for rule in (activity_constraints or {}).values()])
    hard_limit = max(max_total, len(planned_activities)) if max_total else len(planned_activities)

    while len(planned_activities) < hard_limit:
        candidates = []
        for act in activities:
            current_count = planned_activities.count(act)
            rule = activity_constraints.get(act, {})
            if "max" in rule and current_count >= rule["max"]:
                continue
            if "exact" in rule and current_count >= rule["exact"]:
                continue
            candidates.append(act)

        if not candidates:
            break
        planned_activities.append(random.choice(candidates))

    random.shuffle(planned_activities)

    # Step 3: Create events
    for i, act in enumerate(planned_activities, start=1):
        event_id = f"e{i}"
        vmap = {}
        activity_schema = activities.get(act, {})

        for attr, spec in activity_schema.items():
            if spec["type"] == "enum":
                vmap[attr] = random.choice(spec["values"])
            elif spec["type"] == "num":
                val = (
                    random.randint(spec["min"], spec["max"])
                    if spec["num_type"] == "int"
                    else round(random.uniform(spec["min"], spec["max"]), 2)
                )
                vmap[attr] = val

        omap = []
        omap_constraints = object_mapping_constraints.get(act, {}) if object_mapping_constraints else {}

        for obj_type, rule in omap_constraints.items():
            pool = object_pool.get(obj_type, [])
            if not pool:
                continue

            if "exact" in rule:
                count = rule["exact"]
            else:
                min_val = rule.get("min", 1)
                max_val = rule.get("max", len(pool))
                count = random.randint(min_val, min(max_val, len(pool)))

            omap += random.sample(pool, min(count, len(pool)))

        events[event_id] = {
            "ocel:activity": act,
            "ocel:timestamp": timestamp.isoformat(),
            "ocel:omap": omap,
            "ocel:vmap": vmap
        }

        timestamp += timedelta(days=1)

    print(f"\n✅ {len(events)} events generated based on activity constraints.")
    return events, objects
