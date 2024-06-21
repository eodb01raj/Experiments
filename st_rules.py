import streamlit as st
import pandas as pd
import time
df = pd.read_excel('Clean filtered rajasthan factories rules excel table.xlsx', sheet_name='Table1')

a = df.columns

options = st.selectbox(
    "What do you choose",
    a
    )
# filter the dataframe based on the selected options where the option is not null
df1 = df[df[options].notnull()]
st.dataframe(df1)


with st.sidebar:
    st.sidebar.header("Search")
    search_value = st.text_input("Enter search value")
    df3 = df1[df1[options].str.contains(search_value)]
    chapters = df3['Chapter'].unique()
    rules = df3['rule_number'].unique()
    # group sub-rules by rule_number and rule_number by chapter and print the unique values
    

   


    #st.dataframe(df3)
    
    
           
    if search_value:
        # number of rows in df3
        st.write("Number of rules found:")
        st.subheader(len(df3))
        df4 = df3.groupby('Chapter')['rule_number'].unique()
        for chapter, rule_numbers in df4.items():
            st.write(f"{chapter}: {rule_numbers}")
        count = 0
       # write the 5 values in rows of the dataframe to the sidebar in the order chapter, section, sub-section, rule, cleaned
        for index, row in df3.iterrows():
            st.sidebar.write(row['Chapter'])
            st.sidebar.write( "Rule", row['rule_number'])
            st.sidebar.write(row['Cleaned'])
            count += 1
            if count == 5:
                break
    