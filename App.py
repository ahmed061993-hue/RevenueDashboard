import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Excel Dashboard", layout="wide")

st.title("📊 Streamlit Excel Dashboard")

# ---- File Upload ----
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # ---- Clean Columns ----
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    st.subheader("📄 Data Preview")
    st.dataframe(df)

    # ---- Basic Info ----
    st.subheader("📌 Dataset Info")
    col1, col2 = st.columns(2)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])

    # ---- Column Selector ----
    numeric_cols = df.select_dtypes(include="number").columns
    cat_cols = df.select_dtypes(include="object").columns

    if len(numeric_cols) > 0:
        st.subheader("📈 Chart Builder")

        y_col = st.selectbox("Select Numeric Column", numeric_cols)

        if len(cat_cols) > 0:
            x_col = st.selectbox("Select Category Column", cat_cols)

            chart_type = st.radio(
                "Chart Type",
                ["Bar", "Line", "Pie"]
            )

            if chart_type == "Bar":
                fig = px.bar(df, x=x_col, y=y_col)
            elif chart_type == "Line":
                fig = px.line(df, x=x_col, y=y_col)
            else:
                fig = px.pie(df, names=x_col, values=y_col)

            st.plotly_chart(fig, use_container_width=True)

    # ---- Filters ----
    st.subheader("🔍 Filters")

    for col in cat_cols:
        selected = st.multiselect(
            f"Filter {col}",
            options=df[col].dropna().unique()
        )
        if selected:
            df = df[df[col].isin(selected)]

    st.subheader("Filtered Data")
    st.dataframe(df)

else:
    st.info("Please upload an Excel file to begin.")
