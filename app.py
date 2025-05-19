import streamlit as st
from generator.activity_definer import define_activities
from generator.object_definer import define_object_types
from generator.event_generator import generate_events
from generator.ocel_builder import build_ocel_log
from generator.log_saver import save_log

# --- Page 1: Activities ---
def define_activities_page():
    st.subheader("🧩 Activity Definitions")

    # Init session state
    if "activities" not in st.session_state:
        st.session_state.activities = {}

    col1, col2 = st.columns([1, 2])

    # --- 📋 Activity list + delete ---
    with col1:
        st.markdown("### 📋 Defined Activities")
        activity_list = list(st.session_state.activities.keys())

        if activity_list:
            selected_activity = st.radio("Select activity", activity_list, key="activity_selector")

            if st.button("🗑️ Remove Selected Activity"):
                del st.session_state.activities[selected_activity]
                st.session_state.pop("activity_selector", None)
                st.success(f"Removed activity: {selected_activity}")
                st.rerun()

        else:
            st.info("No activities defined yet.")

        new_activity = st.text_input("➕ Add new activity")
        if st.button("Add Activity"):
            if new_activity and new_activity not in st.session_state.activities:
                st.session_state.activities[new_activity] = {}
                st.success(f"Added activity: {new_activity}")
                st.rerun()
            elif new_activity in st.session_state.activities:
                st.warning("Activity already exists.")

    # --- 🧩 Add/edit enum and numeric attributes ---
    with col2:
        if "activity_selector" in st.session_state and st.session_state.activity_selector:
            activity = st.session_state.activity_selector
            st.markdown(f"### ✏️ Edit Attributes for `{activity}`")

            # --- Enumerative Attribute ---
            st.markdown("#### 🌱 Enumerative Attribute")
            enum_attr = st.text_input("Attribute name (enum)", key="enum_name")
            enum_values = st.text_area("Comma-separated values", key="enum_vals")
            if st.button("Add Enum Attribute"):
                st.session_state.activities[activity][enum_attr] = {
                    "type": "enum",
                    "values": [v.strip() for v in enum_values.split(",") if v.strip()]
                }
                st.success(f"Enum attribute '{enum_attr}' added to '{activity}'")
                st.rerun()

            # --- Numeric Attribute ---
            st.markdown("#### 📏 Numeric Attribute")
            num_attr = st.text_input("Attribute name (numeric)", key="num_name")
            num_type = st.selectbox("Numeric type", ["int", "float"], key="num_type")
            min_val = st.number_input("Min value", key="num_min")
            max_val = st.number_input("Max value", key="num_max")

            if st.button("Add Numeric Attribute"):
                st.session_state.activities[activity][num_attr] = {
                    "type": "num",
                    "num_type": num_type,
                    "min": float(min_val),
                    "max": float(max_val)
                }
                st.success(f"Numeric attribute '{num_attr}' added to '{activity}'")
                st.rerun()

            # --- Attribute List & Deletion ---
            if st.session_state.activities[activity]:
                st.markdown("### 🧠 Current Attributes")
                attr_list = list(st.session_state.activities[activity].keys())
                selected_attr = st.selectbox("Select attribute to delete", attr_list, key="attr_delete")

                if st.button("❌ Delete Selected Attribute"):
                    del st.session_state.activities[activity][selected_attr]
                    st.success(f"Deleted attribute '{selected_attr}' from '{activity}'")
                    st.rerun()
        else:
            st.info("Select an activity from the list to edit attributes.")


# --- Page 2: Object Types ---
def define_object_types_page():
    st.subheader("📦 Object Type Definitions")

    # Init session state
    if "object_types" not in st.session_state:
        st.session_state.object_types = {}

    col1, col2 = st.columns([1, 2])

    # --- 📋 Object type list + delete ---
    with col1:
        st.markdown("### 📋 Defined Object Types")
        object_type_list = list(st.session_state.object_types.keys())

        if object_type_list:
            selected_type = st.radio("Select object type", object_type_list, key="object_type_selector")

            if st.button("🗑️ Remove Selected Object Type"):
                del st.session_state.object_types[selected_type]
                st.session_state.pop("object_type_selector", None)
                st.success(f"Removed object type: {selected_type}")
                st.rerun()
        else:
            st.info("No object types defined yet.")

        new_type = st.text_input("➕ Add new object type")
        if st.button("Add Object Type"):
            if new_type and new_type not in st.session_state.object_types:
                st.session_state.object_types[new_type] = {}
                st.success(f"Added object type: {new_type}")
                st.rerun()
            elif new_type in st.session_state.object_types:
                st.warning("Object type already exists.")

    # --- 🧩 Add/edit attributes for selected object type ---
    with col2:
        if "object_type_selector" in st.session_state and st.session_state.object_type_selector:
            obj_type = st.session_state.object_type_selector
            st.markdown(f"### ✏️ Edit Attributes for `{obj_type}`")

            # --- Enumerative Attribute ---
            st.markdown("#### 🌱 Enumerative Attribute")
            enum_attr = st.text_input("Attribute name (enum)", key="enum_obj_name")
            enum_values = st.text_area("Comma-separated values", key="enum_obj_vals")
            if st.button("Add Enum Attribute"):
                st.session_state.object_types[obj_type][enum_attr] = {
                    "type": "enum",
                    "values": [v.strip() for v in enum_values.split(",") if v.strip()]
                }
                st.success(f"Enum attribute '{enum_attr}' added to '{obj_type}'")
                st.rerun()

            # --- Numeric Attribute ---
            st.markdown("#### 📏 Numeric Attribute")
            num_attr = st.text_input("Attribute name (numeric)", key="num_obj_name")
            num_type = st.selectbox("Numeric type", ["int", "float"], key="num_obj_type")
            min_val = st.number_input("Min value", key="num_obj_min")
            max_val = st.number_input("Max value", key="num_obj_max")

            if st.button("Add Numeric Attribute"):
                st.session_state.object_types[obj_type][num_attr] = {
                    "type": "num",
                    "num_type": num_type,
                    "min": float(min_val),
                    "max": float(max_val)
                }
                st.success(f"Numeric attribute '{num_attr}' added to '{obj_type}'")
                st.rerun()

            # --- Attribute List & Deletion ---
            if st.session_state.object_types[obj_type]:
                st.markdown("### 🧠 Current Attributes")
                attr_list = list(st.session_state.object_types[obj_type].keys())
                selected_attr = st.selectbox("Select attribute to delete", attr_list, key="obj_attr_delete")

                if st.button("❌ Delete Selected Attribute"):
                    del st.session_state.object_types[obj_type][selected_attr]
                    st.success(f"Deleted attribute '{selected_attr}' from '{obj_type}'")
                    st.rerun()
        else:
            st.info("Select an object type from the list to edit attributes.")


# --- Page 3: Activity Constraints ---
def define_activity_constraints_page():
    st.subheader("📏 Activity Constraints")

    if "activity_constraints" not in st.session_state:
        st.session_state.activity_constraints = {}

    # Left: View and delete existing constraints
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### 📋 Defined Constraints")
        constraint_list = []
        for activity, rules in st.session_state.activity_constraints.items():
            for kind, value in rules.items():
                constraint_list.append(f"{kind.upper()} | {activity} | {value}")

        selected_constraint = st.radio("Select constraint to remove", constraint_list if constraint_list else ["No constraints yet"])

        if st.button("🗑️ Remove Selected Constraint") and constraint_list and selected_constraint != "No constraints yet":
            kind, activity, _ = selected_constraint.split(" | ")
            kind = kind.lower()
            if kind in st.session_state.activity_constraints.get(activity, {}):
                del st.session_state.activity_constraints[activity][kind]
                if not st.session_state.activity_constraints[activity]:
                    del st.session_state.activity_constraints[activity]
                st.success(f"Removed constraint: {selected_constraint}")
                st.rerun()

    with col2:
        st.markdown("### ➕ Add New Constraint")

        constraint_type = st.selectbox("Constraint type", [
            "Min: Activity A occurs at least N times",
            "Max: Activity A occurs at most N times",
            "Exact: Activity A occurs exactly N times"
        ])

        activity_options = list(st.session_state.activities.keys()) if "activities" in st.session_state else []
        selected_activity = st.selectbox("Select Activity", activity_options)

        n = st.number_input("Enter N", min_value=1, step=1)

        if st.button("➕ Add Constraint"):
            kind = constraint_type.split(":")[0].lower()  # Extract min/max/exact
            st.session_state.activity_constraints.setdefault(selected_activity, {})[kind] = int(n)
            st.success(f"Added {kind.upper()} constraint: {selected_activity} => {n}")
            st.rerun()



# --- Page 4: Object Constraints ---
def define_object_constraints_page():
    st.subheader("📦 Object Constraints")

    # Initialize session state
    if "object_constraints" not in st.session_state:
        st.session_state.object_constraints = {}
    if "object_types" not in st.session_state or not st.session_state.object_types:
        st.info("⚠️ Please define object types first before adding constraints.")
        return

    obj_type = st.selectbox("Object Type O", list(st.session_state.object_types.keys()))

    # Mapping for display vs internal keys
    label_to_key = {
        "Min: Object Type O has at least N objects": "min",
        "Max: Object Type O has at most N objects": "max",
        "Exact: Object Type O has exactly N objects": "exact"
    }

    constraint_label = st.selectbox("Constraint type", list(label_to_key.keys()))
    constraint_value = st.number_input("Enter N", min_value=1, step=1)

    if st.button("➕ Add Object Constraint"):
        key = label_to_key[constraint_label]
        st.session_state.object_constraints.setdefault(obj_type, {})[key] = constraint_value
        st.success(f"✅ Constraint added: `{constraint_label}` for object type `{obj_type}`")
        st.rerun()

    if st.session_state.object_constraints:
        st.markdown("### 📌 Current Object Constraints")
        st.json(st.session_state.object_constraints)



# --- Page 5: Object Mapping Constraints ---
def define_object_mapping_page():
    st.subheader("🔗 Object Mapping Constraints")
    if "object_mapping_constraints" not in st.session_state:
        st.session_state.object_mapping_constraints = {}

    act = st.selectbox("Activity", list(st.session_state.activities.keys()))
    obj = st.selectbox("Object Type", list(st.session_state.object_types.keys()))
    constraint_type = st.selectbox("Type", ["Min", "Max", "Exact"])
    value = st.number_input("Count", min_value=1, step=1)

    if st.button("➕ Add Mapping Constraint"):
        st.session_state.object_mapping_constraints.setdefault(act, {}).setdefault(obj, {})[constraint_type.lower()] = int(value)
        st.success("Mapping constraint added.")

    st.markdown("### Summary")
    st.json(st.session_state.object_mapping_constraints)

# --- Page 6: Generate Log ---
def generate_log_page():
    st.subheader("⚙️ Generate OCEL Log")

    #  Ensure all required session state attributes are initialized
    for key in ["activities", "object_types", "activity_constraints", "object_constraints", "object_mapping_constraints"]:
        if key not in st.session_state:
            st.session_state[key] = {}

    if st.button("🚀 Generate Log"):
        events, objects = generate_events(
            activities=st.session_state.activities,
            object_types=st.session_state.object_types,
            activity_constraints=st.session_state.activity_constraints,
            object_constraints=st.session_state.object_constraints,
            object_mapping_constraints=st.session_state.object_mapping_constraints
        )
        ocel_log = build_ocel_log(st.session_state.activities, objects, events)
        save_log(ocel_log, "generated_log.jsonocel")
        with open("generated_log.jsonocel", "rb") as f:
            st.download_button("📥 Download OCEL Log", f, file_name="generated_log.jsonocel")

    if st.button("🔄 Reset Session"):
        st.session_state.clear()
        st.rerun()

# --- Run App ---
def main():
    st.set_page_config(page_title="OCEL Generator", layout="wide")
    st.title("Ocel-Gen: Generating OCEL logs based on user-defined")

    pages = {
        "🧩 Define Activities": define_activities_page,
        "📦 Define Object Types": define_object_types_page,
        "🔒 Activity Constraints": define_activity_constraints_page,
        "📦 Object Constraints": define_object_constraints_page,
        "🔗 Object Mapping Constraints": define_object_mapping_page,
        "⚙️ Generate Log": generate_log_page
    }

    selected_page = st.sidebar.radio("Navigation", list(pages.keys()))
    pages[selected_page]()

if __name__ == "__main__":
    main()
