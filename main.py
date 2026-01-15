import json
from config import (
    JSON_FILE, 
    ANALYSIS_DIR, 
    CSV_FILENAME, 
    COLUMNS_TO_EXTRACT, 
    OUTPUT_DIR_AGG, 
    COLUMNS_PRESENCE, 
    OUTPUT_DIR_OTH_CSV, 
    OTH_FILE_DIR_AVG,
    OTH_FILE_DIR_PRE,
    OTH_FILE_DIR_AVG_PRES,
    PLOT_OUTPUT_DIR,
    COLUMNS_NUMERIC,
    OUTPUT_DIR_AGG_NO_OUT
)
import pandas as pd
import os
import csv
import shutil
from pathlib import Path
from packaging.version import parse as parse_version
from packaging.version import InvalidVersion

def delete_dir():
    dirs_to_delete = [OUTPUT_DIR_AGG, OUTPUT_DIR_OTH_CSV, PLOT_OUTPUT_DIR, OUTPUT_DIR_AGG_NO_OUT]
    for dir_name in dirs_to_delete:
        dir_path = Path(dir_name)
        if dir_path.exists() and dir_path.is_dir():
            shutil.rmtree(dir_path)

def load_package_list():
    """Load package list from JSON file"""
    with open(JSON_FILE, 'r') as f:
        return json.load(f)

def load_csv_data(pkg_name: str) -> pd.DataFrame | None:
    """Upload CSV for a single package"""
    csv_path = os.path.join(ANALYSIS_DIR, pkg_name, CSV_FILENAME)
    if not os.path.exists(csv_path):
        #print(f"File not found for {pkg_name}: {csv_path}")
        return None
    try:
        df = pd.read_csv(csv_path, sep=',')
        return df
    except Exception as e:
        #print(f"Error loading {pkg_name}: {e}")
        return None

def append_package_to_column_files(pkg_name, df):
    try:
        df = df.sort_values(by="version", key=lambda s: s.map(parse_version))
    except InvalidVersion:
        #print(f"Skip pkg {pkg_name}: colonne non valide come versioni")
        return   # skip the whole package
    except KeyError:
        #print(f"Skip pkg {pkg_name}: manca la colonna version")
        return
    except Exception as e:
        #print(f"Error sorting versions for {pkg_name}: {e}")
        return
    for col in COLUMNS_TO_EXTRACT:
        if col in df.columns and len(df[col]) == 20:
            values = (
                df[col]
                .fillna(0)
                .replace('', 0)
                .tolist()
            )
            row = [pkg_name] + values
            filepath = os.path.join(OUTPUT_DIR_AGG, col.replace('.', '_') + '.csv')
            with open(filepath, 'a', newline='') as f:
                csv.writer(f).writerow(row)

# ------
def save_no_outliers_version(metric_csv_path, output_dir):
    df = pd.read_csv(metric_csv_path)
    version_cols = [c for c in df.columns if c.startswith("version_")]

    df_versions = df[version_cols]

    Q1 = df_versions.quantile(0.25)
    Q3 = df_versions.quantile(0.75)
    IQR = Q3 - Q1

    low = Q1 - 1.5 * IQR
    high = Q3 + 1.5 * IQR

    mask_ok = (df_versions >= low) & (df_versions <= high)
    rows_ok = mask_ok.all(axis=1)

    df_clean = df[rows_ok]   # tieni anche la colonna package

    return df_clean

# ------
def init_total(output_path):
    columns = ["metric"] + [f"version_{i}" for i in range(1, 21)]
    df = pd.DataFrame(columns=columns)
    df.to_csv(output_path, index=False)

def append_metric_to_avgs_total(metric_csv_path, avgs_total_path):
    metric_name = os.path.basename(metric_csv_path).replace(".csv", "")
    df = pd.read_csv(metric_csv_path)

    # take only version_X
    version_cols = [c for c in df.columns if c.startswith("version_")]
    avgs = df[version_cols].mean().tolist()

    row = [metric_name] + avgs
    df_out = pd.DataFrame([row], columns=["metric"] + version_cols)
    df_out.to_csv(avgs_total_path, mode="a", header=False, index=False)

# ------
def append_metric_to_pres_and_avgs_total(metric_csv_path, prese_path, avgs_pres_path):
    metric_name = os.path.basename(metric_csv_path).replace(".csv", "")
    df = pd.read_csv(metric_csv_path)
    # take only version_X
    version_cols = [c for c in df.columns if c.startswith("version_")]

    counts_greater_than_zero = (df[version_cols] > 0).sum().tolist()
    #counts_zero = (df[version_cols] == 0).sum().tolist()
    #print(f"counts_zero for each versions for {metric_name}: {counts_zero}")
    avgs_greater_than_zero = (df[version_cols].where(df[version_cols] > 0).mean().tolist())

    row_pre = [metric_name] + counts_greater_than_zero
    df_out = pd.DataFrame([row_pre], columns=["metric"] + version_cols)
    df_out.to_csv(prese_path, mode="a", header=False, index=False)

    row_pre_avg = [metric_name] + avgs_greater_than_zero
    df_out = pd.DataFrame([row_pre_avg], columns=["metric"] + version_cols)
    df_out.to_csv(avgs_pres_path, mode="a", header=False, index=False)

# ------

def main():
    delete_dir()
    print("Loading package list...")
    pkg_list = load_package_list()
    print(f"Found {len(pkg_list)} packages in JSON")

    os.makedirs(OUTPUT_DIR_AGG, exist_ok=True)
    
    for col in COLUMNS_TO_EXTRACT:
        filename = col.replace('.', '_') + '.csv'
        filepath = os.path.join(OUTPUT_DIR_AGG, filename)
        
        columns = ["package"] + [f"version_{i}" for i in range(1, 21)]
        df_header = pd.DataFrame(columns=columns)
        df_header.to_csv(filepath, index=False)
    
    for pkg in pkg_list:
        df = load_csv_data(pkg)
        if df is not None:
            append_package_to_column_files(pkg, df)
    print("Data aggregation completed.")

    os.makedirs(OUTPUT_DIR_AGG_NO_OUT, exist_ok=True)
    for col in COLUMNS_NUMERIC:
        filename = col.replace('.', '_') + '.csv'
        filepath = os.path.join(OUTPUT_DIR_AGG, filename)
        if os.path.exists(filepath):
            df_clean = save_no_outliers_version(filepath, OUTPUT_DIR_AGG_NO_OUT)
            out_path = os.path.join(OUTPUT_DIR_AGG_NO_OUT, filename)
            df_clean.to_csv(out_path, index=False)
    print(f"Aggregate CSV files created in {OUTPUT_DIR_AGG} and {OUTPUT_DIR_AGG_NO_OUT}.")

    os.makedirs(OUTPUT_DIR_OTH_CSV, exist_ok=True)
    init_total(OTH_FILE_DIR_AVG)
    
    for col in COLUMNS_NUMERIC:
        filename = col.replace('.', '_') + '.csv'
        filepath = os.path.join(OUTPUT_DIR_AGG_NO_OUT, filename)
        if os.path.exists(filepath):
            append_metric_to_avgs_total(filepath, OTH_FILE_DIR_AVG)
    print(f"{OTH_FILE_DIR_AVG} created successfully.")

    init_total(OTH_FILE_DIR_PRE)
    init_total(OTH_FILE_DIR_AVG_PRES)
    
    for col in COLUMNS_PRESENCE:
        filename = col.replace('.', '_') + '.csv'
        filepath = os.path.join(OUTPUT_DIR_AGG, filename)
        if os.path.exists(filepath):
            append_metric_to_pres_and_avgs_total(filepath, OTH_FILE_DIR_PRE, OTH_FILE_DIR_AVG_PRES)
    print(f"{OTH_FILE_DIR_PRE} and {OTH_FILE_DIR_AVG_PRES} created successfully.")

if __name__ == "__main__":
    main()