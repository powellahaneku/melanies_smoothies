import streamlit as st
from snowflake.snowpark.functions import col
import pandas as pd
# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Load data
df = (
    session.table("SMOOTHIES.PUBLIC.ORDERS")
    .filter(col("ORDER_FILLED") == 0)
    .to_pandas()
)

# Editable UI
edited_df = st.data_editor(df, num_rows="dynamic")

# Save button
if st.button("Save changes"):
    # Write edited data to a temporary table
    session.write_pandas(
        edited_df,
        table_name="ORDERS_TMP",
        database="SMOOTHIES",
        schema="PUBLIC",
        overwrite=True
    )

    # Merge updates back into main table
    session.sql("""
        MERGE INTO SMOOTHIES.PUBLIC.ORDERS tgt
        USING SMOOTHIES.PUBLIC.ORDERS_TMP src
        ON tgt.ORDER_ID = src.ORDER_ID
        WHEN MATCHED THEN
          UPDATE SET
            tgt.ORDER_FILLED = src.ORDER_FILLED
    """).collect()

    st.success("Orders updated successfully ✅")
