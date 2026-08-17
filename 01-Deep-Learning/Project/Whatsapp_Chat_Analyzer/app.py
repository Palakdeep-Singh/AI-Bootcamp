import streamlit as st
import preprocessor
import helper

# CSS for UI.
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Sidebar width */
    [data-testid="stSidebar"] {
        min-width: 350px;
        max-width: 350px;
        background: linear-gradient(180deg, #111827 0%, #1f2937 100%);
    }

    [data-testid="stSidebar"] h1 {
        font-size: 40px;
        color: #f9fafb;
        margin-bottom: 1rem;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div {
        font-size: 18px;
        color: #f3f4f6;
    }

    [data-testid="stButton"] p {
        font-size: 20px;
    }

    [data-testid="stSelectBox"] p {
        font-size: 20px;
    }

    .metric-card {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border-radius: 18px;
        padding: 1.2rem 1rem;
        border: 1px solid rgba(148, 163, 184, 0.25);
        box-shadow: 0 8px 30px rgba(15, 23, 42, 0.18);
        height: 100%;
    }

    .metric-label {
        color: #cbd5e1;
        font-size: 0.88rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.5rem;
    }

    .metric-value {
        color: #f8fafc;
        font-size: 2rem;
        font-weight: 700;
        line-height: 1.2;
    }

    .section-title {
        color: #e2e8f0;
        margin-bottom: 1rem;
    }

    .stDataFrame {
        font-size: 1rem;
    }

    div[data-testid="stDataFrame"] {
        min-height: 420px;
        width: 100% !important;
        max-width: 100% !important;
    }

    div[data-testid="stDataFrame"] > div {
        max-height: 520px;
        width: 100% !important;
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
    # remove notification rows if they exist
    
    if 'group_notification' in users_list:
        users_list.remove('group_notification')
        
    users_list.sort()
    users_list.insert(0,"Overall")
    
    # now show the options on sidebar and whatever selected store in variable.
    selected_user = st.sidebar.selectbox("Show Analysis for",users_list)
    
    if st.sidebar.button("Show Analysis"):
        st.header("Chat Summary")

        num_msgs, words_count, media,links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Total Messages</div>
                    <div class="metric-value">{num_msgs}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Total Words</div>
                    <div class="metric-value">{words_count}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">Media Shared</div>
                    <div class="metric-value">{media}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        with col4:
            st.markdown(
                        f"""
                        <div class="metric-card">
                            <div class="metric-label">Links Shared</div>
                            <div class="metric-value">{links}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                        )
                                       
            st.write("")
            
        if selected_user == "Overall":
            preview_df = df.sort_values('date').tail(5)
        else:
            preview_df = df[df['user'] == selected_user].sort_values('date').tail(5)

        ## show table preview under the cards.
        preview_df = preview_df[['user', 'message', 'year', 'month', 'day', 'hour', 'minute']].reset_index(drop=True)
        
        preview_df.insert(0, 'Sr. No', range(1, len(preview_df) + 1))
        
        st.table(preview_df)