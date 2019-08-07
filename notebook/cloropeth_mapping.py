# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 15:16:02 2019

@author: Rowan McNitt
"""
###############################################################################
#                                         _                                   #
#                                        (_)                                  #
#  _ __ ___     __ _   _ __               _   ___    ___    _ __              #
# | '_ ` _ \   / _` | | '_ \             | | / __|  / _ \  | '_ \             #
# | | | | | | | (_| | | |_) |            | | \__ \ | (_) | | | | |            #
# |_| |_| |_|  \__,_| | .__/             | | |___/  \___/  |_| |_|            #
#                     | |      ______   _/ |                                  #
#                     |_|     |______| |__/                                   #
#                                                                             #
###############################################################################


# start_loc => Focus point of the geomap, (lat, lng) format
# key => Folium chlorpeth key.. Open geojson in web browser and look for properties at the top..
# density => For drug_count, ratios, population, counts, whether to divide by area.. (ratios does not work unless density == True)
# data_file => Latitude and Longitude of the practices as well as the practice key ex: A81004
# geo_data_file => The geojson file **Most important file**
# column_names => The column names to be plotted, first is always* the name column, ex: ccg18nm
# delim => The delimiter used fore the 'data_file' pd.read_csv call
# start_zoom => starting zoom of the geomap
# count_column => The name of the column in the 'data_file' that specifies total prescriptions for each practice
# divisor  **NOT IN USE KEEP AT divisor=1**
# save_name => Name for the html file to view the geomap **must include .html in the name
# pop_file => File used for fuzzy string comparison to map populations onto the ccg regions from the 'data_file'
# by_prac => File used to find specific prescription count of a drug for a specific practice *Not all practices currently line up to those in the 'data_file'
# legend_title => The name of the legend in the top right

# # # # # # COLUMN GUIDE # # # # # # 

# - 'ccg18nm' => The name column, always used in the column names param as the first of the 2 elements in the list 
# - 'drug_count' =>
#       IF DENSITY => The total number of a specific drug(s) in each region divided by the area of the region
#       IF NOT DENSITY => The total number of a specific drug(s) in each region 
# - 'ratios' => (only if given population file and density = true) => Ratio of the log base 10 of practice density / log base 10 of population density
# - 'population' =>
#       IF DENSITY => The total population of a region (SOME MISTAKES IN FUZZY STRING COMPARISON) divided by the area of the region
#       IF NOT DENSITY => The total population of a region (SOME MISTAKES IN FUZZY STRING COMPARISON)
# - 'counts'
#       IF COUNT_COLUMN != ""
#       IF DENSITY => The total number of prescriptions in a region divided by the area of the region
#       IF NOT DENSITY => The total number of prescriptions in a region
#       IF COUNT_COLUMN == ""
#       IF DENSITY => The total number of practices in a region divided by the area of the region
#       IF NOT DENSITY => The total number of practices in a region


import pandas as pd
import geopandas as gpd
import folium
import numpy as np
from shapely.geometry import Point
from fuzzywuzzy import fuzz


def map_json(data_file, geo_data_file, save_name, by_prac="", pop_file="",
             start_loc=[], density=True,
             column_names=[], legend_title="",
             delim=",", start_zoom=5,
             count_column="Total", divisor=1,
             fill_color="OrRd", key="",
             fill_opac=0.6, line_opac=0.3, use_pop=False):
    df = pd.read_csv(data_file, delimiter=delim)
    m = folium.Map(location=start_loc, zoom_start=start_zoom)
    df['geometry'] = df.apply((lambda x: Point(x.lon, x.lat)), axis=1)

    ccg_gdf = gpd.read_file(geo_data_file)

    counts = []
    populations = []
    ratios = []
    drug_count = []

    if (pop_file != ""):
        pop_df = pd.read_csv(pop_file)
    if (by_prac != ""):
        prac_df = pd.read_csv(by_prac)

    # FOR FUZZY MATCHING POPULATION 'AREAS'
    if (not pop_file == ""):
        for i in range(len(ccg_gdf['geometry'])):
            dists = []
            pops = []
            names = []
            comp_name = ccg_gdf[column_names[0]][i]
            comp_name = comp_name[:len(comp_name) - 4]
            for v in range(len(pop_df)):
                current_name = pop_df['geography'][v]
                names.append(current_name)
                pops.append(pop_df['Variable: All usual residents measures: Value'][v])
                dists.append(fuzz.ratio(comp_name, current_name))
            ind = dists.index(max(dists))
            if (density == True):
                populations.append(pops[ind] / ccg_gdf['calculated_area'][i])
            else:
                populations.append(pops[ind])

    if (not by_prac == ""):
        print("Input the desired drug names.. (comma delimited)")
        DRUG_NAMEs = input()

        if (not DRUG_NAMEs == ""):
            DRUG_NAME = DRUG_NAMEs.split(",")
            print(DRUG_NAME)
        else:
            DRUG_NAME = ""
            by_prac = ""

    # Rest of mappinp: coount of total prescriptions, specific prescriptions, total practices, ratios
    for i in range(len(ccg_gdf['geometry'])):
        counts.append(0)
        drug_count.append(0)
        for v in range(len(df['geometry'])):
            if (ccg_gdf['geometry'][i].contains(df['geometry'][v])):
                if (not by_prac == ""):
                    try:
                        for c in range(len(DRUG_NAME)):
                            current_prac = df['PRACTICE'][v]
                            current_prac = current_prac.strip()

                            current_index = pd.Index(prac_df['org_code'])
                            current_ind = current_index.get_loc(current_prac)
                            drug_count[i] += prac_df[DRUG_NAME[c]][current_ind]
                    except:
                        print("No match found..")

                if (count_column == ""):
                    counts[i] += 1
                else:
                    counts[i] += df[count_column][i]

        if (density == True):
            if (not pop_file == ""):
                counts[i] = counts[i] / ccg_gdf['calculated_area'][i]
                ratios.append(np.log10(counts[i]) / np.log10(populations[i]))
            if (not by_prac == ""):
                drug_count[i] = drug_count[i] / ccg_gdf['calculated_area'][i]

        counts[i] = counts[i] / divisor
        print(i, '/', len(ccg_gdf['geometry']))

    if (density == True and not pop_file == ""):
        ccg_gdf['ratios'] = ratios
    elif (not pop_file == ""):
        ccg_gdf['population'] = populations

    if (not by_prac == ""):
        ccg_gdf['drug_count'] = drug_count

    ccg_gdf['counts'] = counts

    ##AREA CRS 27700

    folium.Choropleth(
        geo_data=geo_data_file,
        name='geometry',
        data=ccg_gdf,
        columns=column_names,
        key_on=key,
        fill_color=fill_color,
        fill_opacity=fill_opac,
        line_opacity=line_opac,
        legend_name=legend_title,
        smooth_factor=1).add_to(m)
    folium.LayerControl().add_to(m)
    m.save(save_name)


# Function call

map_json(start_loc=[52.2652, 1.0705], key="properties.ccg_name", density=True,
         data_file="total_rx_by_practice_location_included_2.csv",
         geo_data_file="new_uk_ccg_2018.geojson", column_names=['ccg_name', 'counts'],
         delim=",", start_zoom=6, count_column="Total", divisor=1, save_name="New_Map.html", pop_file="bulk.csv",
         by_prac="rx-by-practice-2018.csv", legend_title="Total Prescriptions By Region")
