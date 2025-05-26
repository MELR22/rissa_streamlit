# %%
from rissa_plotter import readers, visualize
import streamlit as st
import pandas as pd

"""
path = r"c:\work_projects\Rissa\data\ontvangen_phillip\rissa-app-firebase-adminsdk-fbsvc-c66690f67d.json"
city_data = readers.open_city_table(path)
city_data.to_csv("../data/city_data.csv")
"""


# ---- Load Data ----
@st.cache_data
def load_data():
    df = pd.read_csv("../data/city_data.csv", index_col=0, parse_dates=["timestamp"])
    return df


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Chelsea+Market&display=swap');

    /* Change overall app font and color */
    .stApp, .css-1d391kg, .css-ffhzg2 {
        font-family: 'Chelsea Market', cursive !important;
        color: #000000 !important;  /* black text */
        font-size: 16px !important; /* base font size */
        background-color: #FFF8EE !important; /* optional background */
    }

    /* Titles */
    .stTitle, .stHeader, .stSubheader {
        font-family: 'Chelsea Market', cursive !important;
        color: #000000 !important;
    }

    /* Specific sizes for headers */
    h1 {
        font-size: 32px !important;
        font-weight: bold !important;
    }
    h2 {
        font-size: 24px !important;
    }
    h3 {
        font-size: 18px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


city_data = load_data()
cp = visualize.CityPlotter(city_data)

# ---- Sidebar Controls ----
st.sidebar.header("Plot options City Stations")

station_options = city_data["station"].dropna().unique()
station = st.sidebar.selectbox(
    "Select station (optional)", ["All"] + list(sorted(station_options))
)

years = city_data["timestamp"].dt.year.unique()
year = st.sidebar.selectbox("Select year (optional)", ["All"] + sorted(years))

# Convert input
year = int(year) if year != "All" else None
station = station if station != "All" else None

# ---- Plot 1: Time Series ----

st.title("Rissa's Kittiwalker Data")

st.markdown(
    "The black-legged kittiwake (Rissa tridactyla) is highly endangered and on Norway's Red List. The species is facing a very high risk of extinction in the wild. But here is the thing: we care about kittiwakes. It is no accident that “Rissa” is the name of our nonprofit. Why are kittiwakes highly endangered? Climate change, overfishing and pollution contribute to this alarming situation. While kittiwakes disappear in the wild, some individuals find refuge in coastal cities like Tromsø, where predation is lower."
)

st.markdown(
    "In close collaboration with local stakeholders, our volunteers survey the kittiwake nests in town from March to September. Most join the Kittiwalkers, a group of people who believe that coexistence is possible. They meet building owners, listen and inform, offer help and advice, and report illegal destructions if necessary. After receiving a short training, kittiwalkers use a mobile app to survey the nests, and their observations are shared with Rissa’s research partner NINA. Anyone can be a Kittiwalker and contribute to the cause in concrete ways.Kittiwalkers are citizen scientists, watchdogs and whistleblowers."
)

st.header("Development of Kittiwake population in Tromsø (Norway) over time")
fig1 = cp.plot_timeseries(year=year, station=station, figsize=(12, 6), dpi=150)
st.pyplot(fig1)
with st.expander("ℹ️ About this dataset"):
    st.markdown(
        """
        This dataset shows the number of counted Kittiwakes across multiple defined stations in the city.  
        This figures shows:
        
        - **`Visible Adults`**: All visible adult birds through time
        - **`Adults on nest`**: Adults observed sitting on a nest (potential breeding individuals) through time
        
        Counts are shown biweekly from April to October. The data is collected by volunteers (Kittiwalkers).
    """
    )

# ---- Plot 2: Compare Years ----
st.header("Compare the monitored years")
fig2 = cp.compare_years(station=station, figsize=(12, 6), dpi=150)
st.pyplot(fig2)
with st.expander("ℹ️ About this dataset"):
    st.markdown(
        """
        This dataset compares the number of counted Kittiwakes across multiple years.  
        This figures shows:
        
        - **`Visible Adults`**: All visible adult birds 
        - **`Adults on nest`**: Adults observed sitting on a nest (potential breeding individuals) 
        
        Counts are shown biweekly from April to October. The data is collected by volunteers (Kittiwalkers).
    """
    )
