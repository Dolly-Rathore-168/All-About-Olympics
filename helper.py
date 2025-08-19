import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Assuming df is your preprocessed DataFrame
# from preprocessor import preprocess
# df = preprocess()

def yearwise_medal_tally(df, country=None):
    """
    Returns a DataFrame with total medals per year.
    Optionally filter by a given country (region).
    """
    # Only keep rows where Medal and region are present
    temp_df = df.dropna(subset=['Medal', 'region'])

    # Filter by country if provided
    if country and country != 'Overall':
        temp_df = temp_df[temp_df['region'] == country]

    # Group and count medals year-wise
    tally = (
        temp_df.groupby('Year')['Medal']
        .count()
        .reset_index()
        .rename(columns={'Medal': 'Total_Medals'})
        .sort_values('Year')  # Ensure chronological order
    )

    return tally

# Example usage for all countries
all_years = yearwise_medal_tally(df)
print("All countries:\n", all_years.head())

# Example usage for India
india_years = yearwise_medal_tally(df, country='India')
print("\nIndia:\n", india_years.head())

# Plotting India medal tally over years
plt.figure(figsize=(12, 6))
sns.lineplot(data=india_years, x='Year', y='Total_Medals', marker='o')
plt.title("India: Year-wise Medal Tally", fontsize=14)
plt.xlabel("Year", fontsize=12)
plt.ylabel("Total Medals", fontsize=12)
plt.xticks(rotation=45)
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()
