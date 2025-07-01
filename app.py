import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Olympics Analysis", layout="wide")

st.title("🏅 Olympics Data Analysis")

# Load data
df = pd.read_csv("data/athlete_events.csv")
noc = pd.read_csv("data/noc_regions.csv")

# Merge datasets
df = df.merge(noc, on="NOC", how="left")
df.drop_duplicates(inplace=True)

# Feature Engineering
df["Medal"].fillna("No Medal", inplace=True)
df["Participated"] = 1

# Total medals per athlete
total_medals = df[df["Medal"] != "No Medal"].groupby("Name")["Medal"].count().reset_index()
total_medals.columns = ["Name", "Total Medals"]
df = df.merge(total_medals, on="Name", how="left")
df["Total Medals"].fillna(0, inplace=True)

# Tabs for different analysis sections
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Overall Trends", "🌍 Country-wise", "🏅 Sport-wise", "👤 Top Athletes", "⚥ Gender Analysis"
])

with tab1:
    st.header("Total Medals Over Years")
    medal_trend = df[df["Medal"] != "No Medal"].groupby("Year")["Medal"].count().reset_index()
    fig = px.line(medal_trend, x="Year", y="Medal", markers=True, title="Total Medals Over Time")
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Top Countries by Total Medals")
    top_countries = df[df["Medal"] != "No Medal"].groupby("region")["Medal"].count().reset_index()
    top_countries = top_countries.sort_values("Medal", ascending=False).head(10)
    fig = px.bar(top_countries, x="region", y="Medal", color="region", title="Top 10 Countries")
    st.plotly_chart(fig, use_container_width=True)

    country = st.selectbox("Select a Country", sorted(df["region"].dropna().unique()))
    country_df = df[(df["region"] == country) & (df["Medal"] != "No Medal")]
    medals_by_year = country_df.groupby("Year")["Medal"].count().reset_index()
    st.subheader(f"Year-wise Medal Count for {country}")
    fig2 = px.line(medals_by_year, x="Year", y="Medal", title=f"{country} - Medals Over Years")
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.header("Sport-wise Medal Count")
    sport_medals = df[df["Medal"] != "No Medal"].groupby("Sport")["Medal"].count().sort_values(ascending=False).reset_index()
    fig = px.bar(sport_medals.head(15), x="Sport", y="Medal", color="Sport", title="Top 15 Sports by Medal Count")
    st.plotly_chart(fig, use_container_width=True)

    sport = st.selectbox("Select a Sport", sorted(df["Sport"].dropna().unique()))
    sport_df = df[(df["Sport"] == sport) & (df["Medal"] != "No Medal")]
    sport_country = sport_df.groupby("region")["Medal"].count().sort_values(ascending=False).head(10).reset_index()
    fig2 = px.pie(sport_country, values="Medal", names="region", title=f"{sport} - Top 10 Countries")
    st.plotly_chart(fig2)

with tab4:
    st.header("Top Athletes with Most Medals")
    top_athletes = df[df["Medal"] != "No Medal"].groupby(["Name", "region"])["Medal"].count().reset_index()
    top_athletes.columns = ["Athlete", "Country", "Total Medals"]
    top_athletes = top_athletes.sort_values("Total Medals", ascending=False).head(10)
    st.dataframe(top_athletes)

with tab5:
    st.header("Gender Participation Over the Years")
    gender_df = df.drop_duplicates(subset=["Name", "region", "Sex", "Year"])
    gender_counts = gender_df.groupby(["Year", "Sex"])["Name"].count().reset_index()
    gender_counts.rename(columns={"Name": "Count"}, inplace=True)
    fig = px.line(gender_counts, x="Year", y="Count", color="Sex", title="Male vs Female Participation")
    st.plotly_chart(fig, use_container_width=True)
