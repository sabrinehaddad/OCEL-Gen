def define_activities():
    """
    Allows the user to define activities and detailed attribute schemas.
    Supports enumerative and numerative data for each vmap attribute.

    Returns:
        dict: activity_name -> dict(attribute_name -> schema)
    """
    activities = {}

    print("Define the activities and their attributes.")
    print("Type 'done' when finished.\n")

    while True:
        activity_name = input("Enter activity name (or 'done'): ").strip()
        if activity_name.lower() == 'done':
            break

        attributes = {}

        print(f" - Define attributes for activity '{activity_name}'")
        while True:
            attr_name = input("   ➤ Attribute name (or press Enter to finish): ").strip()
            if not attr_name:
                break

            attr_type = input("     Is it enumerative or numerative? (enum/num): ").strip().lower()
            if attr_type == "enum":
                values = []
                print("     ➤ Enter possible values (press Enter when done):")
                while True:
                    value = input("        - Value: ").strip()
                    if value == "":
                        break
                    values.append(value)
                attributes[attr_name] = {
                    "type": "enum",
                    "values": values
                }

            elif attr_type == "num":
                num_type = input("     ➤ Type (int/float): ").strip().lower()
                min_val = input("     ➤ Minimum value: ").strip()
                max_val = input("     ➤ Maximum value: ").strip()

                if num_type == "int":
                    min_val = int(min_val)
                    max_val = int(max_val)
                else:
                    min_val = float(min_val)
                    max_val = float(max_val)

                attributes[attr_name] = {
                    "type": "num",
                    "num_type": num_type,
                    "min": min_val,
                    "max": max_val
                }

            else:
                print("❌ Invalid type. Please enter 'enum' or 'num'.")

        activities[activity_name] = attributes

    print("\n Final activity schema:")
    for name, schema in activities.items():
        print(f" - {name}:")
        for attr, meta in schema.items():
            print(f"   • {attr} → {meta}")

    return activities
