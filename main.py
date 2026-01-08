import os
import matplotlib.pyplot as plt
import pandas as pd
from data_processor import load_package_list, load_all_data, get_numeric_metrics, calculate_averages, create_metric_csv
from config import OUTPUT_DIR, CSV_OUTPUT_DIR, AVERAGES_FILE, FIGURE_SIZE, DPI, MAX_VERSIONS

def check_existing_plots(metrics: list[str], output_dir: str) -> list[str]:
    """Check which metrics already have plots generated"""
    existing_plots = []
    
    for metric in metrics:
        safe_metric_name = metric.replace('.', '_').replace('/', '_')
        all_packages_file = os.path.join(output_dir, f"{safe_metric_name}_all_packages.png")
        average_file = os.path.join(output_dir, f"{safe_metric_name}_average.png")
        
        if os.path.exists(all_packages_file) and os.path.exists(average_file):
            existing_plots.append(metric)
    
    return existing_plots

def check_existing_csvs(metrics: list[str], csv_dir: str) -> list[str]:
    """Check which metrics already have CSV files generated"""
    existing_csvs = []
    
    for metric in metrics:
        safe_metric_name = metric.replace('.', '_').replace('/', '_')
        csv_file = os.path.join(csv_dir, f"{safe_metric_name}.csv")
        
        if os.path.exists(csv_file):
            existing_csvs.append(metric)
    
    return existing_csvs
def plot_metric_all_packages(data_dict: dict, metric: str, output_dir: str) -> None:
    """Create a graph with a line for each package"""

    plt.figure(figsize=FIGURE_SIZE)
    # Generic versions on the x-axis (from 1 to MAX_VERSIONS)
    x_values = list(range(1, MAX_VERSIONS + 1))
    x_labels = [f'V{i}' for i in x_values]
    
    # Plot a line for each package
    for pkg_name, df in data_dict.items():
        values = []
        for idx in range(MAX_VERSIONS):
            if idx < len(df) and metric in df.columns:
                val = df.iloc[idx][metric]
                # Convert to float, handling null values
                try:
                    values.append(float(val) if val is not None and str(val) != 'nan' else None)
                except (ValueError, TypeError):
                    values.append(None)
            else:
                values.append(None)
        
        # Plot only if there are valid values
        if any(v is not None for v in values):
            plt.plot(x_values, values, marker='o', label=pkg_name, alpha=0.7, linewidth=2)
    
    plt.xlabel('Version', fontsize=12)
    plt.ylabel(metric, fontsize=12)
    plt.title(f'{metric} - All Packages', fontsize=14, fontweight='bold')
    plt.xticks(x_values, x_labels, rotation=45)
    # plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save the plot
    safe_metric_name = metric.replace('.', '_').replace('/', '_')
    filename = f"{safe_metric_name}_all_packages.png"
    plt.savefig(os.path.join(output_dir, filename), dpi=DPI, bbox_inches='tight')
    plt.close()

def plot_metric_average(df_averages: pd.DataFrame, metric: str, output_dir: str) -> None:
    """Create a graph with the average per version"""
    
    plt.figure(figsize=FIGURE_SIZE)
    
    # Generic versions on the x-axis (from 1 to MAX_VERSIONS)
    x_values = list(range(1, MAX_VERSIONS + 1))
    x_labels = [f'V{i}' for i in x_values]
    
    # Extract metric values
    values = []
    for i in range(MAX_VERSIONS):
        version_key = f'version_{i+1}'
        if version_key in df_averages.index and metric in df_averages.columns:
            val = df_averages.loc[version_key, metric]
            try:
                values.append(float(val) if val is not None and str(val) != 'nan' else None)
            except (ValueError, TypeError):
                values.append(None)
        else:
            values.append(None)
    
    # Plot only if there are valid values
    if any(v is not None for v in values):
        plt.plot(x_values, values, marker='o', linewidth=2, 
                 markersize=8, color='#2E86AB', label='Average')
    
    plt.xlabel('Version', fontsize=12)
    plt.ylabel(metric, fontsize=12)
    plt.title(f'{metric} - Average across all packages', fontsize=14, fontweight='bold')
    plt.xticks(x_values, x_labels, rotation=45)
    plt.grid(True, alpha=0.3)
    # plt.legend(fontsize=10)
    plt.tight_layout()
    
    # Salva il grafico
    safe_metric_name = metric.replace('.', '_').replace('/', '_')
    filename = f"{safe_metric_name}_average.png"
    plt.savefig(os.path.join(output_dir, filename), dpi=DPI, bbox_inches='tight')
    plt.close()

def main():
    print("Package plotting started...")
    
    # Create output directories if they don't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(CSV_OUTPUT_DIR, exist_ok=True)
    
    print("Loading package list...")
    pkg_list = load_package_list()
    print(f"   Found {len(pkg_list)} packages in JSON")
    
    # Load all data
    data_dict = load_all_data(pkg_list)
    if not data_dict:
        print("No data loaded. Check the paths.")
        return
    
    # Identify numeric metrics
    first_df = next(iter(data_dict.values()))
    # print(f"Columns found: {list(first_df.columns)[:10]}")
    metrics = get_numeric_metrics(first_df)
    print(f"Found {len(metrics)} numeric metrics to analyze")

    if len(metrics) == 0:
        print("No numerical metrics found.")
        return
    
    #print(f"First 5 metrics: {metrics[:5]}")
    #test_metric = metrics[0]
    #print(f"First 3 values of '{test_metric}':")
    #for pkg_name, df in list(data_dict.items())[:1]:
        #print(f"   {pkg_name}: {list(df[test_metric].head(3))}")
    
    # Check if averages file already exists
    if os.path.exists(AVERAGES_FILE):
        print(f"Loading existing averages file: {AVERAGES_FILE}")
        df_averages = pd.read_csv(AVERAGES_FILE, index_col=0)
        print("Averages loaded from existing file.")
    else:
        print("Calculating averages for all packages...")
        df_averages = calculate_averages(data_dict, metrics)
        df_averages.to_csv(AVERAGES_FILE)
        print("Total averages saved successfully.")
    
    # Check which CSVs already exist
    existing_csvs = check_existing_csvs(metrics, CSV_OUTPUT_DIR)
    csv_to_create = [m for m in metrics if m not in existing_csvs]
    
    if csv_to_create:
        print(f"Creating CSV for {len(csv_to_create)} metrics...")
        for i, metric in enumerate(csv_to_create, 1):
            safe_metric_name = metric.replace('.', '_').replace('/', '_')
            csv_filename = f"{safe_metric_name}.csv"
            csv_path = os.path.join(CSV_OUTPUT_DIR, csv_filename)
            create_metric_csv(data_dict, metric, csv_path)
            print(f"   [{i}/{len(csv_to_create)}] Created: {metric}")
    else:
        print(f"All {len(metrics)} CSV files already exist, skipping creation.")
    
    # Check which plots already exist
    existing_plots = check_existing_plots(metrics, OUTPUT_DIR)
    plots_to_create = [m for m in metrics if m not in existing_plots]
    
    if plots_to_create:
        print(f"Generating plots for {len(plots_to_create)} metrics...")
        for i, metric in enumerate(plots_to_create, 1):
            print(f"   [{i}/{len(plots_to_create)}] Processing: {metric}")
            # Plot with all packages
            plot_metric_all_packages(data_dict, metric, OUTPUT_DIR)        
            # Plot with average
            plot_metric_average(df_averages, metric, OUTPUT_DIR)
    else:
        print(f"All {len(metrics)} plots already exist, skipping creation.")
    print("Analysis and plotting completed successfully.")

if __name__ == "__main__":
    main()