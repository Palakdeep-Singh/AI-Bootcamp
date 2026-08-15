import streamlit as st
import preprocessor

# CSS for UI.
st.markdown("""
<style>

    /* Sidebar width */
    [data-testid="stSidebar"] {
        min-width: 350px;
        max-width: 350px;
    }

    /* Sidebar title */
    [data-testid="stSidebar"] h1 {
        font-size: 40px;
    }

    /* Sidebar text */
    [data-testid="stSidebar"] p {
        font-size: 28px;
    }
    [data-testid="stButton"] p {
            font-size: 20px;
        }
    [data-testid="stSelectBox"] p {
            font-size: 20px;
        }
</style>
""", unsafe_allow_html=True)

# set the title
st.sidebar.title("Whatsapp Chat Analyzer")

file_uploaded = st.sidebar.file_uploader("Choose a file")

if file_uploaded is not None:
    bytes_data = file_uploaded.getvalue()
    data_conversion = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data_conversion)
    
    # create users list
    users_list = df['user'].unique().tolist()
    
    # sort the users in ascending order and also add an Overall selectbox option to show analysis for all.
    # also remove group_notification
    
    users_list.remove('group_notification')
    users_list.sort()
    users_list.insert(0,"Overall")
    
    
    # now show the options on sidebar
    st.sidebar.selectbox("Show Analysis for",users_list)
    
    if st.sidebar.button("Show Analysis"):
        st.dataframe(df.head())