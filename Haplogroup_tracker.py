# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 10:29:19 2023

@author: vnikh
"""

import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go
from PIL import Image

data=pd.read_excel("Data/Eurasian.xlsx")
title_text = "Haplogroup Tracker"
st.title(title_text)
col1,col2=st.columns(2)
with col1:
    image=Image.open('LU.png')
    st.image(image,width=150)
def common_code(mtgeo):
    try:
        option=st.multiselect(label="Select the haplogroup",options=mtgeo["mtdna"].unique())
        if not option:
            st.error("Please select atleast one haplogroup")
        else:
            
            mtgeo["Date"]=mtgeo["Date"]+70
            mtgeo['Lat'].astype(float)
            mtgeo['Long'].astype(float)
            select=mtgeo[mtgeo["mtdna"].isin(option)]
            select["hover"] = select["Country"].str.cat('\t' + select["Date"].astype(str) + ' years ago')
            map_type=st.selectbox("Select map type",options=["USGS","Natural Earth"])
            if map_type=="Natural Earth":
                fig1 = px.scatter_geo(select, lat = 'Lat', lon = 'Long',color='mtdna',hover_name="hover",projection='natural earth',
                                      color_discrete_sequence=px.colors.qualitative.Set1)
                fig1.update_geos(showland=True,landcolor="LightGreen",showocean=True, oceancolor="LightBlue",
                                 showrivers=True, rivercolor="Blue",
                                 projection_type="natural earth",fitbounds="locations")
                st.plotly_chart(fig1)
            else:
                fig1 = px.scatter_mapbox(select, lat = 'Lat', lon = 'Long',color='mtdna',hover_name="hover",
                                      color_discrete_sequence=px.colors.qualitative.Set1)
                fig1.update_traces(marker=dict(size=10, symbol="circle"))
                fig1.update_geos(showland=True,landcolor="LightGreen",showocean=True, oceancolor="LightBlue",
                                 showrivers=True, rivercolor="Blue")
                select=select.sort_values(by="Date",ascending=False)
                fig1.update_layout(
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
                st.plotly_chart(fig1)
        select=select.sort_values(by="Date",ascending=False)
        animate_select=st.selectbox("Select haplogroup to animate",options=option)
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
                title_text="Movement of mtHaplogroups over history",
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
        st.plotly_chart(fig3)
    except Exception as e:
        st.error("An error occurred: {}".format(e))
def Onlyfemale_mtdna():    
    mtdata=data.loc[data["Sex"]=="F"]
    mtgeo=mtdata[["Lat.","Long.","mtDNA haplogroup if ≥2 or published","Date mean in BP in years before 1950 CE [OxCal mu for a direct radiocarbon date, and average of range for a contextual date]","Country"]]
    mtgeo=mtgeo.rename(columns={'Lat.':'Lat','Long.':'Long','mtDNA haplogroup if ≥2 or published':'mtdna','Date mean in BP in years before 1950 CE [OxCal mu for a direct radiocarbon date, and average of range for a contextual date]':'Date'})
    mtgeo=mtgeo.drop(mtdata[mtgeo.Lat==".."].index)
    
    common_code(mtgeo)

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
    haplogroup_select=st.selectbox("Select a mode",options=["mtdna","mtdna-male","mtdna-female","y-chrom"])
if not haplogroup_select:
    st.error("Please select one category")
elif haplogroup_select=="mtdna":
    Combined_mtdna()
elif haplogroup_select=="mtdna-male":
    Onlymale_mtdna()
elif haplogroup_select=="mtdna-female":
    Onlyfemale_mtdna()
elif haplogroup_select=="y-chrom":
    Onlymale_ychrom()
#Plotly
#User input given on the haplogroup used and color based on the years
