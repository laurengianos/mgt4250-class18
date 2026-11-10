import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Class 17")
st.header("Streamlit Practice")
st.subheader("Data Structure")
st.write("By Lauren :D")

#begin code
df = pd.read_excel("sample_-_superstore.xls")
df = df[df["Country/Region"]=="United States"]

#filter section
st.write(df.head(3))

all_states = df["State/Province"].unique()
target_states = st.multiselect("Choose States", options=all_states, 
                               default=["North Carolina", "South Carolina", "Georgia", "Florida"])

df=df[df["State/Province"].isin(target_states)] #connecting target_states variable to all later visualizations

#first section
st.subheader("Visualizations")

col1, col2 = st.columns([7, 3])
with col1:
    
    profit_sums_state = df.groupby("State/Province")["Profit"].sum()
    
    sale_sums_state = df.groupby("State/Province")["Sales"].sum()
    
    profit_margin_state = profit_sums_state/sale_sums_state
    profit_margin_state = profit_margin_state.reset_index(name="Profit Margin")

    fig1 = px.choropleth(
    locations=profit_margin_state["State/Province"],
    locationmode="USA-states",
    color=profit_margin_state["Profit Margin"],
    scope="usa",
    color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig1, width="stretch")  #using this instead of fig1.show()


with col2:
    profit_sums_cat=df.groupby("Category")["Profit"].sum()
    sale_sums_cat=df.groupby("Category")["Sales"].sum()
    profit_margin_cat=profit_sums_cat/sale_sums_cat
    profit_margin_cat=profit_margin_cat.reset_index(name="Profit Margin")
    fig2 = px.bar(profit_margin_cat, x="Category",
    y="Profit Margin", color="Category")
    st.plotly_chart(fig2, width="stretch")

#new section
col3, col4 = st.columns([6, 4])
with col3:
    df["YearMonth"] = pd.to_datetime(df["Order Date"]).dt.strftime("%Y-%m")
    a = df.groupby(["Category", "YearMonth"])["Profit"].sum()
    b = df.groupby(["Category", "YearMonth"])["Sales"].sum()
    profit_margin_category_ym = a/b
    profit_margin_category_ym = profit_margin_category_ym.reset_index(name="Profit Margin")
    fig3 = px.line(profit_margin_category_ym,
    x="YearMonth", y="Profit Margin", color="Category")
    st.plotly_chart(fig3, width="stretch")

with col4:
    fig4 = px.treemap(
    df,
    path=['Category', 'Sub-Category'],
    values='Sales',
    color='Category',
    title='Proportion of Sales by Sub-Category'
    )
    st.plotly_chart(fig4, width="stretch")
            