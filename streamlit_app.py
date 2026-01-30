import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Customize Your Smoothie!:cup_with_straw:")
st.write(
  """
  Choose the fruits you want in your **custin Smoothie**!.
  """
)


name_on_order = st.text_input('Name on Smoothie:')
st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake") # for SniS version (Streamlit not in Snowflake)
session = cnx.session() #get_active_session() 
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)

pd_df = my_dataframe.to_pandas()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:'
    ,my_dataframe
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
      
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
      
        st.subheader(fruit_chosen + ' Nutrition Information')
        smoothiefroot_response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{search_on}")
        sf_df = st.dataframe(data =smoothiefroot_response.json(),use_container_width=True)


        my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order) values ('""" + ingredients_string + """','"""+name_on_order+"""')"""


time_to_insert = st.button('Submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")


# import streamlit as st
# import requests
# import pandas as pd
# from snowflake.snowpark.functions import col

# st.title("Customize Your Smoothie! 🥤")
# st.write("Choose the fruits you want in your **custom Smoothie**!")

# name_on_order = st.text_input('Name on Smoothie:')
# st.write("The name on your Smoothie will be:", name_on_order)

# # Snowflake connection
# cnx = st.connection("snowflake")
# session = cnx.session()

# my_dataframe = (
#     session
#     .table("smoothies.public.fruit_options")
#     .select(col('FRUIT_NAME'), col('SEARCH_ON'))
# )

# st.dataframe(my_dataframe, use_container_width=True)

# # Convert to pandas
# pd_df = my_dataframe.to_pandas()

# ingredients_list = st.multiselect(
#     'Choose up to 5 ingredients:',
#     pd_df['FRUIT_NAME'].tolist(),
#     max_selections=5
# )

# if ingredients_list:
#     ingredients_string = ", ".join(ingredients_list)

#     for fruit_chosen in ingredients_list:
#         search_on = pd_df.loc[
#             pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'
#         ].iloc[0]

#         st.write(f"The search value for {fruit_chosen} is {search_on}.")
#         st.subheader(f"{fruit_chosen} Nutrition Information")

#         response = requests.get(
#             f"https://my.smoothiefroot.com/api/fruit/{search_on}"
#         )
#         st.dataframe(response.json(), use_container_width=True)

# time_to_insert = st.button('Submit Order')

# session.sql("USE DATABASE SMOOTHIES").collect()
# session.sql("USE SCHEMA PUBLIC").collect()

# if time_to_insert and ingredients_list and name_on_order:
#     session.sql(
#         """
#         INSERT INTO ORDERS (
#             NAME_ON_ORDER,
#             INGREDIENTS
#         )
#         VALUES (?, ?)
#         """,
#         params=[name_on_order, ingredients_string]
#     ).collect()

#     st.success("Your Smoothie is ordered! 🥤", icon="✅")


