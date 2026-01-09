import os
import pandas as pd
import matplotlib.pyplot as plt
from config import (
    OTH_FILE_DIR_AVG, 
    OUTPUT_DIR_AGG, 
    COLUMNS_TO_EXTRACT, 
    FIGURE_SIZE, 
    DPI, 
    MAX_VERSIONS, 
    AVG_PLOTS_DIR, 
    ALL_PKGS_PLOTS_DIR,
    PLOT_OUTPUT_DIR,
    OTH_FILE_DIR_PRE,
    PLOTS_PRES_DIR,
    OTH_FILE_DIR_AVG_PRES,
    PLOTS_PRES_AVG_DIR
)

def plot_csv_metrics(csv_path, output_dir, title_suffix=""):
    print(f"Generating plots for {csv_path}")

    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    os.makedirs(output_dir, exist_ok=True)

    df = pd.read_csv(csv_path)

    x_values = list(range(1, MAX_VERSIONS + 1))
    x_labels = [f'V{i}' for i in x_values]

    for _, row in df.iterrows():
        metric_name = row['metric']

        values = []
        for i in range(MAX_VERSIONS):
            col = f'version_{i+1}'
            try:
                values.append(float(row[col]) if col in df.columns else None)
            except (ValueError, TypeError):
                values.append(None)

        if not any(v is not None for v in values):
            continue

        plt.figure(figsize=FIGURE_SIZE, dpi=DPI)
        plt.plot(
            x_values,
            values,
            marker='o',
            linewidth=2,
            markersize=8
        )

        plt.xlabel("Version")
        plt.ylabel(metric_name)
        plt.title(f"{metric_name} {title_suffix}".strip())
        plt.xticks(x_values, x_labels, rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        safe_name = metric_name.replace('.', '_').replace('/', '_')
        out_file = os.path.join(output_dir, f"{safe_name}.png")
        plt.savefig(out_file, dpi=DPI, bbox_inches="tight")
        plt.close()


def plot_all_packages_per_metric():

    print(f"Generate plot for package from: {OUTPUT_DIR_AGG}")
    # Generic versions on the x-axis (from 1 to MAX_VERSIONS)
    os.makedirs(ALL_PKGS_PLOTS_DIR, exist_ok=True)
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
    print(f"Generate all plots in {PLOT_OUTPUT_DIR}")
    plot_csv_metrics(OTH_FILE_DIR_AVG, AVG_PLOTS_DIR, title_suffix="- Average across all 496 packages")
    print("Done.")
    plot_csv_metrics(OTH_FILE_DIR_PRE, PLOTS_PRES_DIR, title_suffix="- Presence across all 496 packages")
    print("Done.")
    plot_csv_metrics(OTH_FILE_DIR_AVG_PRES, PLOTS_PRES_AVG_DIR, title_suffix="- Average presence across the non-0 packages")
    print("Done.")
    plot_all_packages_per_metric()
    print("Done.")

if __name__ == "__main__":
    main()