import streamlit as st
import plotly.figure_factory as ff
import preprocessor as prep

# =============================
# Load Preprocessed Data
# =============================
df = prep.preprocess()

st.sidebar.title("Olympics Analysis")
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally', 'Overall Analysis', 'Country-wise Analysis', 'Athlete-wise Analysis')
)

# =============================
# Medal Tally
# =============================
if user_menu == 'Medal Tally':
    st.sidebar.header("Medal Tally")
    years, countries = prep.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year", years)
    selected_country = st.sidebar.selectbox("Select Country", countries)

    medal_tally = prep.fetch_medal_tally(df, selected_year, selected_country)

    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("Overall Medal Tally")
    elif selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f"Medal Tally in {selected_year}")
    elif selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f"Overall Performance of {selected_country}")
    else:
        st.title(f"{selected_country} in {selected_year}")

    st.table(medal_tally)

# =============================
# Overall Analysis
# =============================
elif user_menu == 'Overall Analysis':
    editions = df['Year'].nunique() - 1
    cities = df['City'].nunique()
    sports = df['Sport'].nunique()
    events = df['Event'].nunique()
    athletes = df['Name'].nunique()
    nations = df['region'].nunique()

    st.title("Top Statistics")
    col1, col2, col3 = st.columns(3)
    with col1: st.header("Editions"); st.title(editions)
    with col2: st.header("Hosts"); st.title(cities)
    with col3: st.header("Sports"); st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1: st.header("Events"); st.title(events)
    with col2: st.header("Nations"); st.title(nations)
    with col3: st.header("Athletes"); st.title(athletes)

    # Age Distribution of Medalists
    st.title("Distribution of Athlete Ages (by Medal)")
    overall_ages = df['Age'].dropna()
    gold_ages = df[df['Medal'] == 'Gold']['Age'].dropna()
    silver_ages = df[df['Medal'] == 'Silver']['Age'].dropna()
    bronze_ages = df[df['Medal'] == 'Bronze']['Age'].dropna()

    if not overall_ages.empty:
        fig = ff.create_distplot(
            [overall_ages, gold_ages, silver_ages, bronze_ages],
            ['Overall Age', 'Gold Medalists', 'Silver Medalists', 'Bronze Medalists'],
            show_hist=False,
            show_rug=False
        )
        st.plotly_chart(fig)
    else:
        st.write("No age data available.")

# =============================
# Country-wise Analysis
# =============================
elif user_menu == 'Country-wise Analysis':
    st.sidebar.title("Country-wise Analysis")
    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()
    selected_country = st.sidebar.selectbox("Select a Country", country_list)

    country_df = prep.country_yearwise_medal_tally(df, selected_country)
    st.title(f"{selected_country} Medal Tally over the years")
    st.line_chart(country_df[['Year', 'Total']].set_index('Year'))

# =============================
# Athlete-wise Analysis
# =============================
elif user_menu == 'Athlete-wise Analysis':
    st.title("Distribution of Age of Athletes")
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    overall_ages = athlete_df['Age'].dropna()
    gold_ages = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    silver_ages = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    bronze_ages = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    if not overall_ages.empty:
        fig = ff.create_distplot(
            [overall_ages, gold_ages, silver_ages, bronze_ages],
            ['Overall Age', 'Gold Medalists', 'Silver Medalists', 'Bronze Medalists'],
            show_hist=False,
            show_rug=False
        )
        st.plotly_chart(fig)
    else:
        st.write("No age data available.")
