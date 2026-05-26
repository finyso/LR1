"""
Lab 4, Task 6, Variant 24
Pandas data analysis for Supermarket Sales dataset.
Dataset: https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales
Developer: Finsky Pavel
Date: 01.05.2026
Version: 1.0
"""
import pandas as pd
import numpy as np
import os


def load_supermarket_data():
    """
    Load supermarket sales data from CSV file.
    Searches for the file in multiple possible locations.
    
    Returns:
        pd.DataFrame: Loaded supermarket sales data
    """
    # Possible file locations (searches in order)
    possible_paths = [
        "SuperMarket Analysis.csv",                          # Same directory as main.py
        "SuperMarket Analysis.csv.zip",                      # Zipped version
        os.path.join("..", "SuperMarket Analysis.csv"),      # Parent directory
        os.path.join(os.path.dirname(__file__), "..", "..", "SuperMarket Analysis.csv"),  # Project root
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Loading data from: {path}")
            df = pd.read_csv(path)
            print(f"Successfully loaded {len(df)} rows and {len(df.columns)} columns.")
            return df
    
    # If file not found, show error and instructions
    print("=" * 60)
    print("ERROR: Supermarket sales CSV file not found!")
    print("=" * 60)
    print("\nPlease download the dataset from Kaggle:")
    print("  https://www.kaggle.com/datasets/aungpyaeap/supermarket-sales")
    print("\nPlace the file 'SuperMarket Analysis.csv' in the project root folder:")
    print(f"  {os.path.abspath('.')}")
    print("\nThen run the program again.")
    print("=" * 60)
    
    # Ask user for manual path
    manual_path = input("\nOr enter the full path to the CSV file (press Enter to skip): ").strip()
    if manual_path and os.path.exists(manual_path):
        print(f"Loading data from: {manual_path}")
        df = pd.read_csv(manual_path)
        print(f"Successfully loaded {len(df)} rows and {len(df.columns)} columns.")
        return df
    
    raise FileNotFoundError(
        "Supermarket sales CSV file not found. "
        "Please download it from Kaggle and place in project root."
    )


def display_dataframe_info(df):
    """
    Displays comprehensive information about the DataFrame.
    Covers requirements: getting info about each parameter.
    
    Args:
        df (pd.DataFrame): The dataframe to analyze
    """
    print("\n" + "=" * 60)
    print("DATAFRAME INFORMATION")
    print("=" * 60)
    
    print(f"\n1. Shape (rows, columns): {df.shape}")
    
    print(f"\n2. Column names:")
    for i, col in enumerate(df.columns, 1):
        print(f"   {i}. {col}")
    
    print(f"\n3. Data types:")
    print(df.dtypes)
    
    print(f"\n4. First 5 rows:")
    print(df.head())
    
    print(f"\n5. Last 5 rows:")
    print(df.tail())
    
    print(f"\n6. Basic statistics (numeric columns):")
    print(df.describe())
    
    print(f"\n7. Basic statistics (all columns including text):")
    print(df.describe(include='all'))
    
    print(f"\n8. Missing values per column:")
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100
    missing_df = pd.DataFrame({
        'Missing Count': missing,
        'Missing %': missing_pct.round(2)
    })
    print(missing_df[missing_df['Missing Count'] > 0] if missing_df['Missing Count'].sum() > 0 else "No missing values")
    
    print(f"\n9. Memory usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")
    
    print(f"\n10. Unique values per column:")
    for col in df.columns:
        n_unique = df[col].nunique()
        print(f"    {col}: {n_unique} unique values")


def task_a_categorical_series(df):
    """
    TASK A: Library Pandas. Structures Series and DataFrame.
    
    Specific task: From column 'Product line' create a categorical Series
    with category order. Convert to codes and create a new DataFrame
    with these codes and names.
    
    Key operations: Categorical data with specified order.
    
    Args:
        df (pd.DataFrame): Supermarket sales dataframe
        
    Returns:
        pd.DataFrame: New dataframe with product codes and names
    """
    print("\n" + "=" * 60)
    print("TASK A: Categorical Series from 'Product line'")
    print("=" * 60)
    
    # 1. Check if 'Product line' column exists (Kaggle dataset uses this exact name)
    product_column = None
    for col in df.columns:
        if 'product' in col.lower() and 'line' in col.lower():
            product_column = col
            break
    
    if product_column is None:
        # Try common alternative names
        for col in df.columns:
            if 'product' in col.lower():
                product_column = col
                break
    
    if product_column is None:
        raise ValueError("Column 'Product line' not found in dataset. Available columns: " + str(df.columns.tolist()))
    
    print(f"\nUsing column: '{product_column}'")
    print(f"Sample values: {df[product_column].head(5).tolist()}")
    
    # 2. Get unique product lines and define order
    unique_products = df[product_column].unique().tolist()
    print(f"\nUnique product lines found: {len(unique_products)}")
    for i, product in enumerate(unique_products):
        print(f"  {i + 1}. {product}")
    
    # 3. Create categorical Series with specified order
    print(f"\nCreating categorical Series with {len(unique_products)} categories (ordered)...")
    product_cat_series = pd.Categorical(
        df[product_column],
        categories=unique_products,
        ordered=True
    )
    
    print(f"Type: {type(product_cat_series)}")
    print(f"Categories: {product_cat_series.categories.tolist()}")
    print(f"Ordered: {product_cat_series.ordered}")
    
    # 4. Display first 10 values using both .iloc and .loc
    print(f"\nFirst 10 values (using .iloc):")
    product_s = pd.Series(product_cat_series, name="product_line")
    print(product_s.iloc[:10])
    
    # 5. Convert to codes
    print(f"\nConverting categories to numeric codes (.codes):")
    product_codes = product_cat_series.codes
    print(f"First 20 codes: {product_codes[:20]}")
    print(f"Unique codes: {sorted(set(product_codes))}")
    print(f"Code mapping:")
    for code, category in enumerate(product_cat_series.categories):
        print(f"  Code {code} -> '{category}'")
    
    # 6. Create new DataFrame with codes and names
    print(f"\nCreating new DataFrame with product codes and names:")
    df_products = pd.DataFrame({
        "product_code": product_codes,
        "product_name": df[product_column].values
    })
    
    print(f"New DataFrame shape: {df_products.shape}")
    print(f"Columns: {df_products.columns.tolist()}")
    print(f"\nFirst 10 rows:")
    print(df_products.head(10))
    
    # 7. Value counts by product code
    print(f"\nValue counts by product code:")
    code_counts = df_products["product_code"].value_counts().sort_index()
    for code, count in code_counts.items():
        product_name = unique_products[code]
        pct = (count / len(df_products)) * 100
        print(f"  Code {code}: {product_name} - {count} items ({pct:.1f}%)")
    
    # 8. Demonstrate .loc access with indices
    print(f"\nDemonstrating .loc access on Series with custom index:")
    product_s_indexed = pd.Series(
        product_cat_series,
        index=[f"P{i:04d}" for i in range(len(product_cat_series))]
    )
    print(f"  .loc['P0000']: {product_s_indexed.loc['P0000']}")
    print(f"  .loc['P0000':'P0004']:")
    print(product_s_indexed.loc['P0000':'P0004'])
    print(f"  .iloc[3]: {product_s_indexed.iloc[3]}")
    print(f"  .iloc[5:8]:")
    print(product_s_indexed.iloc[5:8])
    
    return df_products

def task_b_hourly_analysis(df):
    """
    TASK B: Statistical analysis.
    
    Task: Determine how many times the average check amount (Total/Sales)
    in the busiest hour is greater than in the slowest hour.
    Round the answer to hundredths.
    
    Uses indexing and data extraction with statistical methods:
    mean(), max(), min(), idxmax(), idxmin()
    
    Args:
        df (pd.DataFrame): Supermarket sales dataframe
        
    Returns:
        float: Ratio of busiest hour average to slowest hour average
    """
    print("\n" + "=" * 60)
    print("TASK B: Hourly Revenue Analysis")
    print("Determine how many times the average check (Total/Sales)")
    print("in the busiest hour is greater than in the slowest hour.")
    print("=" * 60)
    
    # 1. Find the time column and total/sales column
    time_column = None
    total_column = None
    
    # Look for Total or Sales column (dataset uses 'Sales')
    for col in df.columns:
        if col.lower() == 'time':
            time_column = col
        if col.lower() in ['total', 'sales']:
            total_column = col
    
    if time_column is None:
        raise ValueError("Column 'Time' not found in dataset. Available columns: " + str(df.columns.tolist()))
    if total_column is None:
        raise ValueError("Column 'Total' or 'Sales' not found in dataset. Available columns: " + str(df.columns.tolist()))
    
    print(f"\nUsing columns: '{time_column}' and '{total_column}'")
    
    # 2. Extract hour from Time column
    print(f"\nExtracting hour from '{time_column}' column...")
    
    # Try different time formats
    try:
        df["Hour"] = pd.to_datetime(df[time_column], format="%H:%M").dt.hour
    except:
        try:
            df["Hour"] = pd.to_datetime(df[time_column]).dt.hour
        except:
            # If time is already numeric or in different format
            df["Hour"] = df[time_column].astype(str).str[:2].astype(int)
    
    print(f"Unique hours found: {sorted(df['Hour'].unique())}")
    print(f"Hour value counts:")
    hour_counts = df["Hour"].value_counts().sort_index()
    for hour, count in hour_counts.items():
        print(f"  Hour {hour:02d}:00 - {count} transactions")
    
    # 3. Calculate average Total/Sales per hour
    print(f"\nCalculating average '{total_column}' per hour...")
    hourly_avg = df.groupby("Hour")[total_column].mean()
    hourly_count = df.groupby("Hour")[total_column].count()
    hourly_sum = df.groupby("Hour")[total_column].sum()
    
    print(f"\nHourly statistics:")
    print(f"{'Hour':<10} {'Count':<10} {'Sum':<15} {'Avg':<15}")
    print("-" * 50)
    for hour in sorted(hourly_avg.index):
        print(f"{hour:02d}:00{'':<5} {hourly_count[hour]:<10} {hourly_sum[hour]:<15.2f} {hourly_avg[hour]:<15.2f}")
    
    # 4. Find busiest and slowest hours (by average Total/Sales)
    print(f"\nFinding busiest and slowest hours (by average '{total_column}')...")
    busiest_hour = hourly_avg.idxmax()
    slowest_hour = hourly_avg.idxmin()
    avg_busy = hourly_avg.max()
    avg_slow = hourly_avg.min()
    
    print(f"\nBusiest hour: {busiest_hour:02d}:00")
    print(f"  Number of transactions: {hourly_count[busiest_hour]}")
    print(f"  Total sales: {hourly_sum[busiest_hour]:.2f}")
    print(f"  Average check: {avg_busy:.2f}")
    
    print(f"\nSlowest hour: {slowest_hour:02d}:00")
    print(f"  Number of transactions: {hourly_count[slowest_hour]}")
    print(f"  Total sales: {hourly_sum[slowest_hour]:.2f}")
    print(f"  Average check: {avg_slow:.2f}")
    
    # 5. Calculate ratio
    print(f"\nCalculating ratio...")
    if avg_slow > 0:
        ratio = avg_busy / avg_slow
        print(f"\n{'=' * 60}")
        print(f"RESULT:")
        print(f"  Average check in busiest hour ({busiest_hour:02d}:00): {avg_busy:.2f}")
        print(f"  Average check in slowest hour ({slowest_hour:02d}:00): {avg_slow:.2f}")
        print(f"  Ratio: {avg_busy:.2f} / {avg_slow:.2f} = {ratio:.2f}")
        print(f"{'=' * 60}")
        print(f"\nANSWER: The average check amount in the busiest hour")
        print(f"is {ratio:.2f} times greater than in the slowest hour.")
    else:
        print("Cannot calculate ratio: slowest hour has zero average.")
        ratio = float('inf')
    
    # 6. Ranking of all hours
    print(f"\nComplete ranking of hours by average '{total_column}':")
    ranked_hours = hourly_avg.sort_values(ascending=False)
    for rank, (hour, avg) in enumerate(ranked_hours.items(), 1):
        marker = ""
        if hour == busiest_hour:
            marker = " <-- BUSIEST"
        elif hour == slowest_hour:
            marker = " <-- SLOWEST"
        print(f"  Rank {rank:2d}: Hour {hour:02d}:00 - Avg: {avg:.2f}{marker}")
    
    return round(ratio, 2)


def run_full_analysis():
    """
    Runs the complete analysis for Task 6.
    Demonstrates all required operations.
    
    Returns:
        tuple: (df, df_products, ratio)
    """
    # Load data
    df = load_supermarket_data()
    
    # Display initial info
    print("\n" + "=" * 60)
    print("SUPERMARKET SALES DATA ANALYSIS")
    print("Dataset: Supermarket Sales from Kaggle")
    print("=" * 60)
    
    # Display DataFrame information
    display_dataframe_info(df)
    
    # Task A: Categorical Series
    df_products = task_a_categorical_series(df)
    
    # Task B: Hourly analysis
    ratio = task_b_hourly_analysis(df)
    
    # Summary
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    
    return df, df_products, ratio