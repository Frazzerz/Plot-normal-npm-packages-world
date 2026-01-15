import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import shutil
from pathlib import Path
from config import (
    OTH_FILE_DIR_AVG, 
    OUTPUT_DIR_AGG, 
    COLUMNS_TO_EXTRACT, 
    FIGURE_SIZE, 
    DPI, 
    MAX_VERSIONS, 
    AVG_PLOTS_DIR, 
    HTML_PLOTS_DIR,
    OTH_FILE_DIR_PRE,
    PLOTS_PRES_DIR,
    OTH_FILE_DIR_AVG_PRES,
    PLOTS_PRES_AVG_DIR,
    PLOT_OUTPUT_DIR,
    COLUMNS_NUMERIC,
    OUTPUT_DIR_AGG_NO_OUT
)

def delete_dir():
    dirs_to_delete = [PLOT_OUTPUT_DIR]
    for dir_name in dirs_to_delete:
        dir_path = Path(dir_name)
        if dir_path.exists() and dir_path.is_dir():
            shutil.rmtree(dir_path)

def plot_csv_metrics(csv_path, output_dir, part, title=""):
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

        # for better visualization
        only_metric_name = (metric_name.split("_", 1)[1]).replace("_", " ")
        parts = metric_name.split("_")
        parts[0] = part
        title_metric_name = " ".join(parts)

        plt.xlabel("Version")
        plt.ylabel(title_metric_name)
        plt.title(f"{title} - {only_metric_name}")
        plt.xticks(x_values, x_labels, rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        file_name = "_".join(parts)
        out_file = os.path.join(output_dir, f"{file_name}.png")
        plt.savefig(out_file, dpi=DPI, bbox_inches="tight")
        plt.close()
    print(f"Plots saved in {output_dir}")


def plot_interactive_all_packages(dir, output_dir):
    print(f"Generating interactive plots for all packages in {dir}...")
    os.makedirs(os.path.join(HTML_PLOTS_DIR, output_dir), exist_ok=True)

    x = list(range(1, MAX_VERSIONS + 1))

    for col in COLUMNS_TO_EXTRACT:
        filepath = os.path.join(dir, col.replace('.', '_') + '.csv')
        #filepath = os.path.join(OUTPUT_DIR_AGG, col.replace('.', '_') + '.csv')
        #filepath = os.path.join(OUTPUT_DIR_AGG_NO_OUT, col.replace('.', '_') + '.csv')
        if not os.path.exists(filepath):
            continue

        df = pd.read_csv(filepath)
        df['package'] = df['package'].fillna('').astype(str)
        fig = go.Figure()

        for i, row in df.iterrows():
            pkg = row['package'].strip() or f"pkg_{i+1}"

            values = [
                float(row[f"version_{j+1}"]) if f"version_{j+1}" in df.columns and str(row[f"version_{j+1}"]) != 'nan' else None
                for j in range(MAX_VERSIONS)
            ]

            if any(v is not None for v in values):
                fig.add_trace(go.Scatter(
                    x=x,
                    y=values,
                    mode='lines+markers',
                    text=[pkg] * MAX_VERSIONS,
                    hovertemplate='Package: %{text}<br>Version: %{x}<br>Value: %{y}<extra></extra>'
                ))

        metric = col.split(".", 1)[1].replace("_", " ")
        fig.update_layout(
            title=f"All Packages - {metric}",
            xaxis_title="Version",
            yaxis_title=metric,
            showlegend=False
        )

        out = os.path.join(HTML_PLOTS_DIR, output_dir, f"{col.replace('.', '_')}_all_packages.html")
        fig.write_html(out)
    print("Interactive plots generation completed.")


def plot_boxplot_metric(metric_csv_path, output_dir):
    df = pd.read_csv(metric_csv_path)
    version_cols = [c for c in df.columns if c.startswith("version_")]

    data = [df[c].dropna().values for c in version_cols]

    plt.figure(figsize=(14, 6))
    plt.boxplot(
        data,
        tick_labels=[f"V{i+1}" for i in range(len(version_cols))],
        showfliers=True
    )
    plt.xticks(rotation=45)
    plt.title(os.path.basename(metric_csv_path).replace(".csv", ""))
    plt.xlabel("Version")
    plt.ylabel("Value")
    plt.tight_layout()

    out = os.path.join(output_dir, os.path.basename(metric_csv_path).replace(".csv", "_box.png"))
    plt.savefig(out, dpi=300)
    plt.close()


def main():
    delete_dir()
    plot_csv_metrics(OTH_FILE_DIR_AVG, AVG_PLOTS_DIR, "avg", title="avg value across all 495 packages")
    plot_csv_metrics(OTH_FILE_DIR_PRE, PLOTS_PRES_DIR, "number of", title="number of package that have at least one occurrence across all 495 packages")
    plot_csv_metrics(OTH_FILE_DIR_AVG_PRES, PLOTS_PRES_AVG_DIR, "avg", title="avg value for the number of package that have at least one occurrence")
    plot_interactive_all_packages(OUTPUT_DIR_AGG, Path("all_packages"))
    plot_interactive_all_packages(OUTPUT_DIR_AGG_NO_OUT, Path("all_packages_no_outliers"))


    BOX_DIR = os.path.join(PLOT_OUTPUT_DIR, "boxplots")
    os.makedirs(BOX_DIR, exist_ok=True)
    print("Generating boxplots for each metric...")
    for col in COLUMNS_NUMERIC:  #COLUMNS_TO_EXTRACT:
        filepath = os.path.join(OUTPUT_DIR_AGG, col.replace('.', '_') + '.csv')
        if os.path.exists(filepath):
            plot_boxplot_metric(filepath, BOX_DIR)
    print(f"Boxplots saved in {BOX_DIR}")
    

if __name__ == "__main__":
    main()