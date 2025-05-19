def define_object_types():
    """
    User defines object types and their attribute schemas.
    Returns:
        dict: object_type -> attribute schema (type + enum/num metadata)
    """
    object_types = {}

    print("\n Define the object types .")
    print("Type 'done' when finished.\n")

    while True:
        obj_type = input("Enter object type or 'done': ").strip()
        if obj_type.lower() == "done":
            break

        schema = {}
        print(f" - Define attributes for object type '{obj_type}'")

        while True:
            attr = input("   ➤ Attribute name (or press Enter to finish): ").strip()
            if not attr:
                break

            kind = input("     Is it enumerative or numerative? (enum/num): ").strip().lower()
            if kind == "enum":
                values = []
                print("     ➤ Enter possible values (press Enter when done):")
                while True:
                    val = input("        - Value: ").strip()
                    if val == "":
                        break
                    values.append(val)
                schema[attr] = {
                    "type": "enum",
                    "values": values
                }

            elif kind == "num":
                num_type = input("     ➤ Type (int/float): ").strip().lower()
                min_val = input("     ➤ Minimum value: ")
                max_val = input("     ➤ Maximum value: ")

                min_val = int(min_val) if num_type == "int" else float(min_val)
                max_val = int(max_val) if num_type == "int" else float(max_val)

                schema[attr] = {
                    "type": "num",
                    "num_type": num_type,
                    "min": min_val,
                    "max": max_val
                }

            else:
                print("❌ Invalid type. Use 'enum' or 'num'.")

        object_types[obj_type] = schema

    print("\n✅ Object types defined:")
    for t, s in object_types.items():
        print(f" - {t}: {s}")

    return object_types
