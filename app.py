# core packages
import streamlit as st

# EDA packages
import pandas as pd
import numpy as np
import csv
from numpy import load

# Data Viz
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

# recommendation system\
from models.content_based_rec_system import Content_Based_KNN



edible_dict = {'Yes':True, 'No':False}
backyard_dict = {'Large':'Tree',
                'Medium':'Shrub|Subshrub|Vine',
                'Small':'Forb/herb|Vine|Subshrub'}

def get_value(k, my_dict):
    for key, value in my_dict.items():
        if k == key:
            return value
def get_html():
    html = """
    <head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    <style>
    .grid-container {
      display: grid;
      grid-template-columns: auto auto auto auto auto auto;
    }
    .grid-item {
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        transition: 0.3s;
        padding: 10px;
        font-size: 30px;
        text-align: center;
    }
    table {
      font-family: arial, sans-serif;
      border-collapse: collapse;
      width: 100%;
    }
    td, th {
      border: 1px solid #dddddd;
      text-align: left;
      padding: 8px;
    }
    tr:nth-child(even) {
      background-color: #CFDBC5;
    }
    </style>
    </head>
    <body>
    <div class="grid-container">
    """
    return html
def get_plant_id(val, my_dict):
    for key, value in my_dict.items():
        if val == value:
            return key

def main():
    st.set_page_config(layout="wide")
    dict_data = load('similarity.npz')
    data = dict_data['arr_0']
    st.title("Plant Buddy :herb:")
    plant_info_df = pd.read_csv("data/plant_info.csv")
    plant_id_name_dict = plant_info_df.set_index('species_id').to_dict('dict')['scientific_name']

    filtered_plant_info_df = plant_info_df[
                                #(plant_info_df['edible'] == get_value(edibility,edible_dict)) &
                                #(plant_info_df['growth_habit'].str.contains(get_value(backyard_size,backyard_dict)))
                                #(plant_info_df['growth_habit'].str.contains('Subshrub'))
                                #& (plant_info_df['native'].str.contains(place))&
                                (plant_info_df['popular'] == True)
                                ]
    filtered_plant_info_df.reset_index(inplace = True, drop = True)

    #st.write(filtered_plant_info_df)
    filtered_plant_num = len(filtered_plant_info_df)
    #st.write(len(filtered_plant_info_df))


    #st.write(len(data[0]))
    html = get_html()

    for i in range(12):
        html = html + '<div class="grid-item"><img border="0" alt="pic unavailable" src="'+ str(filtered_plant_info_df.iloc[i]['image_url']) +'" width="200" height="200"><div class="container"><h4>'+ str(filtered_plant_info_df.iloc[i]['scientific_name'])+'</h4><p>'+ str(filtered_plant_info_df.iloc[i]['common_name'])+'</p><p><i class="fa fa-star" style="font-size:36px;color:gold;"></i></p></div></div>'
    html = html + '</div>'
    st.markdown(html,unsafe_allow_html=True)

    plant_name = st.sidebar.radio(
    "Click on the plant name to learn about it in detail...",
    ([filtered_plant_info_df.iloc[i]['scientific_name'] for i in range(12)]))

    if plant_name:
        plant_id = get_plant_id(plant_name,plant_id_name_dict)
        #st.write(plant_id)


        st.markdown("<br><br><br>",unsafe_allow_html=True)
        st.title(plant_name)
        col1, col2 = st.beta_columns(2)
        with col1:
            html = get_html() + "<table>"
            details ="""
                        <tr><th><b>Scientific name</b></th><td>The scientific name of species</td><td>"""+str(filtered_plant_info_df[filtered_plant_info_df['species_id']==int(plant_id)]['scientific_name'].values[0])+"""</td></tr>
                        <tr><th><b>Rank</b></th><td>The taxonomic rank of the species</td><td>"""+str(filtered_plant_info_df[filtered_plant_info_df['species_id']==int(plant_id)]['rank'].values[0])+"""</td></tr>
                        <tr><th><b>Genus</b></th><td>The scientific name of the species genus</td><td>"""+str(filtered_plant_info_df[filtered_plant_info_df['species_id']==int(plant_id)]['genus'].values[0])+"""</td></tr>
                        <tr><th><b>Family</b></th><td>The scientific name of the species family</td><td>"""+str(filtered_plant_info_df[filtered_plant_info_df['species_id']==int(plant_id)]['family'].values[0])+"""</td></tr>
                        <tr><th><b>Edible</b></th><td>Is the species edible?</td><td>"""+str(get_plant_id(filtered_plant_info_df[filtered_plant_info_df['species_id']==int(plant_id)]['edible'].values[0],edible_dict))+"""</td></tr>
                        <tr><th><b>Edible Parts</b></th><td>The plant edible part(s), if any</td><td>"""+str(filtered_plant_info_df[filtered_plant_info_df['species_id']==int(plant_id)]['edible_parts'].values[0])+"""</td></tr>
                        <tr><th><b>Vegetable</b></th><td>Is the species a vegetable?</td><td>"""+str(get_plant_id(filtered_plant_info_df[filtered_plant_info_df['species_id']==int(plant_id)]['vegetable'].values[0],edible_dict))+"""</td></tr>
                        <tr><th><b>Growth Habit</b></th><td>The general appearance, growth form, or architecture of the plant</td><td>"""+str(filtered_plant_info_df[filtered_plant_info_df['species_id']==int(plant_id)]['growth_habit'].values[0])+"""</td></tr>

                    """
            html = html +details
            st.markdown(html,unsafe_allow_html=True)
        with col2:
            #st.markdown("<br><br>",unsafe_allow_html=True)
            html = get_html() + '<div class="grid-item"><img border="0" alt="Plant App" src="'+ str(filtered_plant_info_df[filtered_plant_info_df['species_id']==int(plant_id)]['image_url'].values[0]) +'" width="400" height="400"><br><br><p><b>Native: </b>'+str(filtered_plant_info_df[filtered_plant_info_df['species_id']==int(plant_id)]['native'].values[0])+'</p></div>'
            st.markdown(html, unsafe_allow_html = True)
            #st.write(str(filtered_plant_info_df[filtered_plant_info_df['species_id']==int(plant_id)]['native'].values[0]))
            #st.image(filtered_plant_info_df[filtered_plant_info_df['species_id']==int(plant_id)]['image_url'].values[0],use_column_width=True)
            #st.image("https://unsplash.com/photos/XKNhgX1rDUk")
            #st.write(data[0][1])
            predictions = Content_Based_KNN.estimate(int(plant_id), plant_info_df, data)

        st.markdown("<br><br><br><br>",unsafe_allow_html=True)
        st.write("You may also like....")
        html = get_html()
        for i in range(5):
            if plant_info_df.iloc[predictions[i]]['popular'] == 1:
                html = html + '<div class="grid-item"><img border="0" alt="Plant App" src="'+ str(plant_info_df.iloc[predictions[i]]['image_url']) +'" width="200" height="200"><div class="container"><h3>'+str(plant_info_df.iloc[predictions[i]]['scientific_name'])+'</h3><p>'+ str(plant_info_df.iloc[predictions[i]]['common_name'])+'</p><p><i class="fa fa-star" style="font-size:36px;color:gold;"></i></p></div></div>'
            else:
                html = html + '<div class="grid-item"><img border="0" alt="Plant App" src="'+ str(plant_info_df.iloc[predictions[i]]['image_url']) +'" width="200" height="200"><div class="container"><h3>'+str(plant_info_df.iloc[predictions[i]]['scientific_name'])+'</h3><p>'+ str(plant_info_df.iloc[predictions[i]]['common_name'])+'</p></div></div>'
            #html = html + '<p><b>Rank:</b> '+str(plant_info_df.iloc[predictions[i]]['rank'])+'</p><p><b>Genus:</b> '
            #html = html + str(plant_info_df.iloc[predictions[i]]['genus'])+'</p><p><b>Family:</b> '+ str(plant_info_df.iloc[predictions[i]]['family'])+'</p></div></div>'
            #html = html + '<p><b>Native: </b>'+str(plant_info_df.iloc[predictions[i]]['native'])+'</p></div></div>'
        html = html + '</div>'
        st.markdown(html,unsafe_allow_html=True)

        col1, col2, col3, col4, col5, col6 = st.beta_columns(6)
        cols = st.beta_columns(5)

        #st.write(cols)
        for i in range(5):
            with cols[i]:
                with st.beta_expander(str(plant_info_df.iloc[predictions[i]]['scientific_name'])):
                    html = get_html() + "<table>"
                    details ="""
                                <tr><th><b>Rank</b></th><td>"""+str(plant_info_df.iloc[predictions[i]]['rank'])+"""</td></tr>
                                <tr><th><b>Genus</b></th><td>"""+str(plant_info_df.iloc[predictions[i]]['genus'])+"""</td></tr>
                                <tr><th><b>Family</b></th><td>"""+str(plant_info_df.iloc[predictions[i]]['family'])+"""</td></tr>
                                <tr><th><b>Edible</b></th><td>"""+str(get_plant_id(plant_info_df.iloc[predictions[i]]['edible'],edible_dict))+"""</td></tr>
                                <tr><th><b>Edible Parts</b><td>"""+str(plant_info_df.iloc[predictions[i]]['edible_parts'])+"""</td></tr>
                                <tr><th><b>Vegetable</b></th><td>"""+str(get_plant_id(plant_info_df.iloc[predictions[i]]['vegetable'],edible_dict))+"""</td></tr>
                                <tr><th><b>Growth Habit</b></th><td>"""+str(plant_info_df.iloc[predictions[i]]['growth_habit'])+"""</td></tr>
                                <tr><th><b>Native</b></th><td>"""+str(plant_info_df.iloc[predictions[i]]['native'])+"""</td></tr>
                            """
                    html = html +details
                    st.markdown(html,unsafe_allow_html=True)




if __name__ == "__main__":
    main()
