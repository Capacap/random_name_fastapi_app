import pandas as pd
import numpy as np
from typing import List

def process_csv_data(filepath: str) -> pd.DataFrame:
    """Process CSV data and return a DataFrame.

    Args:
        filepath (str): The path to the CSV file.

    Returns:
        pd.DataFrame: The processed DataFrame with additional columns for gender and probabilities.
    """

    # Read csv data
    raw_df = pd.read_csv(filepath, delimiter=';', header=0)
    processed_df = raw_df.copy()

    # Convert name frequency notation into percentage probabilities
    processed_df = raw_df.fillna(0)
    for col in processed_df.columns[2:]:
        processed_df[col] = processed_df[col].apply(lambda x: 2 ** (int(x) - 1) / 100 if x != 0 else 0)

    # Helper method for standardizing column names
    def rename(name: str) -> str:
        name = name.lower() 
        name = name.replace('.', '')
        name = name.replace(' ', '_')
        name = name.replace(',', '_')
        name = name.replace('/', '_')
        return name

    # Standardize column names into snake case
    processed_df.columns = [rename(col) for col in raw_df.columns]

    # Taxonomize the names into male and female
    processed_df['male'] = processed_df['gender'].str.contains('m', regex=False) | processed_df['gender'].str.contains('?', regex=False)
    processed_df['female'] = processed_df['gender'].str.contains('f', regex=False) | processed_df['gender'].str.contains('?', regex=False)

    # Reorder columns for readability and discard redundant columns
    cols = list(processed_df.columns)
    new_order = ['name', 'male', 'female'] + [col for col in cols if col not in ['name', 'male', 'female']]
    processed_df = processed_df[new_order]
    processed_df = processed_df.drop(columns=['gender'])

    return processed_df

def get_countries(df: pd.DataFrame) -> List[str]:
    """Get a list of valid country names.

    Args:
        df (pd.DataFrame): The DataFrame containing name data.

    Returns:
        List[str]: A list of valid country names.
    """
    return [col for col in list(df.columns) if col not in ['name', 'male', 'female']]

def get_random_names(df: pd.DataFrame, country: str, count: int) -> List[str]:
    """Generate a random list of names based on their probabilities for a specific country.

    Args:
        df (pd.DataFrame): The DataFrame containing names and their probabilities.
        country (str): The country for which to retrieve random names.
        count (int): The number of random names to generate.

    Returns:
        List[str]: A list of randomly selected names.
    """
    country_df = df[df[country] != 0].copy()
    prob_series = country_df[country] / country_df[country].sum()
    country_df['probability'] = prob_series

    random_names = np.random.choice(country_df['name'], size=count, replace=False, p=country_df['probability'].values).tolist()
    return random_names

def get_random_male_names(df: pd.DataFrame, country: str, count: int) -> List[str]:
    """Generate a random list of male names (including unisex names) based on their probabilities for a specific country.

    Args:
        df (pd.DataFrame): The DataFrame containing names and their probabilities.
        country (str): The country for which to retrieve random male names.
        count (int): The number of random male names to generate.

    Returns:
        List[str]: A list of randomly selected male names.
    """
    country_df = df[df[country] != 0].copy()
    prob_series = country_df[country] / country_df[country].sum()
    country_df['probability'] = prob_series

    male_df = country_df[country_df['male']].copy()
    if male_df.empty:
        return []
    
    # Normalize the probabilities
    male_df['probability'] /= male_df['probability'].sum()
    random_names = np.random.choice(male_df['name'], size=count, replace=False, p=male_df['probability'].values).tolist()
    return random_names

def get_random_female_names(df: pd.DataFrame, country: str, count: int) -> List[str]:
    """Generate a random list of female names (including unisex names) based on their probabilities for a specific country.

    Args:
        df (pd.DataFrame): The DataFrame containing names and their probabilities.
        country (str): The country for which to retrieve random female names.
        count (int): The number of random female names to generate.

    Returns:
        List[str]: A list of randomly selected female names.
    """
    country_df = df[df[country] != 0].copy()
    prob_series = country_df[country] / country_df[country].sum()
    country_df['probability'] = prob_series

    female_df = country_df[country_df['female']].copy()
    if female_df.empty:
        return []
    
    # Normalize the probabilities
    female_df['probability'] /= female_df['probability'].sum()
    random_names = np.random.choice(female_df['name'], size=count, replace=False, p=female_df['probability'].values).tolist()
    return random_names
