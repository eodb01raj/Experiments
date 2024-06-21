import streamlit as st
import pandas as pd
import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")
text_string = "Health Officer means the Municipal Health Officer or District Health Officer or such other official as may be appointed by the State Government in that behalf."
# doc = nlp(text_string)
# for token in doc:
#     st.write(token.text)
# for ent in doc.ents:
#     st.write(ent.text, ent.start_char, ent.end_char, ent.label_)
# return non-common words and their frequency in text_string
def get_non_common_words(text_string):
    doc = nlp(text_string)
    non_common_words = {}
    for token in doc:
        if token.is_stop or token.is_punct:
            continue
        if token.text.lower() in non_common_words:
            non_common_words[token.text.lower()] += 1
        else:
            non_common_words[token.text.lower()] = 1
    return non_common_words
st.write(get_non_common_words(text_string))
def load_data(file_path, sheet_name):
    """
    Load data from an Excel file.

    Args:
        file_path (str): The path to the Excel file.
        sheet_name (str): The sheet name to load from the Excel file.

    Returns:
        pd.DataFrame: The loaded DataFrame.
    """
    return pd.read_excel(file_path, sheet_name=sheet_name)

def filter_dataframe(df, column):
    """
    Filter the DataFrame based on non-null values in the specified column.

    Args:
        df (pd.DataFrame): The DataFrame to filter.
        column (str): The column to filter by.

    Returns:
        pd.DataFrame: The filtered DataFrame.
    """
    return df[df[column].notnull()]

def search_dataframe(df, column, search_value):
    """
    Search the DataFrame for rows where the specified column contains the search value.

    Args:
        df (pd.DataFrame): The DataFrame to search.
        column (str): The column to search within.
        search_value (str): The value to search for.

    Returns:
        pd.DataFrame: The DataFrame containing the search results.
    """
    return df[df[column].str.contains(search_value, case=False, na=False)]

def highlight_text(text, search_value):
    """
    Highlight the search value in the given text.

    Args:
        text (str): The text to highlight.
        search_value (str): The value to highlight in the text.

    Returns:
        str: The text with the search value highlighted.
    """
    highlighted_text = text.replace(
        search_value, f"<mark style='background-color: yellow'>{search_value}</mark>"
    )
    return highlighted_text

def display_search_results(df, search_value):
    """
    Display search results in the Streamlit main area with highlighted search text.

    Args:
        df (pd.DataFrame): The DataFrame containing search results.
        search_value (str): The value to highlight in the search results.
    """
    st.write("Number of rules found for:", search_value)
    st.subheader(len(df))
    grouped_rules = df.groupby('Chapter')['rule_number'].unique()
    grouped_clause = df.groupby('rule_number')['clause'].unique()

    for chapter, rule_numbers in grouped_rules.items():
        st.write(f"**{chapter}**: {', '.join(map(str, rule_numbers))}")
    for rule_numbers, clause in grouped_clause.items():
            st.write(f"**{rule_numbers}**: {', '.join(map(str, clause))}")
        # else:
        #     st.write(f"**{rule_numbers}**")

    st.write("---")
    for index, row in df.iterrows():
        st.write(f"**Chapter**: {row['Chapter']}")
        st.write(f"**Rule**: {row['rule_number']}")
        cleaned_highlighted = highlight_text(row['Cleaned'], search_value)
        st.markdown(f"**Cleaned**: {cleaned_highlighted}", unsafe_allow_html=True)
        st.write("---")

# Load data
df = load_data('Clean filtered rajasthan factories rules excel table.xlsx', sheet_name='Table1')

# Get column options
column_options = df.columns

# Streamlit UI
st.title("Rajasthan Factories Rules")

with st.sidebar:
    st.header("Filters")
    #options = st.selectbox("Select Column to Filter By", column_options)
    options = "Cleaned"
    filtered_df = filter_dataframe(df, options)
    st.write("Filtered Data:")
    #st.dataframe(filtered_df)

    search_value = st.text_input("Enter search value")
    if st.button("Search"):
        search_results_df = search_dataframe(filtered_df, options, search_value)
        if not search_results_df.empty:
            st.write("Search Results:")
            st.dataframe(search_results_df[options])
        else:
            st.write("No results found.")

if search_value:
    search_results_df = search_dataframe(filtered_df, options, search_value)
    if not search_results_df.empty:
        display_search_results(search_results_df, search_value)
    else:
        st.write("No results found.")

st.write("Filtered Data:")
st.dataframe(filtered_df)
