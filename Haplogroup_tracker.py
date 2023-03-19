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

User Defined Functions:
    common_code(mtgeo): This function is used to plot the haplogroups on the map based on the user input.
    The function takes the data as input and returns the map with the haplogroups plotted on it and the user can select the group to be animated.
    Onlyfemale_mtdna(): This function is used to filter the data to only include the females mtdna and then call the common_code function to plot the haplogroups on the map.
    Onlymale_mtdna(): This function is used to filter the data to only include the males mtdna and then call the common_code function to plot the haplogroups on the map.
    Combined_mtdna():This function is used to filter the data to only include  mtdna and then call the common_code function to plot the haplogroups on the map.
    Onlymale_ychrom():This function is used to filter the data to include only individuals with y-chromosome and then call the common_code function to plot the haplogroups on the map.
Procedure:
1.Import the required libraries
2.Read the data from the excel file which acts as the database.
3.Filter the data based on the user input.
4.Plot the haplogroups on the map based on the user input.
5.Create static traces based on the groups selected.
5.Create frames based on the longitude and latitude of the haplogroups selected.
6.Create the animation based on the frames created.
User Guide:
1.User selects mode of the haplogroup ie. the mtdna mode or y-chromosome mode.
2.User selects the Haplogroups that they want to visualize.
3.User selects the map type.
4.User selects the haplogroup to animate.
5.Press the play button to animate the haplogroup movement over time.

    """
#Create a streamlit app to track the movement of haplogroups over time
#Importing the required libraries
import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from PIL import Image
import os
from pathlib import Path
#Adding a browser title
st.set_page_config(page_title="HaploTracker",page_icon=":dna:",layout="wide",initial_sidebar_state="expanded")
def load_css():
    """
    Function to load custom CSS styles.
    """
    streamlit_static_path = Path(st.__path__[0]) / 'static'
    css_path = streamlit_static_path / "css"
    if not css_path.is_dir():
        css_path.mkdir()
    css_file = css_path / "style.css"
    if not css_file.exists():
        css_file.write_text(open("assests/style.css", "r").read())
    st.markdown(f'<link rel="stylesheet" href="{os.path.join("/", str(css_file))}">', unsafe_allow_html=True)

load_css()
#Hiding the main menu and footer
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
#Reading the data
data=pd.read_excel("Data/Eurasian.xlsx") #Rename the file name to the file name of the data ifyou want to use your own data.
#Creating a title for the app
title_text = "Haplo Tracker"
st.title(title_text)
#Creating a dataframe with the required columns and renaming the columns
col1,col2=st.columns(2)
with col1:
    image=Image.open('assests/LU.png')
    st.image(image,width=150)
#Creating the main function for the app    
def common_code(mtgeo):     
    try:
        #creating a sidebar to select the haplogroups
        option=st.multiselect(label="Select the haplogroup",options=mtgeo["mtdna"].unique())
        if not option:#if no haplogroup is selected
            st.error("Please select atleast one haplogroup")
        else:  #    if haplogroup is selected
            mtgeo["Date"]=mtgeo["Date"]+70 #adding 70 years to the date column to find age from 2020
            mtgeo['Lat'].astype(float) #converting the latitude column to float
            mtgeo['Long'].astype(float) #converting the longitude column to float
            select=mtgeo[mtgeo["mtdna"].isin(option)]      #selecting the haplogroups selected in the sidebar
            select["hover"] = select["Country"].str.cat('\t' + select["Date"].astype(str) + ' years ago') #creating a hover column
            map_type=st.selectbox("Select map type",options=["USGS","Natural Earth"]) #selecting the map type
            if map_type=="Natural Earth":   #if natural earth is selected
                    fig1 = px.scatter_geo(select, lat = 'Lat', lon = 'Long',color='mtdna',hover_name="hover",projection='natural earth',
                                          color_discrete_sequence=px.colors.qualitative.Set1)
                    fig1.update_geos(showland=True,landcolor="LightGreen",showocean=True, oceancolor="LightBlue",
                                     showrivers=True, rivercolor="Blue",
                                     projection_type="natural earth",fitbounds="locations")
                    st.plotly_chart(fig1)
                    select=select.sort_values(by="Date",ascending=False)  #sorting the data based on the date in descending order
                    animate_select=st.selectbox("Select haplogroup to animate",options=option)  #Using the user input to select the haplogroup to animate
                    animate_data = select[select["mtdna"].isin([animate_select])]
                    fig3 = go.Figure(
                        data=[
                            go.Scattermapbox(
                                lat=animate_data["Lat"],
                                lon=animate_data["Long"],
                                mode="lines",
                                line=dict(width=2, color="blue"),
                                name="Haplogroup Movement",
                                hovertext=animate_data["hover"]
                            ),
                            go.Scattermapbox(
                                lat=animate_data["Lat"],
                                lon=animate_data["Long"],
                                mode="lines",
                                line=dict(width=2, color="blue")
                            ),
                            go.Scattermapbox(
                                lat=animate_data["Lat"],
                                lon=animate_data["Long"],
                                mode="markers",
                                marker=dict(
                                    size=6,
                                    color="red"
                                ),
                                name="Haplogroup locations",
                                hovertext=animate_data["hover"]
                            )
                        ],
                        layout=go.Layout(
                            title_text="Movement of selected Haplogroup over history",
                            mapbox_style="carto-positron", # Change the mapbox_style to "carto-positron"
                            mapbox=dict(
                                accesstoken="pk.eyJ1IjoibmlraGlsZXNoMjMiLCJhIjoiY2xmMmJucGx6MDFxaTN5bnRpYW12cWxxeCJ9.KeccdtSz6Hc9F_vPrYoiNg",
                                bearing=0,
                                center=dict(
                                    lat=select["Lat"].mean(),
                                    lon=select["Long"].mean()),
                                pitch=0,
                                zoom=1
                            ),
                            updatemenus=[
                                dict(
                                    type="buttons",
                                    buttons=[dict(label="Play", method="animate",args=[None])]
                                )
                            ]
                        ),
                        frames=[
                            go.Frame(
                                data=[
                                    go.Scattermapbox(
                                        lat=[list(animate_data["Lat"])[k]],
                                        lon=[list(animate_data["Long"])[k]],
                                        mode="markers",
                                        marker=dict(color="red", size=10),
                                        text=list(animate_data["mtdna"])[k]
                                    ),

                                    go.Scattermapbox(
                                        lat=list(animate_data["Lat"])[:k+1],
                                        lon=list(animate_data["Long"])[:k+1],
                                        mode="lines",
                                        line=dict(width=2, color="orange"),
                                        name="Movement"
                                    )
                                ]
                            )
                            for k in range(1, len(animate_data["mtdna"]))
                        ]
                    )

                    # Change the map style using update_layout
                    fig3.update_layout(
                        mapbox=dict(
                            style="carto-positron",
                            center=dict(
                                lat=select["Lat"].mean(),
                                lon=select["Long"].mean()
                            ),
                            zoom=1
                        )
                    )

                    st.plotly_chart(fig3)

            else:       #if USGS is selected
                    fig1 = px.scatter_mapbox(select, lat = 'Lat', lon = 'Long',color='mtdna',hover_name="hover",
                                          color_discrete_sequence=px.colors.qualitative.Set1)   #creating a scatter plot on the map based on the haplogroups selected
                    fig1.update_traces(marker=dict(size=10, symbol="circle"))#updating the size of the markers and the shape of the markers
                    fig1.update_geos(showland=True,landcolor="LightGreen",showocean=True, oceancolor="LightBlue",   #updating the map features
                                     showrivers=True, rivercolor="Blue")
                    select=select.sort_values(by="Date",ascending=False)       #sorting the data based on the date in descending order
                    fig1.update_layout( #updating the layout of the map
                    mapbox_style="white-bg",            
                    mapbox_layers=[
                        {
                            "below": 'traces',
                            "sourcetype": "raster",
                            "sourceattribution": "United States Geological Survey",
                            "source": [
                                "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                                ]
                            }
                        ])
                    st.plotly_chart(fig1)   #plotting the map
                    select=select.sort_values(by="Date",ascending=False)  #sorting the data based on the date in descending order
                    animate_select=st.selectbox("Select haplogroup to animate",options=option)  #Using the user input to select the haplogroup to animate
                    animate_data = select[select["mtdna"].isin([animate_select])]       #selecting the haplogroup to animate from the data
                    
                    fig3 = go.Figure( #Initializing the figure
                        data=[  #adding the data to the figure
                            go.Scattermapbox( #adding the scattermapbox to the figure
                                lat=animate_data["Lat"], #adding the latitude column to the scattermapbox
                                lon=animate_data["Long"],      #adding the longitude column to the scattermapbox
                                mode="lines",#adding the mode to the scattermapbox
                                line=dict(width=2, color="blue"),#adding the line properties to the scattermapbox
                                name="Haplogroup Movement",#adding the name to the scattermapbox
                                hovertext=animate_data["hover"]#adding the hover text to the scattermapbox
                            ),
                            go.Scattermapbox(#adding a second scattermapbox to the figure
                                lat=animate_data["Lat"],    #adding the latitude column to the scattermapbox
                                lon=animate_data["Long"],   #adding the longitude column to the scattermapbox
                                mode="lines",   #adding the mode to the scattermapbox
                                line=dict(width=2, color="blue")        #adding the line properties to the scattermapbox
                            ),
                            go.Scattermapbox(   #adding a third scattermapbox to the figure
                                lat=animate_data["Lat"],        #adding the latitude column to the scattermapbox
                                lon=animate_data["Long"],       #adding the longitude column to the scattermapbox
                                mode="markers",     #adding the mode to the scattermapbox
                                marker=dict(            #adding the marker properties to the scattermapbox
                                    size=6, #adding the size of the marker
                                    color="red"     #adding the color of the marker
                                ),
                                name="Haplogroup locations",   #adding the name to the scattermapbox
                                hovertext=animate_data["hover"]    #adding the hover text to the scattermapbox
                            )
                        ],
                        layout=go.Layout(  #adding the layout to the figure
                            title_text="Movement of mtHaplogroups over history", #adding the title to the figure
                            mapbox_style="white-bg",   #adding the mapbox style to the figure
                            mapbox_layers=[ #adding the mapbox layers to the figure
                                {
                                    "below": 'traces',
                                    "sourcetype": "raster",
                                    "sourceattribution": "United States Geological Survey",
                                    "source": [
                                        "https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryOnly/MapServer/tile/{z}/{y}/{x}"
                                    ]
                                }
                            ],
                            mapbox=dict( 
                                accesstoken="pk.eyJ1IjoibmlraGlsZXNoMjMiLCJhIjoiY2xmMmJucGx6MDFxaTN5bnRpYW12cWxxeCJ9.KeccdtSz6Hc9F_vPrYoiNg",
                                bearing=0,
                                center=dict(
                                    lat=select["Lat"].mean(),
                                    lon=select["Long"].mean()),
                                pitch=0,
                                zoom=1
                            ),
                            updatemenus=[ #adding the updatemenus to the figure which will be used to animate the figure
                                dict(
                                    type="buttons",
                                    buttons=[dict(label="Play",method="animate",args=[None])] 
                                )
                            ]
                        ),
                        frames=[ #The frames are used to animate the figure initializing the frames.
                            go.Frame(
                                data=[
                                    go.Scattermapbox( #adding the scattermapbox "markers" to the frame to animate
                                        lat=[list(animate_data["Lat"])[k]],
                                        lon=[list(animate_data["Long"])[k]],
                                        mode="markers",
                                        marker=dict(color="red", size=10),
                                        text=list(animate_data["mtdna"])[k]
                                    ),
                                    
                                    go.Scattermapbox( #adding the scattermapbox "lines" to the frame to animate
                                        lat=list(animate_data["Lat"])[:k+1], #adding the latitude column to the scattermapbox
                                        lon=list(animate_data["Long"])[:k+1], #adding the longitude column to the scattermapbox
                                        mode="lines",
                                        line=dict(width=2, color="orange"),
                                        name="Movement"
                                    )
                                ]
                            )
                            for k in range(1, len(animate_data["mtdna"]))   #for loop to iterate through the data
                        ]
                    )
                    st.plotly_chart(fig3)   #plotting the figure
            st.success("The maps have been plotted successfully",icon="✅") #printing the success message
    except Exception as e:  #exception handling
            st.error("An error occurred: {}".format(e)) #printing the error message
def Onlyfemale_mtdna():        #Creating various functions to plot the data based on the user mode of selection
    mtdata=data.loc[data["Sex"]=="F"]
    # Selecting the required columns from the data
    mtgeo=mtdata[["Lat.","Long.","mtDNA haplogroup if ≥2 or published","Date mean in BP in years before 1950 CE [OxCal mu for a direct radiocarbon date, and average of range for a contextual date]","Country"]]
    # Renaming the columns for ease of use
    mtgeo=mtgeo.rename(columns={'Lat.':'Lat','Long.':'Long','mtDNA haplogroup if ≥2 or published':'mtdna','Date mean in BP in years before 1950 CE [OxCal mu for a direct radiocarbon date, and average of range for a contextual date]':'Date'})
    mtgeo=mtgeo.drop(mtdata[mtgeo.Lat==".."].index) #dropping the rows with missing values
    
    common_code(mtgeo)#calling the common code function to plot the data

def Onlymale_mtdna():
    mtdata=data.loc[data["Sex"]=="M"]
    mtgeo=mtdata[["Lat.","Long.","mtDNA haplogroup if ≥2 or published","Date mean in BP in years before 1950 CE [OxCal mu for a direct radiocarbon date, and average of range for a contextual date]","Country"]]
    mtgeo=mtgeo.rename(columns={'Lat.':'Lat','Long.':'Long','mtDNA haplogroup if ≥2 or published':'mtdna','Date mean in BP in years before 1950 CE [OxCal mu for a direct radiocarbon date, and average of range for a contextual date]':'Date'})
    mtgeo=mtgeo.drop(mtdata[mtgeo.Lat==".."].index)
    common_code(mtgeo)
    
def Combined_mtdna():
    mtdata=data
    mtgeo=mtdata[["Lat.","Long.","mtDNA haplogroup if ≥2 or published","Date mean in BP in years before 1950 CE [OxCal mu for a direct radiocarbon date, and average of range for a contextual date]","Country"]]
    mtgeo=mtgeo.rename(columns={'Lat.':'Lat','Long.':'Long','mtDNA haplogroup if ≥2 or published':'mtdna','Date mean in BP in years before 1950 CE [OxCal mu for a direct radiocarbon date, and average of range for a contextual date]':'Date'})
    mtgeo=mtgeo.drop(mtdata[mtgeo.Lat==".."].index)
    common_code(mtgeo)
    
def Onlymale_ychrom():
    mtdata=data.loc[data["Sex"]=="M"]
    mtgeo=mtdata[["Lat.","Long.","Y haplogroup  in ISOGG v15.73 notation (automatically called)","Date mean in BP in years before 1950 CE [OxCal mu for a direct radiocarbon date, and average of range for a contextual date]","Country"]]
    mtgeo=mtgeo.rename(columns={'Lat.':'Lat','Long.':'Long','Y haplogroup  in ISOGG v15.73 notation (automatically called)':'mtdna','Date mean in BP in years before 1950 CE [OxCal mu for a direct radiocarbon date, and average of range for a contextual date]':'Date'})
    mtgeo=mtgeo.drop(mtdata[mtgeo.Lat==".."].index)
    common_code(mtgeo)
with col2:
    haplogroup_select=st.selectbox("Select a mode",options=["MtDNA","MtDNA-Male","MtDNA-Female","Y-Chromosome"]) #selecting the mode of selection
if not haplogroup_select:       #exception handling
    st.error("Please select one category")  #printing the error message
elif haplogroup_select=="MtDNA":    #if the user selects the mtdna mode
    Combined_mtdna()    #calling the Combined_mtdna function
elif haplogroup_select=="MtDNA-Male":   #if the user selects the mtdna-male mode
    Onlymale_mtdna() #calling the Onlymale_mtdna function
elif haplogroup_select=="MtDNA-Female": #If the user selects the mtdna-female mode
    Onlyfemale_mtdna() #calling the Onlyfemale_mtdna function
elif haplogroup_select=="Y-Chromosome": #If the user selects the y-chrom mode
    Onlymale_ychrom()   #calling the Onlymale_ychrom function

