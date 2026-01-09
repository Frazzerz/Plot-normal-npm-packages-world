import json
from config import JSON_FILE, ANALYSIS_DIR, CSV_FILENAME, COLUMNS_TO_EXTRACT, OUTPUT_DIR_AGG, AVGS_TOTAL_FILE_DIR
import pandas as pd
import os
import csv

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
    
    for col in COLUMNS_TO_EXTRACT:
        if col in df.columns:
            values = []
            values_temp = []
            for val in df[col].tolist():
                if pd.isna(val) or val is None or val == '':
                    values_temp.append(0)
                else:
                    values_temp.append(val)
            
            if len(values_temp) == 20:
                values = values_temp
            else:
                #print(f"pkg_name {pkg_name}, col {col}, values_temp {values_temp}")
                continue

            row = [pkg_name] + values
            filename = col.replace('.', '_') + '.csv'
            filepath = os.path.join(OUTPUT_DIR_AGG, filename)
            with open(filepath, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(row)

# ------
def init_avgs_total(output_path):
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
def main():

    print("Loading package list...")
    pkg_list = load_package_list()
    print(f"   Found {len(pkg_list)} packages in JSON")

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
    print("Done.")

    init_avgs_total(AVGS_TOTAL_FILE_DIR)
    
    for col in COLUMNS_TO_EXTRACT:
        filename = col.replace('.', '_') + '.csv'
        filepath = os.path.join(OUTPUT_DIR_AGG, filename)

        if os.path.exists(filepath):
            #print(f"col:{col}")
            append_metric_to_avgs_total(filepath, AVGS_TOTAL_FILE_DIR)
    print(f"{AVGS_TOTAL_FILE_DIR} created successfully.")

if __name__ == "__main__":
    main()