
import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Sorting vs Formatting Test")

data = {
    "Name": ["A", "B", "C", "D"],
    "Value": [1000.50, 200000.00, 50000.00, 900.00]
}
df = pd.DataFrame(data)

st.subheader("Raw Dataframe (Numeric)")
st.dataframe(df, use_container_width=True)

st.subheader("Styler Formatted (Currency with commas)")
st.dataframe(
    df.style.format({"Value": "${:,.2f}"}),
    use_container_width=True
)

st.subheader("String Converted (Manual)")
df_str = df.copy()
df_str['Value'] = df_str['Value'].apply(lambda x: f"${x:,.2f}")
st.dataframe(df_str, use_container_width=True)
