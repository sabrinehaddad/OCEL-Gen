def build_ocel_log(activities, objects, events):
    """
    Combines activities, objects, and events into a valid OCEL 1.0 log structure.

    Args:
        activities (dict): activity_name -> vmap attribute names and sample values
        objects (dict): object_id -> {"ocel:type": ..., "ocel:ovmap": {...}}
        events (dict): event_id -> OCEL event dictionary

    Returns:
        dict: full OCEL log in OCEL 1.0 JSON format
    """

    # Extract unique object types from the object list
    object_types = list({obj["ocel:type"] for obj in objects.values()})

    ocel_log = {
        "ocel:global-event": {
            "ocel:activity": "__INVALID__"
        },
        "ocel:global-object": {
            "ocel:type": "__INVALID__"
        },
        "ocel:global-log": {
            "ocel:attribute-names": [],
            "ocel:object-types": object_types,
            "ocel:version": "1.0",
            "ocel:ordering": "timestamp"
        },
        "ocel:events": events,
        "ocel:objects": objects
    }

    print(" OCEL log assembled successfully.")
    return ocel_log