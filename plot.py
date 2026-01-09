import os
import pandas as pd
import matplotlib.pyplot as plt
from config import AVGS_TOTAL_FILE_DIR, OUTPUT_DIR_AGG, COLUMNS_TO_EXTRACT, FIGURE_SIZE, DPI, MAX_VERSIONS, AVG_PLOTS_DIR, ALL_PKGS_PLOTS_DIR

def setup_directories():
    for d in [AVG_PLOTS_DIR, ALL_PKGS_PLOTS_DIR]:
        os.makedirs(d, exist_ok=True)

def plot_averages():
    print(f"Generate average plot from: {AVGS_TOTAL_FILE_DIR}")
    if not os.path.exists(AVGS_TOTAL_FILE_DIR):
        print(f"Error: {AVGS_TOTAL_FILE_DIR} not found.")
        return

    df = pd.read_csv(AVGS_TOTAL_FILE_DIR)
    
    # Generic versions on the x-axis (from 1 to MAX_VERSIONS)
    x_values = list(range(1, MAX_VERSIONS + 1))
    x_labels = [f'V{i}' for i in x_values]
    
    for index, row in df.iterrows():
        metric_name = row['metric']
        
        # Extract values for all versions
        values = []
        for i in range(MAX_VERSIONS):
            version_key = f'version_{i+1}'
            if version_key in df.columns:
                val = row[version_key]
                try:
                    values.append(float(val) if val is not None and str(val) != 'nan' else None)
                except (ValueError, TypeError):
                    values.append(None)
            else:
                values.append(None)
        
        plt.figure(figsize=FIGURE_SIZE, dpi=DPI)
        
        # Plot only if there are valid values
        if any(v is not None for v in values):
            plt.plot(x_values, values, marker='o', linewidth=2, markersize=8, color='#2E86AB', label='Average')
        
        plt.xlabel('Version', fontsize=12)
        plt.ylabel(metric_name, fontsize=12)
        plt.title(f'{metric_name} - Average across all packages', fontsize=14, fontweight='bold')
        plt.xticks(x_values, x_labels, rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        safe_metric_name = metric_name.replace('.', '_').replace('/', '_')
        filename = os.path.join(AVG_PLOTS_DIR, f"avg_{safe_metric_name}.png")
        plt.savefig(filename, dpi=DPI, bbox_inches='tight')
        plt.close()
        #print(f"Saved plot: {filename}")

def plot_all_packages_per_metric():

    print(f"Generate plot for package from: {OUTPUT_DIR_AGG}")
    # Generic versions on the x-axis (from 1 to MAX_VERSIONS)
    x_values = list(range(1, MAX_VERSIONS + 1))
    x_labels = [f'V{i}' for i in x_values]
    
    for col in COLUMNS_TO_EXTRACT:
        filename_csv = col.replace('.', '_') + '.csv'
        filepath = os.path.join(OUTPUT_DIR_AGG, filename_csv)
        
        if not os.path.exists(filepath):
            continue

        df = pd.read_csv(filepath)
        
        plt.figure(figsize=FIGURE_SIZE, dpi=DPI)
        
        # Plot a line for each package
        for index, row in df.iterrows():
            pkg_name = row['package']
            values = []
            for i in range(MAX_VERSIONS):
                version_key = f'version_{i+1}'
                if version_key in df.columns:
                    val = row[version_key]
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
        plt.ylabel(col, fontsize=12)
        plt.title(f'{col} - All Packages', fontsize=14, fontweight='bold')
        plt.xticks(x_values, x_labels, rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        safe_metric_name = col.replace('.', '_').replace('/', '_')
        save_path = os.path.join(ALL_PKGS_PLOTS_DIR, f"all_pkgs_{safe_metric_name}.png")
        plt.savefig(save_path, dpi=DPI, bbox_inches='tight')
        plt.close()
        #print(f"Saved plot: {save_path}")

def main():
    setup_directories()
    plot_averages()
    print("Done.")
    plot_all_packages_per_metric()
    print("Done.")

if __name__ == "__main__":
    main()