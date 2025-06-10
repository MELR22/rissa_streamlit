# %%
from rissa_plotter import visualize, readers, CityData, HotelData
import streamlit as st
import pandas as pd
import ast

"""
path = r"c:\work_projects\Rissa\data\ontvangen_phillip\rissa-app-firebase-adminsdk-fbsvc-c66690f67d.json"
city_data = readers.open_city_table(path)
city_data.to_csv("../data/city_data.csv")

path = r"c:\work_projects\Rissa\data\ontvangen_phillip\rissa-app-firebase-adminsdk-fbsvc-c66690f67d.json"
city_data = readers.open_hotel_table(path)
city_data.data.to_csv("c:\work_projects\Rissa\data\hotel_data.csv")
"""
# %%
DPI = 300
FIGSIZE = (12, 6)


# ---- Load Data ----
@st.cache_data
def load_data():
    years = [2023, 2024, 2025]

    city_data = pd.read_csv(
        "c:\work_projects\Rissa\data\city_data.csv",
        parse_dates=["timestamp"],
    ).set_index("timestamp")

    hotels = [
        "Hotel 1",
        "Hotel 2",
        "Hotel 3",
        "Hotel 4",
        "Hotel 5.1A",
        "Hotel 5.1B",
        "Hotel 5.1C",
        "Hotel 5.2A",
        "Hotel 5.2B",
        "Hotel 5.2C",
        "Hotel 5.3",
    ]

    hotel_data = pd.read_csv(
        "c:\work_projects\Rissa\data\hotel_data.csv",
        index_col=0,
        parse_dates=["timestamp"],
    )
    hotel_data["ledgeStatuses"] = hotel_data["ledgeStatuses"].apply(
        lambda x: ast.literal_eval(x) if isinstance(x, str) else x
    )
    return CityData(data=city_data, years=years), HotelData(
        data=hotel_data, years=years, hotels=hotels
    )


st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Chelsea+Market&display=swap');

    /* App-wide font and background */
    .stApp {
        font-family: 'Chelsea Market', cursive !important;
        color: #000000 !important;
        background-color: #FFF8EE !important;
    }
        
    /* Force tab labels text color to black */
    button[role="tab"] {
        color: black !important;
        font-family: 'Chelsea Market', cursive !important;
    }

    /* Active tab label in black (can bold it) */
    button[role="tab"][aria-selected="true"] {
        color: red !important;
        font-weight: bold !important;
    }
    /* Top bar (header) styling */
    header[data-testid="stHeader"] {
        background-color: #FFF8EE !important;
    }

    header[data-testid="stHeader"]::before {
        box-shadow: none !important;
    }

    /* Sidebar background and text */
    section[data-testid="stSidebar"] {
        background-color: #81B080 !important;
    }

    section[data-testid="stSidebar"] .css-1cpxqw2 {
        color: #000000 !important;
        font-family: 'Chelsea Market', cursive !important;
    }

    /* Titles */
    .stTitle, .stHeader, .stSubheader {
        font-family: 'Chelsea Market', cursive !important;
        color: #000000 !important;
    }

    /* Header font sizes */
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


city_data, hotel_data = load_data()

st.sidebar.header("Lay-out options")
transparent = st.sidebar.checkbox("Transparent background", value=True)

cp = visualize.CityPlotter(city_data, transparent=transparent)
hp = visualize.HotelPlotter(hotel_data, transparent=transparent)
tab1, tab2, tab3 = st.tabs(["City Stations", "Hotels", "Submissions"])

with tab1:
    st.title("City Stations")

    # ---- Sidebar Controls ----
    st.sidebar.header("Plot options City Stations")
    station_options = city_data.data["station"].dropna().unique()
    station = st.sidebar.selectbox(
        "Select station (optional)", ["All"] + list(sorted(station_options))
    )

    years = city_data.years
    year = st.sidebar.selectbox("Select year (optional)", ["All"] + sorted(years))

    # Convert input
    year = int(year) if year != "All" else None
    station = station if station != "All" else None

    st.header("Development of Kittiwake population over time")
    fig1 = cp.plot_timeseries(year=year, station=station, figsize=FIGSIZE, dpi=DPI)
    st.pyplot(fig1)
    with st.expander("ℹ️ About this figure"):
        st.markdown(
            """
            This dataset shows the number of counted Kittiwakes across multiple defined stations in the city.  
            This figure shows:
            
            - **`Visible Adults`**: All visible adult birds 
            - **`Apperently Occupied Nests`**: when one or more adults observed sitting on a nest 

            The observations are aggregated to semi-monthly values (1st and 15th of each month) by taking the max value (this may be an overestimation) at each station of all observations at a specific city station with the closest days to either 1st or 15th of the month. Missing dates are filled with zeros. 
            """
        )

    st.header("Compare the monitored years")
    fig2 = cp.compare_years(station=station, figsize=FIGSIZE, dpi=DPI)
    st.pyplot(fig2)
    with st.expander("ℹ️ About this figure"):
        st.markdown(
            """
            This dataset compares the number of counted Kittiwakes across multiple years.  
            This figures shows:
            
            - **`Visible Adults`**: All visible adult birds 
            - **`Apperently Occupied Nests`**: when one or more adults observed sitting on a nest 
            
            The observations are aggregated to semi-monthly values (1st and 15th of each month) by taking the max value (this may be an overestimation) at each station of all observations at a specific city station with the closest days to either 1st or 15th of the month. Missing dates are filled with zeros. 
        """
        )

with tab2:
    st.title("Hotels")

    st.sidebar.header("Plot options Hotels")
    hotel_options = hotel_data.hotels
    hotels = st.sidebar.multiselect(
        "Select hotel",
        ["All"] + list(sorted(hotel_options)),
        default=hotel_options[:4],
    )

    month_options = {
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
    }
    month_name = st.sidebar.selectbox(
        "Select month", ["Breeding season"] + list(month_options.keys())
    )

    if month_name == "Breeding season":
        month = None
    else:
        month = month_options[month_name]

    fig3 = hp.plot_chick_counts(figsize=FIGSIZE, dpi=DPI, hotels=hotels, month=month)
    st.pyplot(fig3)
    with st.expander("ℹ️ About this figure"):
        st.markdown(
            """
            This figure displays the number of visible Kittiwake chicks observed at the various hotels.  
            You can view chick counts for a specific month or for the entire breeding season.  
            Please note: For the current year, data may not be available for all months yet.
            """
        )
with tab3:
    st.title("Submissions")

    fig4 = cp.plot_submissions(figsize=FIGSIZE, dpi=DPI)
    st.pyplot(fig4)
    fig5 = hp.plot_submissions(figsize=FIGSIZE, dpi=DPI)
    st.pyplot(fig5)
