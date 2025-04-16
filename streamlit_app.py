# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests
# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie!:cup_with_straw:")
st.write(
  "Choose the fruits you want in your custom Smoothie"
)


name_on_order = st.text_input("Name of Smoothie")
st.write('The name on your Smoothie will be', name_on_order)

#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
###st.dataframe(data=my_dataframe, use_container_width=True)
st.dataframe(data=my_dataframe,use_container_width=True
st.stop()

ingredient_list = st.multiselect ("Choose up to 5 Incredients", my_dataframe, max_selections=5)
if ingredient_list :
##       st.write(ingredient_list)
    ingredients_string =''
    for fruit_chosen in ingredient_list:
        ingredients_string += fruit_chosen+ ' '
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" +fruit_chosen)
#st.text(smoothiefroot_response.json())
        sf_df = st.dataframe(data=smoothiefroot_response.json(),use_container_width=True)

    st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)   values ('""" + ingredients_string + """','"""+name_on_order+"""')"""
#    st.write(my_insert_stmt)
##    st.stop
    time_to_insert = st.button(" Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered '+ name_on_order +'I', icon="✅")



