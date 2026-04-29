import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Hockey Match Dashboard",
    page_icon="🏑",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #f7fbff 0%, #eef5fb 100%);
    color: #132238;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #102a43;
    margin-bottom: 5px;
}

.sub-title {
    font-size: 18px;
    color: #52606d;
    margin-bottom: 25px;
}

.card {
    background-color: white;
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0px 4px 16px rgba(0,0,0,0.08);
    margin-bottom: 28px;
}

.image-bubble {
    background-color: #ffffff;
    padding: 18px;
    border-radius: 18px;
    border-left: 6px solid #2f80ed;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.08);
    margin-bottom: 30px;
}

.section-title {
    font-size: 26px;
    font-weight: 700;
    color: #102a43;
    margin-top: 25px;
    margin-bottom: 16px;
}

.small-note {
    color: #52606d;
    font-size: 15px;
}
</style>
""", unsafe_allow_html=True)

DATA_FILE = Path("hockey_dashboard_data.xlsx")
IMAGE_DIR = Path("images")

@st.cache_data
def load_data():
    if not DATA_FILE.exists():
        st.error("No Excel data file found. Make sure hockey_dashboard_data.xlsx is in the same folder as app.py.")
        st.stop()

    df = pd.read_excel(DATA_FILE)
    df.columns = df.columns.str.strip()
    return df

df = load_data()

def find_column(possible_names):
    for name in possible_names:
        for col in df.columns:
            if col.lower().strip() == name.lower().strip():
                return col
    return None

team_col = find_column(["Team", "Side"])
event_col = find_column(["Event", "Action", "Type"])
minute_col = find_column(["Minute", "Time", "Match Minute"])
x_col = find_column(["X", "x", "X Position", "X Coordinate"])
y_col = find_column(["Y", "y", "Y Position", "Y Coordinate"])
outcome_col = find_column(["Outcome", "Result", "Success"])
match_col = find_column(["Match", "Game", "Fixture"])

score_col = find_column(["Final Score", "Score"])
venue_col = find_column(["Venue", "Location"])
date_col = find_column(["Date", "Match Date"])
possession_col = find_column(["Possession", "Possession %"])
shots_col = find_column(["Shots on Target", "Shots"])
pass_accuracy_col = find_column(["Pass Accuracy", "Pass Accuracy %"])
circle_entries_col = find_column(["Circle Entries"])

st.markdown('<div class="main-title">🏑 Hockey Match Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">A comparative dashboard design exploring how data visualisation and contextual match images support hockey understanding.</div>',
    unsafe_allow_html=True
)

st.sidebar.title("Dashboard Controls")

dashboard_choice = st.sidebar.radio(
    "Choose Dashboard",
    ["Dashboard A: Standard Data Dashboard", "Dashboard B: Enhanced Visual Dashboard"]
)

filtered_df = df.copy()

if match_col:
    matches = sorted(df[match_col].dropna().unique().tolist())
    selected_match = st.sidebar.selectbox("Select Match", matches)
    filtered_df = filtered_df[filtered_df[match_col] == selected_match]
else:
    selected_match = "Selected Match"
    st.sidebar.warning("No Match column found in the data.")

st.sidebar.markdown("---")
st.sidebar.info(
    "Use the match dropdown to compare different hockey matches. Dashboard B adds images and explanations to support understanding."
)

# MATCH OVERVIEW

if not filtered_df.empty:
    overview_row = filtered_df.iloc[0]

    score = overview_row[score_col] if score_col else "N/A"
    venue = overview_row[venue_col] if venue_col else "N/A"
    date = overview_row[date_col] if date_col else "N/A"

    possession = overview_row[possession_col] if possession_col else "N/A"
    shots = overview_row[shots_col] if shots_col else "N/A"
    pass_accuracy = overview_row[pass_accuracy_col] if pass_accuracy_col else "N/A"
    circle_entries = overview_row[circle_entries_col] if circle_entries_col else "N/A"

    st.markdown('<div class="section-title">Match Overview</div>', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card">
        <p><b>{selected_match}</b> | Final score: <b>{score}</b> | Venue: <b>{venue}</b> | Date: <b>{date}</b></p>
        <p>This prototype presents key hockey performance indicators and highlights how visual context can support interpretation of fast-paced match events for less experienced viewers.</p>
    </div>
    """, unsafe_allow_html=True)

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    with kpi1:
        st.metric("Possession", f"{possession}%")

    with kpi2:
        st.metric("Shots on Target", shots)

    with kpi3:
        st.metric("Pass Accuracy", f"{pass_accuracy}%")

    with kpi4:
        st.metric("Circle Entries", circle_entries)

    st.markdown("<br>", unsafe_allow_html=True)

# CHARTS SECTION

st.markdown('<div class="section-title">Performance Charts</div>', unsafe_allow_html=True)

chart_col1, chart_col2 = st.columns(2, gap="large")

with chart_col1:
    if event_col:
        event_counts = filtered_df[event_col].value_counts().reset_index()
        event_counts.columns = ["Event", "Count"]

        fig = px.bar(
            event_counts,
            x="Event",
            y="Count",
            title="Event Frequency",
            text="Count"
        )
        fig.update_layout(height=430, margin=dict(l=30, r=30, t=60, b=80))
        st.plotly_chart(fig, use_container_width=True, key="event_frequency_chart")
    else:
        st.warning("No event/action column found.")

with chart_col2:
    if outcome_col:
        outcome_counts = filtered_df[outcome_col].value_counts().reset_index()
        outcome_counts.columns = ["Outcome", "Count"]

        fig = px.pie(
            outcome_counts,
            names="Outcome",
            values="Count",
            title="Outcome Distribution",
            hole=0.45
        )
        fig.update_layout(height=430, margin=dict(l=30, r=30, t=60, b=40))
        st.plotly_chart(fig, use_container_width=True, key="outcome_distribution_chart")
    else:
        st.warning("No outcome/result column found.")

chart_col3, chart_col4 = st.columns(2, gap="large")

with chart_col3:
    if team_col and event_col:
        team_events = filtered_df.groupby(team_col).size().reset_index(name="Count")

        fig = px.bar(
            team_events,
            x=team_col,
            y="Count",
            title="Team Event Comparison",
            text="Count"
        )
        fig.update_layout(height=430, margin=dict(l=30, r=30, t=60, b=80))
        st.plotly_chart(fig, use_container_width=True, key="team_event_chart")
    else:
        st.warning("Team or event column not found.")

with chart_col4:
    if minute_col and event_col:
        timeline = filtered_df.groupby(minute_col).size().reset_index(name="Events")

        fig = px.line(
            timeline,
            x=minute_col,
            y="Events",
            markers=True,
            title="Match Event Timeline"
        )
        fig.update_layout(height=430, margin=dict(l=30, r=30, t=60, b=60))
        st.plotly_chart(fig, use_container_width=True, key="event_timeline_chart")
    else:
        st.warning("Minute/time column not found.")


# HEATMAP

st.markdown('<div class="section-title">Pitch Heatmap</div>', unsafe_allow_html=True)

if x_col and y_col:
    fig = px.density_heatmap(
        filtered_df,
        x=x_col,
        y=y_col,
        nbinsx=20,
        nbinsy=12,
        title="Action Location Heatmap",
        labels={x_col: "Pitch X Position", y_col: "Pitch Y Position"}
    )

    fig.update_layout(
        height=560,
        xaxis_title="Pitch Length",
        yaxis_title="Pitch Width",
        margin=dict(l=40, r=40, t=70, b=50)
    )

    st.plotly_chart(fig, use_container_width=True, key="pitch_heatmap")
else:
    st.warning(
        "Heatmap needs X and Y position columns in your Excel file. "
        "Add columns called X and Y if you want the heatmap to work."
    )


# DASHBOARD B IMAGE SECTION

if dashboard_choice == "Dashboard B: Enhanced Visual Dashboard":

    st.markdown('<div class="section-title">Visual Match Explanations</div>', unsafe_allow_html=True)

    st.markdown(
        '<p class="small-note">These images provide visual context to help users connect the statistical dashboard with real hockey situations.</p>',
        unsafe_allow_html=True
    )

    image_data = [
        {
            "file": "tackling.JPG",
            "title": "Defensive Tackle",
            "text": "This image shows a defensive tackle, where a player attempts to regain possession from the opposition. Tackling is important because it disrupts attacking play and can quickly change the momentum of a match."
        },
        {
            "file": "penalty_flick.JPG",
            "title": "Penalty Flick",
            "text": "This image shows a penalty flick situation. Penalty flicks are key moments because they provide a direct scoring opportunity and can strongly influence the final result of a match."
        },
        {
            "file": "injection.JPG",
            "title": "Ball Control and Injection",
            "text": "This image highlights controlled ball movement during play. Good ball control is important because it helps players retain possession, create passing options and build attacking pressure."
        },
        {
            "file": "one_v_one.JPG",
            "title": "1v1 Attacking Scenario",
            "text": "This image shows a 1v1 situation, where an attacker directly faces a defender. These moments are important because they can create space, break defensive structure and lead to goal-scoring chances."
        }
    ]

    for item in image_data:
        img_path = IMAGE_DIR / item["file"]

        img_col, text_col = st.columns([1.2, 1], gap="large")

        with img_col:
            if img_path.exists():
                st.image(str(img_path), use_container_width=True)
            else:
                st.error(f"Missing image: {img_path}")

        with text_col:
            st.markdown(f"""
            <div class="image-bubble">
                <h3>{item["title"]}</h3>
                <p>{item["text"]}</p>
            </div>
            """, unsafe_allow_html=True)


# DATA TABLE

with st.expander("View anonymised match data table"):
    st.dataframe(filtered_df, use_container_width=True)

st.markdown("---")
st.caption(
    "Dashboard A presents a standard statistics-based view. Dashboard B adds visual explanations to support user understanding and engagement. Data is presented at match/team level to protect participant anonymity."
)