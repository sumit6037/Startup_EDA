import pandas as pd

def handle_valuation(df):
    df2_valuation=df.copy()
    df2_valuation["Valuation ($B)"]= df2_valuation["Valuation ($B)"].str.replace('/td>\n12/20/2019\nIndia\nFaridabad\nE-commerce & direct-to-consumer\nChiratae Ventures, PremjiInvest, Softbank\n','')
    df2_valuation["Valuation ($B)"]= df2_valuation["Valuation ($B)"].str.replace('$','').astype(float)
    return df2_valuation

def total_valuation(df):
    df2_valuation=df.copy()
    df2_valuation["Valuation ($B)"]= df2_valuation["Valuation ($B)"].str.replace('/td>\n12/20/2019\nIndia\nFaridabad\nE-commerce & direct-to-consumer\nChiratae Ventures, PremjiInvest, Softbank\n','')
    df2_valuation["Valuation ($B)"]= df2_valuation["Valuation ($B)"].str.replace('$','').astype(float)

    total_val=df2_valuation['Valuation ($B)'].sum().astype(int).astype(str)
    total_val="$ "+total_val
    return total_val

def add_continent_col(df):
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
    return df_5
