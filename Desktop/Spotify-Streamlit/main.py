import pandas as pd
import streamlit as st
import os
import plotly.express as px

st.set_page_config(layout="wide", page_title="Spotify Dashboard")

def format_large_number(number, color=None):
    """
    Formats a large number into a more readable format (e.g., millions, billions).
    """
    if number is None:
        return "No data"

    abs_number = abs(number)
    
    if abs_number >= 1_000_000_000:
        formatted_val = f"{number / 1_000_000_000:.2f}B"
    elif abs_number >= 1_000_000:
        formatted_val = f"{number / 1_000_000:.2f}M"
    elif abs_number >= 1_000:
        formatted_val = f"{number / 1_000:.1f}K"
    else:
        formatted_val = f"{number:,}"
    
    if color:
        return f"<span style='color: {color};'>{formatted_val}</span>"
    return formatted_val


def format_percentage(value, color='#1db954'):
    """
    Formats a percentage value with a specific color.
    """
    if value is None:
        return "No data"
    
    return f"<span style='color: {color};'>{value}%</span>"

def calculate_top_song_vs_avg(top_song_streams, average_streams_per_year):
    """
    Calculates the percentage difference of a top song's streams
    compared to the average streams.
    """
    if average_streams_per_year != 0:
        return (top_song_streams - average_streams_per_year) / average_streams_per_year
    else:
        return None
    
def format_kpi_value(top_song_vs_avg_val):
    """
    Formats a value based on a comparison to an average,
    adding a percentage and a colored up or down arrow.
    """
    if top_song_vs_avg_val is None:
        return "No data"
    elif top_song_vs_avg_val > 0:
        return f"<span style='color: #1db954;'>{top_song_vs_avg_val:.1%} ▲</span>"
    else:
        return f"<span style='color: red;'>{top_song_vs_avg_val:.1%} ▼</span>"

try:
    spotify_df = pd.DataFrame(pd.read_excel(os.path.join(os.getcwd(),"dataSet","spotify.xlsx")))
    spotify_df = spotify_df.drop(574, axis=0)
except FileNotFoundError:
    st.error("Error: 'spotify.xlsx' not found in the 'dataSet' folder.")
    st.stop()

spotify_df_sorted = spotify_df.sort_values(by='streams', ascending=False)
average_streams = spotify_df_sorted['streams'].mean()
top_song_row = spotify_df_sorted.iloc[0]
top_song_name = top_song_row['track_name']
top_song_streams = top_song_row['streams']

st.markdown("""
<style>

    .stApp {
    background-color: #121212;
    color: white;
    }
    
    [data-testid="stSidebar"] {
        background-color: #000000;
        border-right: 1px solid #1db954;
        padding-top: 2rem;
    }

    a.sidebar-link {
        color: white;
        text-decoration: none;
        font-size: 1.1rem;
        font-weight: bold;
        display: block;
        padding: 0.5rem 1rem;
        margin-bottom: 0.5rem;
        transition: color 0.3s;
    }
    a.sidebar-link:hover {
        color: #1db954;
        text-decoration: none;
    }
    
    .css-hi6a2p {
        visibility: hidden;
    }
            
[data-testid="stHorizontalBlock"] > div {
    align-items: flex-start !important;
}

.bento-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
    gap: 1rem;
    margin: 0;
}

.bento-card {
    border-radius: 8px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 0.75rem 1rem;
    min-height: 110px;

    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
    text-align: center;
}

.bento-label {
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.6);
    margin: 0 0 0.25rem 0;
}

.bento-value {
    font-size: 2.25rem;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<a href='#track-details' class='sidebar-link'>Track Details <span style='color: white; margin-left: 10px;'>\u25B8</span></a>", unsafe_allow_html=True)
    st.markdown("<a href='#audio-features' class='sidebar-link'>Audio Features <span style='color: white; margin-left: 10px;'>\u25B8</span></a>", unsafe_allow_html=True)
    st.markdown("<a href='#most-streamed-tracks' class='sidebar-link'>Most Streamed Tracks <span style='color: white; margin-left: 10px;'>\u25B8</span></a>", unsafe_allow_html=True)
    st.markdown("<a href='#overall-dataset-summary' class='sidebar-link'>Overall Summary <span style='color: white; margin-left: 10px;'>\u25B8</span></a>", unsafe_allow_html=True)
    st.markdown("<a href='#track-releases-over-time' class='sidebar-link'>Releases Over Time <span style='color: white; margin-left: 10px;'>\u25B8</span></a>", unsafe_allow_html=True)

st.title("Spotify DashBoard")
st.divider()

st.subheader("Track Details")
st.caption("Select any track from the dropdown to see its specific details and core metrics, including its total streams and release date.")

selected_track = st.selectbox("Select a track to view details:", spotify_df_sorted['track_name'])
track_row = spotify_df_sorted[spotify_df_sorted["track_name"] == selected_track].iloc[0]

main_col_image, main_col_details = st.columns([1, 2])

with main_col_image:
    st.markdown(
        f"""<img src="{track_row['cover_url']}"
                  style="width:100%;border-radius:8px;margin:0;">""",
        unsafe_allow_html=True
    )

with main_col_details:
    st.markdown("<div class='bento-grid'>", unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="bento-card">
            <div class="bento-label">Track Name</div>
            <div class="bento-value" style="font-size: 1.5rem;">{track_row['track_name']}</div>
        </div>
    """, unsafe_allow_html=True)

    first_artist = str(track_row['artist(s)_name']).split(',')[0].strip()
    st.markdown(f"""
        <div class="bento-card">
            <div class="bento-label">First Artist</div>
            <div class="bento-value" style="font-size: 1.5rem;">{first_artist}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="bento-card">
            <div class="bento-label">Artist Count</div>
            <div class="bento-value">{len(str(track_row['artist(s)_name']).split(','))}</div>
        </div>
    """, unsafe_allow_html=True)

    formatted_streams = format_large_number(track_row['streams'], color='#1db954')
    st.markdown(f"""
        <div class="bento-card">
            <div class="bento-label">Streams</div>
            <div class="bento-value">{formatted_streams}</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="bento-card">
            <div class="bento-label">Date</div>
            <div class="bento-value">{track_row['released_year']}-{track_row['released_month']}-{track_row['released_day']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

st.divider()

st.subheader("Audio Features")
st.caption("These metrics show the unique acoustic characteristics of the selected track, with higher percentages indicating a greater presence of that feature.")

col_a, col_b, col_c, col_d, col_e = st.columns(5)

with col_a:
    with st.container(border=True):
        st.markdown(f"<div>Acousticness</div><div style='font-size: 2.25rem;'>{format_percentage(track_row['acousticness_%'])}</div>", unsafe_allow_html=True)

with col_b:
    with st.container(border=True):
        st.markdown(f"<div>Danceability</div><div style='font-size: 2.25rem;'>{format_percentage(track_row['danceability_%'])}</div>", unsafe_allow_html=True)

with col_c:
    with st.container(border=True):
        st.markdown(f"<div>Liveness</div><div style='font-size: 2.25rem;'>{format_percentage(track_row['liveness_%'])}</div>", unsafe_allow_html=True)

with col_d:
    with st.container(border=True):
        st.markdown(f"<div>Speechiness</div><div style='font-size: 2.25rem;'>{format_percentage(track_row['speechiness_%'])}</div>", unsafe_allow_html=True)

with col_e:
    with st.container(border=True):
        st.markdown(f"<div>Valence</div><div style='font-size: 2.25rem;'>{format_percentage(track_row['valence_%'])}</div>", unsafe_allow_html=True)


st.divider()

st.subheader("Most Streamed Tracks")
st.caption("This chart displays the top 10 most streamed tracks. Use the slider to filter the list by a specific release date range.")

spotify_df['release_date'] = pd.to_datetime({
    'year': spotify_df['released_year'],
    'month': spotify_df['released_month'],
    'day': spotify_df['released_day']
})

min_Date = spotify_df["release_date"].min().date()
max_Date = spotify_df["release_date"].max().date()
date_range = st.slider(
    "Select a Date Range",
    min_value=min_Date,
    max_value=max_Date,
    value=(min_Date, max_Date),
    format="YYYY-MM-DD"
)

filtered_df = spotify_df[
    (spotify_df['release_date'].dt.date >= date_range[0]) & (spotify_df['release_date'].dt.date <= date_range[1])
]

if not filtered_df.empty:
    filtered_df_sorted = filtered_df.sort_values(by="streams", ascending=False)

fig_bar = px.bar(
    filtered_df_sorted.head(10),
    x='streams',
    y='track_name',
    orientation='h',
    title='Top 10 Most Streamed Tracks',
    labels={'streams': "Streams", 'track_name': ''},
    color_discrete_sequence=['#1db954']
)

fig_bar.update_traces(
    marker_color='#1db954',
    text=filtered_df_sorted.head(10)['track_name'],
    textposition='inside',
    insidetextanchor='end',
    insidetextfont={
        'color': "#2c2d2d",
        'size': 12,
        'family': 'sans',
        'weight': 600
    }
)

fig_bar.update_layout(
    yaxis=dict(
        showticklabels=False
    ),
    xaxis=dict(
        showgrid=False,
        zeroline=False
    ),
    title_font_color='white',
    plot_bgcolor='#121212',
    paper_bgcolor='#121212',
    font_color='white'
)

fig_bar.update_yaxes(autorange="reversed")
st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

st.subheader("Overall Dataset Summary")
st.caption("These key performance indicators (KPIs) provide a high-level overview of the entire dataset. The 'Top Song vs. Average' metric shows how much the most streamed song exceeds the average streams across all songs.")

raw_kpi_value = calculate_top_song_vs_avg(top_song_streams, average_streams)
formatted_kpi = format_kpi_value(raw_kpi_value)
formatted_average_streams = format_large_number(average_streams)
formatted_top_song_streams = format_large_number(top_song_streams)

col_x, col_y, col_z = st.columns(3)

with col_x:
    with st.container(border=True):
        st.metric(
            label="Average Streams (All Songs)",
            value=formatted_average_streams
        )

with col_y:
    with st.container(border=True):
        st.metric(
            label=f"Streams for Top Song: {top_song_name}",
            value=formatted_top_song_streams
        )

with col_z:
    with st.container(border=True):
        st.markdown(f"<div>Top Song vs. Average</div>",unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: 2.6rem;'>{formatted_kpi}</div>",unsafe_allow_html=True)

st.divider()

st.subheader("Track Releases Over Time")
st.caption("This line graph visualizes the number of tracks released per year, revealing trends in music production over time.")

tracks_per_year = spotify_df.groupby('released_year')['track_name'].count().reset_index()
tracks_per_year.rename(columns={'track_name': 'track_count'}, inplace=True)

fig_line = px.line(
    tracks_per_year,
    x='released_year',
    y='track_count',
    title='Number of Tracks Released Per Year',
    labels={'released_year': 'Year', 'track_count': 'Number of Tracks'},
    color_discrete_sequence=['#1DB954']
)

fig_line.update_traces(
    mode="lines+markers",
    marker_line_color='white',
    hovertemplate="<br>Date:%{x}<br>Number of Tracks: %{y}<extra></extra>"
)
fig_line.update_layout(hovermode="x unified",title_font_color='white',
    plot_bgcolor='#121212',
    paper_bgcolor='#121212',
    font_color='white',
    xaxis=dict(showgrid=False, zeroline=False),
    yaxis=dict(showgrid=False, zeroline=False))

st.plotly_chart(fig_line, use_container_width=True)

st.divider()

st.markdown("""
<style>
.signature-container {
    display:flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    font-size: 14px;
    color: white;
    font-style: italic;
    margin: 0;
    padding: 0;
}
</style>
<div class="signature-container">
    Dashboard created by Srivalli Krishna Nandini Velamuri
</div>
""", unsafe_allow_html=True)