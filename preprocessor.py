import pandas as pd

# =============================
# Preprocessing Function
# =============================
def preprocess():
    # Load datasets
    df = pd.read_csv("athlete_events.csv")
    regions = pd.read_csv("noc_regions.csv")

    # Merge with regions
    df = df.merge(regions, how="left", on="NOC")

    # Drop duplicates
    df.drop_duplicates(inplace=True)

    # Fill missing Medal values
    df["Medal"].fillna("No Medal", inplace=True)

    # Convert Medal to dummy columns
    df["Gold"] = (df["Medal"] == "Gold").astype(int)
    df["Silver"] = (df["Medal"] == "Silver").astype(int)
    df["Bronze"] = (df["Medal"] == "Bronze").astype(int)
    df["Total"] = df["Gold"] + df["Silver"] + df["Bronze"]

    return df

# =============================
# Country-Year List
# =============================
def country_year_list(df):
    years = df["Year"].dropna().unique().tolist()
    years.sort()
    years.insert(0, "Overall")

    countries = df["region"].dropna().unique().tolist()
    countries.sort()
    countries.insert(0, "Overall")

    return years, countries

# =============================
# Medal Tally
# =============================
def fetch_medal_tally(df, year, country):
    temp_df = df.copy()

    if year != "Overall":
        temp_df = temp_df[temp_df["Year"] == int(year)]

    if country != "Overall":
        temp_df = temp_df[temp_df["region"] == country]

    medal_tally = (
        temp_df.groupby("region")[["Gold", "Silver", "Bronze", "Total"]]
        .sum()
        .reset_index()
        .sort_values(by=["Gold", "Silver", "Bronze"], ascending=False)
    )

    return medal_tally

# =============================
# Country Yearwise Medal Tally
# =============================
def country_yearwise_medal_tally(df, country):
    temp_df = df[df["region"] == country]

    medal_tally = (
        temp_df.groupby("Year")[["Gold", "Silver", "Bronze", "Total"]]
        .sum()
        .reset_index()
    )

    return medal_tally
