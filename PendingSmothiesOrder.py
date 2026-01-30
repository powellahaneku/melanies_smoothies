import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Pending Smoothie Orders 🥤")
st.write(
    """
    Choose the fruits you want in your **custom Smoothie**!
    """
)

name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Query data
my_dataframe = (
    session.table("SMOOTHIES.PUBLIC.ORDERS")
    .filter(col("ORDER_FILLED") == 0)
    .to_pandas()
)

# Editable table (UI only)
editable_df = st.data_editor(my_dataframe)
