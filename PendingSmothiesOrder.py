import streamlit as st
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f"Pending Smoothi Orders!:cup_with_straw:")
st.write(
  """
  Choose the fruits you want in your **custin Smoothie**!.
  """
)




name_on_order = st.text_input('Name on Smoothie:')
st.write("The name on your Smoothie will be:", name_on_order)

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
#st.dataframe(data=my_dataframe, use_container_width=True)


editable_df = st.data_editor(my_dataframe)
