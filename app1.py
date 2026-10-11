import streamlit as st

# Page configuration
st.set_page_config(
    page_title="SmartTransitAI",
    page_icon="🚌",
    layout="wide"
)

# Main heading
st.title("🚌 SmartTransitAI")
st.subheader("Festival Crowd Prediction and Bus Redistribution")

st.write(
    "A smart transport dashboard designed to help manage festival crowds "
    "by planning the redistribution of existing buses."
)

st.info(
    "Frontend Demo: Crowd levels and chart values are sample data. "
    "Prediction and AI features are not connected yet."
)

# Sidebar settings
st.sidebar.header("Festival Settings")

festival = st.sidebar.selectbox(
    "Select Festival",
    ["Temple Festival", "Pongal", "Diwali", "Other Event"]
)

expected_visitors = st.sidebar.number_input(
    "Expected Visitors",
    min_value=1000,
    max_value=1000000,
    value=50000,
    step=1000
)

time_slot = st.sidebar.selectbox(
    "Select Time Slot",
    [
        "6 AM - 9 AM",
        "9 AM - 12 PM",
        "12 PM - 3 PM",
        "3 PM - 6 PM",
        "6 PM - 9 PM",
        "9 PM - 12 AM"
    ]
)

total_buses = st.sidebar.number_input(
    "Total Existing Buses",
    min_value=1,
    max_value=500,
    value=20,
    step=1
)

# Dashboard overview
st.header("📊 Dashboard Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Expected Visitors",
        f"{expected_visitors:,}"
    )

with col2:
    st.metric(
        "Existing Bus Fleet",
        total_buses
    )

with col3:
    st.metric(
        "Selected Festival",
        festival
    )

st.caption(f"Selected time: {time_slot}")

st.divider()

# Transport locations
st.header("📍 Transport Location Overview")

locations = [
    "Main Bus Stand",
    "Temple East Stop",
    "Railway Station",
    "Town South Stop"
]

crowd_values = [90, 80, 55, 30]

crowd_levels = [
    ("High", "🔴"),
    ("High", "🔴"),
    ("Medium", "🟠"),
    ("Low", "🟢")
]

left, right = st.columns(2)

with left:
    st.subheader("Crowd Levels")

    for location, (level, icon) in zip(locations, crowd_levels):
        st.write(f"**{location}**")

        if level == "High":
            st.error(f"{icon} {level} Crowd")
        elif level == "Medium":
            st.warning(f"{icon} {level} Crowd")
        else:
            st.success(f"{icon} {level} Crowd")

with right:
    st.subheader("Sample Crowd Distribution")

    chart_data = {
        "Crowd Level": crowd_values
    }

    st.bar_chart(chart_data)

    st.caption(
        "Chart values are illustrative sample values, not actual predictions."
    )

st.divider()

# Bus redistribution
st.header("🚌 Bus Redistribution Planning")

st.write(
    "Manually assign the existing buses to different locations. "
    "The total number assigned cannot exceed the available fleet."
)

# Default allocation adds up to the total fleet
base_buses = total_buses // len(locations)
remainder = total_buses % len(locations)

default_allocations = [
    base_buses + (1 if i < remainder else 0)
    for i in range(len(locations))
]

bus_allocations = {}

for i, location in enumerate(locations):
    bus_allocations[location] = st.number_input(
        f"Buses assigned to {location}",
        min_value=0,
        max_value=int(total_buses),
        value=int(default_allocations[i]),
        step=1,
        key=f"bus_{i}"
    )

allocated_buses = sum(bus_allocations.values())

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Available Buses", total_buses)

with col2:
    st.metric("Assigned Buses", allocated_buses)

with col3:
    remaining_buses = total_buses - allocated_buses
    st.metric(
        "Unassigned Buses",
        remaining_buses
    )

if allocated_buses > total_buses:
    st.error(
        "Your allocation exceeds the available fleet. "
        "Reduce the assigned buses."
    )
elif allocated_buses < total_buses:
    st.warning(
        f"{remaining_buses} bus(es) remain unassigned."
    )
else:
    st.success(
        "All existing buses have been assigned. "
        "No additional buses have been added."
    )

# Allocation summary
st.subheader("Allocation Summary")

for location, count in bus_allocations.items():
    st.write(f"**{location}:** {count} bus(es)")

st.divider()

# Future features
st.header("🚀 Planned Features")

st.markdown(
    """
    - Live crowd data integration
    - AI-based crowd prediction
    - Automatic bus redistribution recommendations
    - Interactive transport route map
    - GenAI-generated explanations
    """
)

st.warning(
    "These features are planned for future development and are not "
    "implemented in this frontend-only version."
)

st.caption("SmartTransitAI | Hackathon Frontend Prototype")
