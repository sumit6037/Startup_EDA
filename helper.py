import numpy as np
import pandas as pd
import plotly.express as px
import preprocessor

def filter_unicorn(df,year,country):
    flag=0
    if year =='Overall' and country == 'Overall':
        temp_df=df
    if year !='Overall' and country == 'Overall':
        temp_df=df[ (df['Year']==year)]
    if year =='Overall' and country != 'Overall':
        flag=1
        temp_df=df[ (df['Country']==country)]
    if year !='Overall' and country != 'Overall':
        temp_df=df[(df['Year']==year) & (df["Country"]==country)]


    #temp
    temp1=temp_df.copy()
    temp1["Valuation ($B)"]= temp1["Valuation ($B)"].str.replace('/td>\n12/20/2019\nIndia\nFaridabad\nE-commerce & direct-to-consumer\nChiratae Ventures, PremjiInvest, Softbank\n','')
    temp1["Valuation ($B)"]= temp1["Valuation ($B)"].str.replace('$','').astype(float)
    #temp1
    df_3=temp1.groupby('Country')["Valuation ($B)"].sum().to_frame(name='Total_Valuation ($B)').reset_index()
    df_3['Total_Valuation ($B)'] ='$' + df_3['Total_Valuation ($B)'].astype(str)
    df_3['Total_Valuation ($B)'] = df_3['Total_Valuation ($B)'].str.slice(0, 8)
    #df_3
    if flag==1:
        df_4=temp1.groupby('Year')["Company"].count().to_frame(name='No of Startups').reset_index()
        df_5=temp1.groupby('Year')["Valuation ($B)"].sum().to_frame(name='Total Valuation ($B)').reset_index()
        df_5['Total Valuation ($B)'] ='$' + df_5['Total Valuation ($B)'].astype(str)
        #df_5['Total_Valuation ($B)'] = df_5['Total Valuation ($B)'].str.slice(0, 8)
        extracted_col=df_5['Total Valuation ($B)']
        startup_va=df_4.join(extracted_col)
    else:
        df_4=temp1.groupby('Country')["Company"].count().to_frame(name='No of Startups').reset_index()
        startup_va=df_4.merge(df_3[['Country','Total_Valuation ($B)']])
    return startup_va

def unicorns_created_over_year(df):
    unicorns_created_per_year=df['Year'].value_counts().reset_index().sort_values('index')
    unicorns_created_per_year.rename(columns={'index': 'Year', 'Year': 'Startups Created'}, inplace=True)
    return unicorns_created_per_year

def total_valuation_over_year(df):
    df_valuation=df.copy()

    df_valuation["Valuation ($B)"]= df_valuation["Valuation ($B)"].str.replace('/td>\n12/20/2019\nIndia\nFaridabad\nE-commerce & direct-to-consumer\nChiratae Ventures, PremjiInvest, Softbank\n','')
    df_valuation["Valuation ($B)"]= df_valuation["Valuation ($B)"].str.replace('$','').astype(float)
    valuation_over_time=df_valuation.groupby('Year')['Valuation ($B)'].sum().reset_index().sort_index()
    return valuation_over_time

def share_of_unicorn(df):
    df_5=df.copy()
    df_5.loc[(df['Country']=='Colombia') | (df['Country']=='Brazil') | (df['Country']=='Argentina') | (df['Country']=='Ecuador') | (df['Country']=='Chile')
         ,"Continent"]= 'South America'

    df_5.loc[(df['Country']=='Seychelles') | (df['Country']=='Nigeria') | (df['Country']=='Senegal') | (df['Country']=='South Africa')
            ,"Continent"]= 'Africa'

    df_5.loc[(df['Country']=='United Kingdom') | (df['Country']=='Germany') | (df['Country']=='Ireland')| (df['Country']=='Sweden') | (df['Country']=='Estonia') | (df['Country']=='Netherlands') | (df['Country']=='France') | (df['Country']=='Finland') | (df['Country']=='Belgium') | (df['Country']=='Denmark') | (df['Country']=='Switzerland') | (df['Country']=='Lithuania') | (df['Country']=='Austria') | (df['Country']=='Spain') | (df['Country']=='Luxembourg') | (df['Country']=='Croatia') | (df['Country']=='Norway') | (df['Country']=='Czech Republic') | (df['Country']=='Italy')
            ,"Continent"]= 'Europe'

    df_5.loc[(df['Country']=='China') | (df['Country']=='India') | (df['Country']=='Indonesia') | (df['Country']=='Hong Kong') | (df['Country']=='South Korea') | (df['Country']=='Vietnam') | (df['Country']=='Singapore') | (df['Country']=='United Arab Emirates') | (df['Country']=='Philippines') | (df['Country']=='Malaysia') | (df['Country']=='Thailand') | (df['Country']=='Israel') | (df['Country']=='Japan') | (df['Country']=='Turkey')
             ,"Continent"]= 'Asia'

    df_5.loc[(df['Country']=='Australia')
             ,"Continent"]= 'Oceania'

    df_5.loc[(df['Country']=='United States') | (df['Country']=='Bahamas') | (df['Country']=='Mexico') | (df['Country']=='Canada') | (df['Country']=='Bermuda')
             ,"Continent"]= 'North America'
    startup_count=df_5.groupby('Continent')['Company'].count().reset_index().sort_values('Company')
    startup_count.rename(columns={'Company': 'Startups Count'}, inplace=True)
    return startup_count

def share_of_unicorn_by_country(df):
    company_count=df.groupby('Country')['Company'].count().reset_index().sort_values('Company')
    company_count.rename(columns={'Company': 'Startups Count'}, inplace=True)
    return company_count

def share_of_unicorn_by_city(df):
    city_count=df.groupby('City')['Company'].count().reset_index().sort_values('Company')
    city_count.rename(columns={'Company': 'Startups Count'}, inplace=True)
    return city_count


from itertools import chain
from operator import length_hint



def unicorn_investors(df):
    df_inves=df.copy()
    df_inves1=df_inves["Select Investors"].str.split(",",n=4,expand=True)
    df_inves["Select Investors 1"]= df_inves1[0]
    df_inves["Select Investors 2"]= df_inves1[1]
    df_inves["Select Investors 3"]= df_inves1[2]
    df_inves["Select Investors 4"]= df_inves1[3]
    investor=[]
    l=list(set(df['Country'].to_list()))
    for i in l:
        df_argen=df_inves[df_inves["Country"]== i]
        a1=df_argen[["Select Investors 1","Select Investors 2","Select Investors 3","Select Investors 4"]].to_numpy()
        list_1 = a1.tolist()
        flatten_list = list(set(list(chain.from_iterable(list_1))))
        length_flatten_list=len(flatten_list)
        investor.append(length_flatten_list)
        investor_df=pd.DataFrame({'Investor Count':investor})
        country_df=pd.DataFrame({'Country':l})
        t=pd.concat([investor_df,country_df], axis=1, join='inner').sort_values("Investor Count")
        #fig = px.bar(t.tail(10), x="Country", y="Investor Count")
    return t



# def unicorn_investors(df):
#     l=list(set(df['Country'].to_list()))
#     ap=[]
#     for i in l:
#         c=df[df['Country']==i]
#         c1=c['Select Investors'].to_list()
#         l1=len(list(set(c1)))
#         ap.append(l1)
#     investor_count=pd.DataFrame(list(zip(l, ap)),columns =['Country', 'Investor Count']).sort_values('Investor Count')
#     return investor_count

def startup(df):
    df2=df.copy()

    df2["Valuation ($B)"]= df2["Valuation ($B)"].str.replace('/td>\n12/20/2019\nIndia\nFaridabad\nE-commerce & direct-to-consumer\nChiratae Ventures, PremjiInvest, Softbank\n','')
    df2["Valuation ($B)"]= df2["Valuation ($B)"].str.replace('$','').astype(float)

    df2['Valuation ($B)']
    df3=df2.groupby('Country')["Valuation ($B)"].sum().to_frame(name='SUM').reset_index()
    df3['Total_Valuation ($B)'] ='$' + df3['SUM'].astype(str)
    df3['Total_Valuation ($B)'] = df3['Total_Valuation ($B)'].str.slice(0, 8)

    df4=df.groupby('Country')["Company"].count().to_frame(name='No of Startups').reset_index()
    startup_analysis=df4.merge(df3[['Country','Total_Valuation ($B)']])

    return startup_analysis


def years_country_city_industry(df):

    #df['Year']=df['Year'].astype(str)
    years=df["Year"].unique().tolist()
    years.sort()
    years.insert(0,'Overall')

    country=df['Country'].unique().tolist()
    country.sort()
    country.insert(0,'Overall')

    city= np.unique(df['City'].dropna().values).tolist()
    city.sort()
    city.insert(0,'Overall')

    industry=df["Industry"].unique().tolist()
    industry.sort()
    industry.insert(0,'Overall')

    return years,country,city,industry

def country_drop_down(df):
    country=df['Country'].unique().tolist()
    country.sort()
    country.insert(0,'Overall')

    return country


def filter_country(df,country):
    flag=0
    if country == 'Overall':
        temp_df=df
    if country != 'Overall':
        flag=1
        temp_df=df[ (df['Country'] == country)]
    #temp
    temp1=temp_df.copy()
    temp1["Valuation ($B)"]= temp1["Valuation ($B)"].str.replace('/td>\n12/20/2019\nIndia\nFaridabad\nE-commerce & direct-to-consumer\nChiratae Ventures, PremjiInvest, Softbank\n','')
    temp1["Valuation ($B)"]= temp1["Valuation ($B)"].str.replace('$','').astype(float)
    #temp1
    df_3=temp1.groupby('Country')["Valuation ($B)"].sum().to_frame(name='Total_Valuation ($B)').reset_index()
    df_3['Total_Valuation ($B)'] ='$' + df_3['Total_Valuation ($B)'].astype(str)
    df_3['Total_Valuation ($B)'] = df_3['Total_Valuation ($B)'].str.slice(0, 8)
    #df_3
    if flag==1:
        df_4=temp1.groupby('Year')["Company"].count().to_frame(name='No of Startups').reset_index()
        df_5=temp1.groupby('Year')["Valuation ($B)"].sum().to_frame(name='Total Valuation ($B)').reset_index()
        df_5['Total Valuation ($B)'] ='$' + df_5['Total Valuation ($B)'].astype(str)
        #df_5['Total_Valuation ($B)'] = df_5['Total Valuation ($B)'].str.slice(0, 8)
        extracted_col=df_5['Total Valuation ($B)']
        startup_va=df_4.join(extracted_col)
    else:
        df_4=temp1.groupby('Country')["Company"].count().to_frame(name='No of Startups').reset_index()
        startup_va=df_4.merge(df_3[['Country','Total_Valuation ($B)']])
    return startup_va

def filter_country_1(df,country):
    flag=0
    if country == 'Overall':
        temp_df=df
    if country != 'Overall':
        flag=1
        temp_df=df[ (df['Country'] == country)]
    #temp
    temp1=temp_df.copy()
    temp1["Valuation ($B)"]= temp1["Valuation ($B)"].str.replace('/td>\n12/20/2019\nIndia\nFaridabad\nE-commerce & direct-to-consumer\nChiratae Ventures, PremjiInvest, Softbank\n','')
    temp1["Valuation ($B)"]= temp1["Valuation ($B)"].str.replace('$','').astype(float)

    return temp1.head(10)

def investor_filter(df,country):
    f_list=[]
    df_new=df[df["Country"]== country]
    df_new['Select Investors'] = df_new['Select Investors'].astype(str)
    df_new['Select Investors'] = df_new['Select Investors'].replace('\[|\'|\"|\]| ', '', regex=True)
    df_new['Select Investors'] = df_new['Select Investors'].str.split(',')
    final_list = [x for xs in df_new['Select Investors'].tolist() for x in xs]
    for i in final_list:
        f_list.append(i)
    df_new=pd.DataFrame(f_list,columns=["Investors"]).value_counts().reset_index()
    df_new.rename(columns={0: 'Investors Count'}, inplace=True)

    return df_new.head(10)

def valuation_countrywise(df,country):
    temp1=df.copy()
    temp1["Valuation ($B)"]= temp1["Valuation ($B)"].str.replace('/td>\n12/20/2019\nIndia\nFaridabad\nE-commerce & direct-to-consumer\nChiratae Ventures, PremjiInvest, Softbank\n','')
    temp1["Valuation ($B)"]= temp1["Valuation ($B)"].str.replace('$','').astype(float)
    #temp1
    # df_3=temp1.groupby('Country')["Valuation ($B)"].sum().to_frame(name='Total_Valuation ($B)').reset_index()
    # df_3['Total_Valuation ($B)'] ='$' + df_3['Total_Valuation ($B)'].astype(str)
    # df_3['Total_Valuation ($B)'] = df_3['Total_Valuation ($B)'].str.slice(0, 8)

    val_1=temp1[temp1["Country"] == country]
    val_1.groupby("Industry")["Valuation ($B)"].sum()

    return val_1
