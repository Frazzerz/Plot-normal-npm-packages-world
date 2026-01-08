import json
import os
import pandas as pd
from config import JSON_FILE, ANALYSIS_DIR, CSV_FILENAME, NON_NUMERIC_COLUMNS, MAX_VERSIONS

def load_package_list():
    """Load package list from JSON file"""
    with open(JSON_FILE, 'r') as f:
        return json.load(f)

def load_csv_data(pkg_name: str) -> pd.DataFrame | None:
    """Upload CSV for a single package"""
    
    csv_path = os.path.join(ANALYSIS_DIR, pkg_name, CSV_FILENAME)
    if not os.path.exists(csv_path):
        print(f"File not found for {pkg_name}: {csv_path}")
        return None
    
    try:
        df = pd.read_csv(csv_path, sep=',')
        # Limit to the first MAX_VERSIONS versions
        if len(df) > MAX_VERSIONS:
            df = df.head(MAX_VERSIONS)
        return df
    except Exception as e:
        print(f"Error loading {pkg_name}: {e}")
        return None

def load_all_data(pkg_list: list[str]) -> dict[str, pd.DataFrame]:
    """Load all CSVs for the specified packages"""
    data = {}
    print(f"Loading data for {len(pkg_list)} packages...")
    for pkg in pkg_list:
        df = load_csv_data(pkg)
        if df is not None:
            data[pkg] = df
    print(f"Successfully loaded {len(data)} packages")
    return data

def get_numeric_metrics(df: pd.DataFrame) -> list[str]:
    """Identify the numeric columns to analyze, returns a list of numeric column names"""

    numeric_cols = []
    for col in df.columns:
        if col in NON_NUMERIC_COLUMNS:
            continue
        # Check if the column is numeric
        try:
            if pd.api.types.is_numeric_dtype(df[col]):
                numeric_cols.append(col)
        except:
            # Skip problematic columns
            continue
    
    return numeric_cols

def calculate_averages(data_dict: dict[str, pd.DataFrame], metrics: list[str]) -> pd.DataFrame:
    """Calculate averages for each generic version across all packages, returns a dataFrame with averages per version"""
    
    # Prepare structure for averages
    averages = {f'version_{i+1}': {} for i in range(MAX_VERSIONS)}
    
    for metric in metrics:
        for version_idx in range(MAX_VERSIONS):
            values = []
            
            # Collect values from all packages for this version
            for pkg_name, df in data_dict.items():
                if version_idx < len(df) and metric in df.columns:
                    value = df.iloc[version_idx][metric]
                    # Convert to float, ignoring invalid values
                    try:
                        if value is not None and str(value) != 'nan' and str(value).strip() != '':
                            float_val = float(value)
                            values.append(float_val)
                    except (ValueError, TypeError):
                        # Ignore non-convertible values
                        pass
            
            # Calculate the average
            if values:
                averages[f'version_{version_idx+1}'][metric] = sum(values) / len(values)
            else:
                averages[f'version_{version_idx+1}'][metric] = None
    
    # Convert to DataFrame
    df_avg = pd.DataFrame.from_dict(averages, orient='index')
    df_avg.index.name = 'version'
    return df_avg

def create_metric_csv(data_dict: dict[str, pd.DataFrame], metric: str, output_path: str) -> None:
    """Create a CSV for a single metric with packages as rows and versions as columns"""
    
    metric_data = {}
    for pkg_name, df in data_dict.items():
        pkg_values = []
        
        for version_idx in range(MAX_VERSIONS):
            if version_idx < len(df) and metric in df.columns:
                value = df.iloc[version_idx][metric]
                # Convert to float, setting None for invalid values
                try:
                    if value is not None and str(value) != 'nan' and str(value).strip() != '':
                        pkg_values.append(float(value))
                    else:
                        pkg_values.append(None)
                except (ValueError, TypeError):
                    pkg_values.append(None)
            else:
                pkg_values.append(None)
        
        metric_data[pkg_name] = pkg_values
    
    # Create DataFrame with packages as rows and versions as columns
    df_metric = pd.DataFrame.from_dict(metric_data, orient='index')
    df_metric.columns = [f'version_{i+1}' for i in range(MAX_VERSIONS)]
    df_metric.index.name = 'package'
    
    # Save CSV
    df_metric.to_csv(output_path)