import json
from pprint import pprint

def save_ocel_log(log, filename="output_log.jsonocel"):
    with open(filename, "w") as f:
        json.dump(log, f, indent=2)
    print(f"\n✅ OCEL log saved to: {filename}")


def collect_activities_with_objects():
    events = {}
    objects = {}
    event_counter = 1

    print("🛠️  Enter full event data for your OCEL log.")
    print("Type 'done' as the activity name to finish.\n")

    while True:
        activity = input(f"Enter activity for event e{event_counter}: ")
        if activity.lower() == 'done':
            break

        timestamp = input(f"Enter timestamp for event e{event_counter} (e.g., 1980-01-01T00:00:00): ")

        # Collect vmap (event attributes)
        vmap = {}
        print("Enter event attributes for ocel:vmap (press Enter to skip or 'done' to finish):")
        while True:
            attr_name = input(" - Event attribute name: ").strip()
            if attr_name.lower() == 'done' or attr_name == '':
                break
            attr_value = input(f"   Value for '{attr_name}': ")
            vmap[attr_name] = attr_value

        # Collect omap (linked objects)
        omap = []
        print("Enter object IDs involved in this event (press Enter with no input to stop):")
        while True:
            object_id = input(" - Object ID: ").strip()
            if object_id == "":
                break
            omap.append(object_id)

            # Add object definition if new
            if object_id not in objects:
                obj_type = input(f"   Type for object '{object_id}': ")
                ovmap = {}
                print(f"   Add attributes for object '{object_id}' (press Enter to skip or 'done' to finish):")
                while True:
                    oattr = input("   - Object attribute name: ").strip()
                    if oattr.lower() == 'done' or oattr == "":
                        break
                    ovalue = input(f"     Value for '{oattr}': ")
                    ovmap[oattr] = ovalue
                objects[object_id] = {
                    "ocel:type": obj_type,
                    "ocel:ovmap": ovmap
                }

        # Build event entry
        event_id = f"e{event_counter}"
        events[event_id] = {
            "ocel:activity": activity,
            "ocel:timestamp": timestamp,
            "ocel:omap": omap,
            "ocel:vmap": vmap
        }
        event_counter += 1

    return {
        "ocel:events": events,
        "ocel:objects": objects
    }


if __name__ == "__main__":
    ocel_log = collect_activities_with_objects()

    # Wrap into full OCEL structure
    full_log = {
        "ocel:global-event": {
            "ocel:activity": "__INVALID__"
        },
        "ocel:global-object": {
            "ocel:type": "__INVALID__"
        },
        "ocel:global-log": {
            "ocel:attribute-names": [],
            "ocel:object-types": list({obj["ocel:type"] for obj in ocel_log["ocel:objects"].values()}),
            "ocel:version": "1.0",
            "ocel:ordering": "timestamp"
        },
        "ocel:events": ocel_log["ocel:events"],
        "ocel:objects": ocel_log["ocel:objects"]
    }

    print("\n📝 Your full OCEL log:")
    pprint(full_log)

    save_ocel_log(full_log)
