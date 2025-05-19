from generator.activity_definer import define_activities
from generator.object_definer import define_object_types
from generator.event_generator import generate_events
from generator.ocel_builder import build_ocel_log
from generator.log_saver import save_log
from generator.event_generator import (
    get_activity_constraints,
    get_object_constraints,
    get_object_mapping_constraints
)

def main():
    print("🎬 OCEL Log Generator Starting...\n")

    # Step 1: Define activities and attributes
    activities = define_activities()

    # Step 2: Define object types and attributes
    object_types = define_object_types()

    # Step 3: Define object constraints (min/max/exact counts)
    object_constraints = get_object_constraints(object_types)

    # Step 4: Define activity constraints (min/max/exact occurrences)
    activity_constraints, _ = get_activity_constraints(list(activities.keys()))

    # Step 5: Define object mapping constraints (how many objects per activity)
    object_mapping_constraints = get_object_mapping_constraints(
        list(activities.keys()),
        list(object_types.keys())
    )

    # ✅ Step 6: Generate events with all constraints (without num_events)
    events, objects = generate_events(
        activities=activities,
        object_types=object_types,
        activity_constraints=activity_constraints,
        object_constraints=object_constraints,
        object_mapping_constraints=object_mapping_constraints
    )

    # Step 7: Build OCEL log
    ocel_log = build_ocel_log(activities, objects, events)

    # Step 8: Save the OCEL log
    filename = input("\n💾 Enter output filename (or press Enter for 'output/generated_log.jsonocel'): ").strip()
    if not filename:
        filename = "output/generated_log.jsonocel"

    save_log(ocel_log, filename)
    print(f"\n✅ Done! Log saved to `{filename}`.")

if __name__ == "__main__":
    main()

