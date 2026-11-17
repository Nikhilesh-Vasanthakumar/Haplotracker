#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 10:29:19 2023
Haplogroup Tracker.py

@author: Nikhilesh Vasanthakumar
Description: This script is used to track the movement of haplogroups over time using streamlit and plotly libraries.
The script takes the data from the excel file and plots the haplogroups on the map based on the user input.
The user can select the haplogroups to be plotted on the map and the map type.
The user can also select the haplogroup to animate and the script will animate the haplogroup movement over time.

Website Link:https://nikhilesh-vasanthakumar-haplotracker-haplogroup-tracker-wqf8g7.streamlit.app/

Functions:
    load_data(): Reads the Excel file once and caches it.
    prepare(mode): Filters the data for one mode (MtDNA, MtDNA-Male, MtDNA-Female, Y-Chromosome),
        drops rows without coordinates, dates or a haplogroup call, and converts dates to "years ago".
    overview_figure(select, map_type): Map of every sample in the selected haplogroups.
    animation_figure(animate_data, center, map_type): Animated trace of one haplogroup, oldest sample first.
    show_maps(mtgeo): The widgets and maps shown for the chosen mode.
Procedure:
1.Import the required libraries
2.Read the data from the excel file which acts as the database.
3.Filter the data based on the user input.
4.Plot the haplogroups on the map based on the user input.
5.Create static traces based on the groups selected.
6.Create frames based on the longitude and latitude of the haplogroups selected.
7.Create the animation based on the frames created.
User Guide:
1.User selects mode of the haplogroup ie. the mtdna mode or y-chromosome mode.
2.User selects the Haplogroups that they want to visualize.
3.User selects the map type.
4.User selects the haplogroup to animate.
5.Press the play button to animate the haplogroup movement over time.

    """
import datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

APP_DIR = Path(__file__).resolve().parent
# Change this to use your own data. It must have the same column names as Eurasian.xlsx.
DATA_FILE = APP_DIR / "Data" / "Eurasian.xlsx"
LOGO_FILE = APP_DIR / "assests" / "LU.png"

DATE_COL = ("Date mean in BP in years before 1950 CE [OxCal mu for a direct radiocarbon date, "
            "and average of range for a contextual date]")
MT_COL = "mtDNA haplogroup if ≥2 or published"
Y_COL = "Y haplogroup  in ISOGG v15.73 notation (automatically called)"
# Mode -> (haplogroup column, sex to keep or None for everyone)
MODES = {
    "MtDNA": (MT_COL, None),
    "MtDNA-Male": (MT_COL, "M"),
    "MtDNA-Female": (MT_COL, "F"),
    "Y-Chromosome": (Y_COL, "M"),
}
USGS_LAYER = {
    "below": "traces",
    "sourcetype": "raster",
    "sourceattribution": "United States Geological Survey",
    "source": [
        "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
    ],
}

st.set_page_config(page_title="HaploTracker", page_icon=":dna:", layout="wide", initial_sidebar_state="expanded")
# Hiding the main menu and footer
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner="Loading data...")
def load_data(path=DATA_FILE):
    """Read the spreadsheet once; later reruns reuse the cached copy."""
    return pd.read_excel(path)


def is_called(value):
    """True for a real haplogroup call, False for missing ones such as '..', 'n/a (<2x)' or 'n/a (female)'."""
    if not isinstance(value, str):
        return False
    value = value.strip()
    return value not in ("", "..") and not value.startswith("n/a")


@st.cache_data
def prepare(mode):
    """Rows for one mode with the columns Lat, Long, mtdna (the haplogroup), Date (years ago) and Country."""
    column, sex = MODES[mode]
    data = load_data()
    if sex is not None:
        data = data[data["Sex"] == sex]
    mtgeo = data[["Lat.", "Long.", column, DATE_COL, "Country"]].rename(
        columns={"Lat.": "Lat", "Long.": "Long", column: "mtdna", DATE_COL: "Date"})
    for col in ("Lat", "Long", "Date"):
        mtgeo[col] = pd.to_numeric(mtgeo[col], errors="coerce")  # '..' becomes NaN
    mtgeo = mtgeo.dropna(subset=["Lat", "Long", "Date"])
    mtgeo = mtgeo[mtgeo["mtdna"].map(is_called)].copy()
    # Dates are years before 1950 (BP); convert them to years before today.
    mtgeo["Date"] = (mtgeo["Date"] + (datetime.date.today().year - 1950)).astype(int)
    return mtgeo


def overview_figure(select, map_type):
    """Every sample in the selected haplogroups, coloured by haplogroup."""
    if map_type == "Natural Earth":
        fig = px.scatter_geo(select, lat="Lat", lon="Long", color="mtdna", hover_name="hover",
                             projection="natural earth", color_discrete_sequence=px.colors.qualitative.Set1)
        fig.update_geos(showland=True, landcolor="LightGreen", showocean=True, oceancolor="LightBlue",
                        showrivers=True, rivercolor="Blue", projection_type="natural earth",
                        fitbounds="locations")
        return fig
    fig = px.scatter_map(select, lat="Lat", lon="Long", color="mtdna", hover_name="hover", zoom=1,
                         color_discrete_sequence=px.colors.qualitative.Set1)
    fig.update_traces(marker=dict(size=10))
    fig.update_layout(map_style="white-bg", map_layers=[USGS_LAYER])
    return fig


def animation_figure(animate_data, center, map_type):
    """Animated trace of one haplogroup through its samples, oldest first."""
    lat, lon = list(animate_data["Lat"]), list(animate_data["Long"])
    names = list(animate_data["mtdna"])
    hover = animate_data["hover"]
    if map_type == "Natural Earth":
        map_layout = dict(style="carto-positron")
    else:
        map_layout = dict(style="white-bg", layers=[USGS_LAYER])
    map_layout.update(center=center, zoom=1, bearing=0, pitch=0)

    fig = go.Figure(
        data=[
            go.Scattermap(lat=lat, lon=lon, mode="lines", line=dict(width=2, color="blue"),
                          name="Haplogroup Movement", hovertext=hover),
            go.Scattermap(lat=lat[:1], lon=lon[:1], mode="lines", line=dict(width=2, color="orange"),
                          name="Movement"),
            go.Scattermap(lat=lat, lon=lon, mode="markers", marker=dict(size=6, color="red"),
                          name="Haplogroup locations", hovertext=hover),
            go.Scattermap(lat=lat[:1], lon=lon[:1], mode="markers", marker=dict(size=10, color="red"),
                          name="Current location", text=names[:1]),
        ],
        layout=go.Layout(
            title_text="Movement of selected Haplogroup over history",
            map=map_layout,
            updatemenus=[dict(type="buttons", buttons=[dict(label="Play", method="animate", args=[None])])],
        ),
        # Each frame grows the orange trail (trace 1) and moves the current-location marker (trace 3).
        frames=[
            go.Frame(
                data=[
                    go.Scattermap(lat=lat[:k + 1], lon=lon[:k + 1], mode="lines",
                                  line=dict(width=2, color="orange")),
                    go.Scattermap(lat=[lat[k]], lon=[lon[k]], mode="markers",
                                  marker=dict(color="red", size=10), text=[names[k]]),
                ],
                traces=[1, 3],
            )
            for k in range(len(lat))
        ],
    )
    return fig


def show_maps(mtgeo):
    """Haplogroup picker, overview map, and the animation for one haplogroup."""
    try:
        option = st.multiselect(label="Select the haplogroup", options=mtgeo["mtdna"].unique())
        if not option:
            st.error("Please select atleast one haplogroup")
            return
        select = mtgeo[mtgeo["mtdna"].isin(option)].copy()
        select["hover"] = select["Country"].str.cat("\t" + select["Date"].astype(str) + " years ago")
        map_type = st.selectbox("Select map type", options=["USGS", "Natural Earth"])
        st.plotly_chart(overview_figure(select, map_type))

        select = select.sort_values(by="Date", ascending=False)  # oldest first
        animate_select = st.selectbox("Select haplogroup to animate", options=option)
        animate_data = select[select["mtdna"] == animate_select]
        if len(animate_data) < 2:
            st.info(f"{animate_select} has only one sample in the data, so there is no movement to animate.")
        center = dict(lat=select["Lat"].mean(), lon=select["Long"].mean())
        st.plotly_chart(animation_figure(animate_data, center, map_type))
        st.success("The maps have been plotted successfully", icon="✅")
    except Exception as e:
        st.error("An error occurred: {}".format(e))


st.title("Haplo Tracker")
col1, col2 = st.columns(2)
with col1:
    st.image(str(LOGO_FILE), width=150)
with col2:
    haplogroup_select = st.selectbox("Select a mode", options=list(MODES))
if not haplogroup_select:
    st.error("Please select one category")
else:
    show_maps(prepare(haplogroup_select))
