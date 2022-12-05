import streamlit as st
import pandas as pd
import plotly.express as px

import helper,preprocessor

df=pd.read_csv("World_Wide-Unicorn-Company-List.csv")

st.sidebar.header("Startup Analysis")

user_menu=st.sidebar.radio(
    'Select an Option',
    ('Unicorn List','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)

#st.dataframe(df)

if user_menu == 'Unicorn List':
    st.sidebar.header("Filters")
    years,country,city,industry=helper.years_country_city_industry(df)

    selected_year=st.sidebar.selectbox("Year",years)
    selected_country=st.sidebar.selectbox("HQ Country",country)

    startup_count = helper.filter_unicorn(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Unicorn List")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title("Unicorn List in " + str(selected_year))
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(selected_country + " Unicorn List")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(" Unicorn List of " + selected_country + " in "+str(selected_year))
    st.table(startup_count)

if user_menu == 'Overall Analysis':
    company = df['Company'].unique().shape[0]
    country = df['Country'].unique().shape[0]
    city = df['City'].unique().shape[0]
    industry = df['Industry'].unique().shape[0]
    investor_list=df["Select Investors"].to_list()
    investor_list=len(list(set(investor_list)))
    valuation=preprocessor.total_valuation(df)

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Company")
        st.title(company)
    with col2:
        st.header("Country")
        st.title(country)
    with col3:
        st.header("City")
        st.title(city)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Industry")
        st.title(industry)
    with col2:
        st.header("Investors")
        st.title(investor_list)
    with col3:
        st.header("Valuation ($B)")
        st.title(valuation)

    st.title("Trends")

    unicorns_created_per_year = helper.unicorns_created_over_year(df)
    fig = px.line(unicorns_created_per_year, x="Year", y="Startups Created")
    st.header("Unicorns Created over the years")
    st.plotly_chart(fig)

    total_valuation_per_year = helper.total_valuation_over_year(df)
    fig = px.line(total_valuation_per_year, x="Year", y="Valuation ($B)")
    st.header("Total Funds Provided To The Unicorns over the years")
    st.plotly_chart(fig)

    share_of_unicorn_by_region_continent = helper.share_of_unicorn(df)
    fig = px.bar(share_of_unicorn_by_region_continent, x="Continent", y="Startups Count")
    st.header("Share of Unicorns Worldwide by Continent")
    st.plotly_chart(fig)

    share_of_unicorn_by_region_country = helper.share_of_unicorn_by_country(df)
    fig = px.bar(share_of_unicorn_by_region_country.tail(10), x="Country", y="Startups Count")
    st.header("Share of Unicorns Worldwide by Country")
    st.plotly_chart(fig)

    share_of_unicorn_by_region_city = helper.share_of_unicorn_by_city(df)
    fig = px.bar(share_of_unicorn_by_region_city.tail(10), x="City", y="Startups Count")
    st.header("Share of Unicorns Worldwide by City")
    st.plotly_chart(fig)

    startup_investors = helper.unicorn_investors(df)
    fig = px.bar(startup_investors.tail(10), x="Country", y="Investor Count")
    st.header("Unicorns Investors ")
    st.plotly_chart(fig)


if user_menu == 'Country-wise Analysis':
    st.sidebar.header("Filters")
    country=helper.country_drop_down(df)

    selected_country = st.sidebar.selectbox("HQ Country",country)

    startup_count = helper.filter_country(df,selected_country)

    if selected_country == 'Overall':
        st.title("Overall Unicorn List")
        st.table(startup_count)
    if selected_country != 'Overall':
        st.title(selected_country + " Unicorn List")

        st.table(startup_count)

        startup_investors = helper.filter_country(df,selected_country)
        fig = px.bar(startup_investors, x="Year", y="No of Startups")
        st.header("No Of Unicorns Created")
        st.plotly_chart(fig)

        startup_investors_1 = helper.filter_country(df,selected_country)
        fig = px.line(startup_investors_1, x="Year", y="Total Valuation ($B)")
        st.header("Total Funds Provided To The Unicorns over the years")
        st.plotly_chart(fig)

        startup_investors_2 = helper.filter_country_1(df,selected_country)
        fig = px.bar(startup_investors_2, x="Company", y="Valuation ($B)")
        st.header("Leading Unicorns in "+selected_country)
        st.plotly_chart(fig)

        leading_investors = helper.investor_filter(df,selected_country)
        fig = px.bar(leading_investors, x="Investors", y="Investors Count")
        st.header("Leading Investors in "+selected_country)
        st.plotly_chart(fig)

        countrywise_valuation = helper.valuation_countrywise(df,selected_country)
        fig = px.bar(countrywise_valuation, x="Industry", y="Valuation ($B)")
        st.header("Market Valuation o Unicorns(IndustryWise) in "+selected_country)
        st.plotly_chart(fig)



