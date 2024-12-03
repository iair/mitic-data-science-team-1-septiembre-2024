import json
import os
import numpy as np
import pandas as pd
from typing import List, Dict, Any

def null_values_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates a table showing the count and percentage of null values in each column.
    
    Args:
        df (pd.DataFrame): The input DataFrame.
    
    Returns:
        pd.DataFrame: A DataFrame with columns `Null Count` and `Percentage`.
    """
    null_count = df.isnull().sum()
    null_percentage = (null_count / len(df)) * 100
    null_table = pd.DataFrame({
        'Null Count': null_count,
        'Percentage': null_percentage
    }).sort_values(by='Null Count', ascending=False)
    
    return null_table

def transform_columns(df: pd.DataFrame, columns: list, dtype: type) -> pd.DataFrame:
    """
    Generalized function to transform specified columns in a DataFrame to a given data type.
    
    Args:
        df (pd.DataFrame): The DataFrame to transform.
        columns (list): List of column names to transform.
        dtype (type or str): Desired data type ('category', 'int', 'float', 'bool', 'str', etc.).
        
    Returns:
        pd.DataFrame: The updated DataFrame with transformed columns.
    """
    for col in columns:
        if col in df.columns:
            try:
                df[col] = df[col].astype(dtype)
            except Exception as e:
                print(f"Error converting column '{col}' to {dtype}: {e}")
        else:
            print(f"Column '{col}' not found in DataFrame.")
    return df


def map_column_values(df: pd.DataFrame, column: str, mapping: Dict) -> pd.DataFrame:
    """
    Maps the values of a specified column in a DataFrame using a given dictionary mapping.

    Args:
        df (pd.DataFrame): The DataFrame containing the column to be transformed.
        column (str): The name of the column to transform using the mapping.
        mapping (Dict): A dictionary where keys are the original values and values are the mapped values.

    Returns:
        pd.DataFrame: The DataFrame with the transformed column, if successful.

    Raises:
        ValueError: If the specified column is not found in the DataFrame.
        TypeError: If an invalid mapping is provided or the column values cannot be mapped.
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in the DataFrame.")

    try:
        df[column] = df[column].map(mapping)
    except Exception as e:
        raise TypeError(f"Error mapping column '{column}': {e}")

    return df

def get_unique_values(df: pd.DataFrame, columns: List[str]) -> Dict[str, List[Any]]:
    """
    Generates a dictionary where the keys are column names and the values are lists of unique values
    for the specified columns in a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the columns to process.
        columns (List[str]): A list of column names for which to retrieve unique values.

    Returns:
        Dict[str, List[Any]]: A dictionary with column names as keys and lists of unique values as values.

    Raises:
        ValueError: If a specified column is not found in the DataFrame.
    """
    unique_values_dict: Dict[str, List[Any]] = {}
    
    for column in columns:
        if column not in df.columns:
            raise ValueError(f"Column '{column}' not found in the DataFrame.")
        unique_values_dict[column] = df[column].dropna().unique().tolist()
    
    return unique_values_dict

def save_dict_as_json(data: Dict[str, List[Any]], path: str, filename: str) -> None:
    """
    Saves a dictionary as a JSON file in the specified location.

    Args:
        data (Dict[str, List[Any]]): The dictionary to save.
        path (str): The directory where the file will be saved.
        filename (str): The name of the JSON file (including .json extension).

    Returns:
        None

    Raises:
        FileNotFoundError: If the specified path does not exist.
    """
    # Ensure the directory exists
    if not os.path.exists(path):
        raise FileNotFoundError(f"Directory '{path}' does not exist.")

    # Construct the full file path
    file_path = os.path.join(path, filename)
    
    # Save the dictionary as a JSON file
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Dictionary saved to {file_path}")