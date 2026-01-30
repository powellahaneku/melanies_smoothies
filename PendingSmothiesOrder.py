import streamlit as st
from snowflake.snowpark.functions import col

st.title("Update Smoothie Orders 🥤")

# Snowflake connection
cnx = st.connection("snowflake")
session = cnx.session()

# Search input
search_name = st.text_input("Search name on order")

if search_name:
    # Query Snowflake based on name
    df = (
        session.table("SMOOTHIES.PUBLIC.ORDERS")
        .filter(col("NAME_ON_ORDER").ilike(f"%{search_name}%"))
        .to_pandas()
    )

    if df.empty:
        st.info("No matching orders found.")
    else:
        # Editable table
        edited_df = st.data_editor(df, num_rows="dynamic")

        # Save button
        if st.button("Save updates"):
            # Temp table
            session.write_pandas(
                edited_df,
                table_name="ORDERS_TMP",
                database="SMOOTHIES",
                schema="PUBLIC",
                overwrite=True
            )

            # Merge back
            session.sql("""
                MERGE INTO SMOOTHIES.PUBLIC.ORDERS tgt
                USING SMOOTHIES.PUBLIC.ORDERS_TMP src
                ON tgt.ORDER_ID = src.ORDER_ID
                WHEN MATCHED THEN
                  UPDATE SET
                    tgt.ORDER_FILLED = src.ORDER_FILLED,
                    tgt.NAME_ON_ORDER = src.NAME_ON_ORDER
            """).collect()

            st.success("Orders updated successfully ✅")
