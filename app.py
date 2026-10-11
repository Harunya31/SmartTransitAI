
import streamlit as st

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="SmartTransitAI",
    page_icon="🚌",
    layout="wide"
)

# ==========================================
# 2. CUSTOM CSS
# ==========================================

st.markdown("""
<style>
    .main-title {
        font-size: 40px;
        font-weight: bold;
        color: #1565C0;
    }

    .subtitle {
        font-size: 18px;
        color: #555555;
    }

    .section-title {
        font-size: 25px;
        font-weight: bold;
        margin-top: 15px;
    }

    .info-card {
        background-color: #F0F7FF;
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #D0E3FF;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. HEADER
# ==========================================

st.markdown(
    '<div class="main-title">🚌 SmartTransitAI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Festival Crowd Prediction and Smart Bus Redistribution'
    '</div>',
    unsafe_allow_html=True
)

st.write("")

st.info(
    "Frontend Demonstration: This version displays sample crowd data "
    "and allows manual bus allocation. Live predictions and AI features "
    "have not been connected yet."
)

# ==========================================
# 4. SIDEBAR INPUTS
# ==========================================

st.sidebar.title("⚙️ Festival Settings")

festival = st.sidebar.selectbox(
    "Select Festival",
    [
        "Temple Festival",
        "Pongal",
        "Diwali",
        "Other Event"
    ]
)

visitors = st.sidebar.number_input(
    "Expected Festival Visitors",
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

st.sidebar.caption(
    "Only existing buses can be allocated. "
    "The total fleet cannot be increased."
)

# ==========================================
# 5. DASHBOARD OVERVIEW
# ==========================================

st.markdown(
    '<div class="section-title">📊 Dashboard Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Expected Visitors",
        value=f"{visitors:,}"
    )

with col2:
    st.metric(
        label="Existing Bus Fleet",
        value=total_buses
    )

with col3:
    st.metric(
        label="Selected Festival",
        value=festival
    )

st.caption("Selected time slot: " + time_slot)

st.divider()

# ==========================================
# 6. CROWD LEVELS BY LOCATION
# ==========================================

st.markdown(
    '<div class="section-title">📍 Crowd Levels by Location</div>',
    unsafe_allow_html=True
)

locations = [
    "Main Bus Stand",
    "Temple East Stop",
    "Railway Station",
    "Town South Stop"
]

crowd_values = [90, 80, 55, 30]

crowd_status = [
    ("High", "🔴"),
    ("High", "🔴"),
    ("Medium", "🟠"),
    ("Low", "🟢")
]

left, right = st.columns(2)

with left:
    st.subheader("Location Status")

    for location, status in zip(locations, crowd_status):
        level, icon = status

        if level == "High":
            st.error(f"{icon} {location}: {level} Crowd")
        elif level == "Medium":
            st.warning(f"{icon} {location}: {level} Crowd")
        else:
            st.success(f"{icon} {location}: {level} Crowd")

with right:
    st.subheader("Sample Crowd Distribution")

    st.bar_chart({
        "Crowd Level": crowd_values
    })

    st.caption(
        "Sample values only; these are not real-time crowd measurements."
    )

st.divider()

# ==========================================
# 7. MANUAL BUS ALLOCATION
# ==========================================

st.markdown(
    '<div class="section-title">🚌 Bus Redistribution Planning</div>',
    unsafe_allow_html=True
)

st.write(
    "Assign the existing buses to different locations. "
    "The system checks whether your allocation stays within the available fleet."
)

# Distribute default values so their sum equals the fleet size.
base = int(total_buses) // len(locations)
remainder = int(total_buses) % len(locations)

default_allocations = [
    base + (1 if index < remainder else 0)
    for index in range(len(locations))
]

allocations = []

for index, location in enumerate(locations):
    buses = st.number_input(
        label=f"Buses assigned to {location}",
        min_value=0,
        max_value=int(total_buses),
        value=default_allocations[index],
        step=1,
        key=f"bus_allocation_{index}"
    )

    allocations.append(int(buses))

assigned_buses = sum(allocations)
unassigned_buses = int(total_buses) - assigned_buses

# ==========================================
# 8. ALLOCATION SUMMARY
# ==========================================

st.subheader("📋 Allocation Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Available Buses",
        int(total_buses)
    )

with col2:
    st.metric(
        "Assigned Buses",
        assigned_buses
    )

with col3:
    st.metric(
        "Unassigned Buses",
        unassigned_buses
    )

if assigned_buses > total_buses:
    st.error(
        "Allocation exceeds the existing fleet. "
        "Reduce the number of buses assigned."
    )

elif assigned_buses < total_buses:
    st.warning(
        f"{unassigned_buses} bus(es) remain unassigned."
    )

else:
    st.success(
        "All existing buses have been allocated. "
        "No additional buses have been added."
    )

# ==========================================
# 9. ALLOCATION TABLE
# ==========================================

st.subheader("Bus Allocation by Location")

st.table([
    {
        "Location": location,
        "Assigned Buses": buses
    }
    for location, buses in zip(locations, allocations)
])

st.subheader("Visual Bus Distribution")

st.bar_chart({
    "Assigned Buses": {
        location: buses
        for location, buses in zip(locations, allocations)
    }
})

st.divider()

# ==========================================
# 10. FUTURE FEATURES
# ==========================================

st.markdown(
    '<div class="section-title">🚀 Planned Features</div>',
    unsafe_allow_html=True
)

feature_col1, feature_col2 = st.columns(2)

with feature_col1:
    st.markdown("""
    **Crowd Management**
    - Real-time crowd monitoring
    - Passenger demand prediction
    - High-crowd location alerts
    """)

with feature_col2:
    st.markdown("""
    **Smart Transportation**
    - Automatic bus recommendations
    - Route optimization
    - GenAI-generated explanations
    """)

st.warning(
    "These features are planned for future development. "
    "They are not implemented in this frontend-only version."
)

# ==========================================
# 11. FOOTER
# ==========================================

st.divider()

st.caption(
    "SmartTransitAI | Hackathon Prototype | Frontend Only"
)

