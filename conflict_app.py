import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Putting a sidebar title 
st.sidebar.title("Upload file")
upload_file = st.sidebar.file_uploader("Choose csv file", type="csv")

if upload_file is not None:
    conflict_df = pd.read_csv(upload_file)
    # st.dataframe(df)
    
    # sidebar code
    no_events = len(conflict_df)
    citizenship_counts = conflict_df["citizenship"].value_counts()
    event_location_region = conflict_df["event_location_region"].value_counts()
    hostility_counts = conflict_df[conflict_df["took_part_in_the_hostilities"] == "Yes"].value_counts()
    no_hostility_counts = conflict_df[conflict_df["took_part_in_the_hostilities"] == "No"].value_counts()
    
    st.sidebar.write(f"No. of events: {no_events}")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.subheader("Citizenship counts")
        st.write(citizenship_counts)
    with col2:
        st.subheader("Event Location Region")
        st.write(event_location_region)
        
    col3, col4 = st.sidebar.columns(2)
    with col3:
        st.write(no_hostility_counts)
        
    weapons_counts = conflict_df["ammunition"].value_counts()
    st.sidebar.write(f"Weapon counts {weapons_counts}")
    
    # Data Analysis part
    st.title("Israel Palestine Conflict Analysis")
    st.write("Dataset Sample", conflict_df)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Type of injuries")
        injury_type = conflict_df["type_of_injury"].value_counts()
        st.bar_chart(injury_type)
    with col2:
        st.subheader("Participation in Hostilities by Gender")
        hostility_by_gender = conflict_df.groupby("gender")["took_part_in_the_hostilities"].value_counts().reset_index(name="count")
        # Visualizing using a grouped bar chart
        fig_1 = px.bar(hostility_by_gender, x="took_part_in_the_hostilities", y="count", color="gender", barmode="group", labels={"count": "Gender", "took_part_in_the_hostilities": "Hostility"})
        st.plotly_chart(fig_1, use_container_width=True, theme=None)
    
    st.subheader("Event Location Region Count")
    elr = conflict_df["event_location_region"].value_counts().reset_index()
    elr.columns = ["region", "count"]  # Ensure correct column names
    # Visualizing using a pie chart with correct columns and unique key
    fig_2 = px.pie(elr, values="count", names="region")
    st.plotly_chart(fig_2, use_container_width=True, theme=None, key="event_location_pie")
    
    st.subheader("Resident count by region")
    place_of_residence_per_region = conflict_df.groupby("event_location_region")["place_of_residence"].nunique()
    fig_3, ax = plt.subplots()
    ax.pie(place_of_residence_per_region, labels=place_of_residence_per_region.index, autopct="%1.1f%%")
    st.pyplot(fig_3)
    
    st.subheader("Average age by region")
    average_age_by_reg = conflict_df.groupby("event_location_region")["age"].mean()
    st.bar_chart(average_age_by_reg)
    
    st.subheader("Incident count by citizenship")
    incident_by_citizenship = conflict_df.groupby("citizenship").size().reset_index()
    incident_by_citizenship.columns = ["citizenship", "incident count"]
    # Visualizing using a donut chart
    fig_4 = px.pie(incident_by_citizenship, values="incident count", names="citizenship", hole=0.4)
    st.plotly_chart(fig_4, use_container_width=True, theme=None, key="citizenship")
    
    st.subheader("Kill count by gender")
    kill_count = conflict_df.groupby("gender")["killed_by"].value_counts().reset_index(name="count")
    gender_inc = kill_count["gender"] + "-" + kill_count["killed_by"]
    # Visualizing using a sliced pie chart
    fig_5 = px.pie(kill_count, values="count", names=gender_inc, color="killed_by")
    fig_5.update_traces(pull=[0.2, 0, 0, 0.1, 0.3, 0.1])
    st.plotly_chart(fig_5, use_container_width=True, theme=None)
    
    def avg_based_on_gender():
        conflict_df["gender"] = conflict_df["gender"].replace({"M": "Male", "F": "Female"})
        gender = conflict_df["gender"].unique().tolist()
        gender_select = st.selectbox("Select gender: ",gender)
        st.subheader(f"Kill count based on {gender_select}")
        genders = conflict_df[conflict_df["gender"] == gender_select]
        event_loc = genders.groupby("gender")["event_location_district"].value_counts().reset_index(name="count")
        # Visualizing using a donut chart
        gender_count = event_loc["gender"] + "-" + event_loc["event_location_district"]
        fig_5 = px.pie(event_loc, names=gender_count, values="count", color="event_location_district", hole=0.3)
        st.plotly_chart(fig_5, use_container_width=True, theme=None)
    avg_based_on_gender()
    
    # Time based events
    conflict_df["date_of_event"] = pd.to_datetime(conflict_df["date_of_event"])
    # Getting the year
    conflict_df["year"] = conflict_df["date_of_event"].dt.year
    # Getting the month
    conflict_df["month"] = conflict_df["date_of_event"].dt.month_name()
    # Grouping by year and month
    time_event = conflict_df.groupby(["year", "month"]).size().reset_index(name="incident count")
    time_event["year-month"] = time_event["month"] + "-" + time_event["year"].astype(str)
    st.subheader("Time-Based Events")
    st.line_chart(time_event.set_index("year-month")["incident count"])