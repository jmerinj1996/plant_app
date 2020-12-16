# core packages
import streamlit as st

# EDA packages
import pandas as pd
import numpy as np

# Data Viz
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")

import streamlit.components.v1 as components


edible_dict = {'Yes':True, 'No':False}
backyard_dict = {'Large':['Forb/herb','Vine', 'Subshrub'],'Medium':['Shrub','Subshrub','Vine'], 'Small':['Tree','Vine']}
countries = ['China',
'India','United States', 'Indonesia','Pakistan', 'Brazil',
'Nigeria','Bangladesh','Russia','Mexico','Japan','Ethiopia','Philippines','Egypt',
'Vietnam','DR Congo','Turkey','Iran','Germany','Thailand','United Kingdom','France','Italy','Tanzania','South Africa','Myanmar',
'Kenya','South Korea','Colombia','Spain','Uganda','Argentina','Algeria','Sudan','Ukraine','Iraq','Afghanistan','Poland',
'Canada','Morocco','Saudi Arabia','Uzbekistan','Peru','Angola','Malaysia','Mozambique','Ghana','Yemen','Nepal','Venezuela','Madagascar','Cameroon',
"Côte d'Ivoire",'North Korea','Australia','Niger','Sri Lanka','Burkina Faso','Mali','Romania','Malawi','Chile','Kazakhstan','Zambia',
'Guatemala','Ecuador','Syria','Netherlands','Senegal','Cambodia','Chad','Somalia','Zimbabwe','Guinea','Rwanda','Benin','Burundi','Tunisia',
'Bolivia','Belgium','Haiti','Cuba','South Sudan','Dominican Republic','Czech Republic (Czechia)','Greece','Jordan','Portugal','Azerbaijan','Sweden',
'Honduras','United Arab Emirates','Hungary','Tajikistan','Belarus','Austria','Papua New Guinea','Serbia','Israel','Switzerland','Togo',
'Sierra Leone','Laos','Paraguay','Bulgaria','Libya','Lebanon','Nicaragua','Kyrgyzstan','El Salvador','Turkmenistan','Singapore','Denmark',
'Finland','Congo','Slovakia','Norway','Oman','State of Palestine','Costa Rica','Liberia','Ireland','Central African Republic','New Zealand','Mauritania', 'Panama'
'Kuwait','Croatia','Moldova','Georgia','Eritrea','Uruguay','Bosnia and Herzegovina','Mongolia','Armenia','Jamaica','Qatar','Albania','Lithuania',
'Namibia','Gambia','Botswana','Gabon','Lesotho','North Macedonia','Slovenia','Guinea-Bissau','Latvia','Bahrain','Equatorial Guinea','Trinidad and Tobago',
'Estonia','Timor-Leste','Mauritius','Cyprus','Eswatini','Djibouti','Fiji','Comoros','Guyana','Bhutan','Solomon Islands','Montenegro','Luxembourg',
'Suriname','Cabo Verde','Maldives','Malta','Brunei','Belize','Bahamas','Iceland','Vanuatu','Barbados','Sao Tome & Principe','Samoa','Saint Lucia',
'Kiribati','Micronesia','Grenada','St. Vincent & Grenadines','Tonga','Seychelles','Antigua and Barbuda','Andorra','Dominica','Marshall Islands',
'Saint Kitts & Nevis','Monaco','Liechtenstein','San Marino','Palau','Tuvalu','Nauru','Holy See']

def get_html():
    html = """
    <head>
    <style>
    .grid-container {
      display: grid;
      grid-template-columns: auto auto auto;
    }
    .grid-item {
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        transition: 0.3s;
        padding: 10px;
        font-size: 30px;
        text-align: center;
    }
    </style>
    </head>
    <body>
    <div class="grid-container">
    """
    return html


def get_value(val, my_dict):
    for key, value in my_dict.items():
        if val == key:
            return value
def get_key(val, my_dict):
    for key, value in my_dict.items():
        if val == key:
            return key

def main():
    # Plant recommendation App
    st.title("Plant Buddy :herb:")

    menu = ['Home', 'About']
    choice = st.sidebar.selectbox("Menu", menu)
    if choice == "Home":
        st.subheader("A plant recommender system")
        df = pd.read_csv("data/items_df.csv")
        plant_id_name_dict = df.set_index('species_id').to_dict('dict')['scientific_name']
        #st.write(plant_id_name_dict)
        #st.dataframe(df)
        #st.bar_chart(df['edible'].value_counts())
        backyard_size = st.radio(
        'How big is your backyard?',tuple(backyard_dict.keys()))

        edibility = st.radio(
        "Do you want a plant that's edible ?",tuple(edible_dict.keys()))
        #st.write(get_value(edibility,edible_dict))
        with st.beta_expander("See plot"):
            st.bar_chart(df['edible'].value_counts())
            #df['edible'].value_counts().plot(kind='bar')
            #st.dataframe(df[df['edible']==get_value(edibility,edible_dict)])
            #st.set_option('deprecation.showPyplotGlobalUse', False)
            #st.pyplot()

        place = st.selectbox(
                'Which part of the world are you from?',
                (countries))
        col1, col2, col3 = st.beta_columns(3)
        with col2:
            find_plant = st.checkbox('Find my plant!')
        if find_plant:
            st.subheader("Here are some plants we recommend.....")
            html = get_html()
            for i in range(12):
                html = html + '<div class="grid-item"><a href="#details"><img border="0" alt="W3Schools" src="'+str(df.iloc[i]['image_url']) +'" width="200" height="200"></a><div class="container"><h4><b>'+str(df.iloc[i]['scientific_name'])+'</b></h4></div></div>'
            html = html + '</div><div id = "details"></div>'
            st.markdown(html,unsafe_allow_html=True)

            plant_id = st.sidebar.radio(
            "Click on the plant name to learn about it in detail...",
            ([df.iloc[i]['scientific_name'] for i in range(12)]))

            if plant_id:
                st.subheader(plant_id)


    else:
        st.subheader("About this App")

if __name__ == "__main__":
    main()
