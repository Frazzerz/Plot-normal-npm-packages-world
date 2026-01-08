import os

# Path
JSON_FILE = "list_pkg.json"
ANALYSIS_DIR = "analysys_results"
CSV_FILENAME = "aggregate_metrics_by_single_version.csv"
OUTPUT_DIR = "output"
CSV_OUTPUT_DIR = "csv"
AVERAGES_FILE = os.path.join(CSV_OUTPUT_DIR, "avgs_total_metrics_for_all_pkgs.csv")

# Columns to exclude from plotting (non-numeric)
NON_NUMERIC_COLUMNS = [
    'package', 
    'version',
    'evasion.code_types',
    'crypto.list_crypto_addresses',
    'payload.preinstall_scripts',
    'account.npm_maintainers',
    'account.npm_hash_commit',
    'account.npm_release_date'
]

# Plot settings
MAX_VERSIONS = 20
FIGURE_SIZE = (12, 6)
DPI = 100