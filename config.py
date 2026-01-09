import os

# Path
JSON_FILE = "list_pkg.json"
ANALYSIS_DIR = "analysys_results"
CSV_FILENAME = "aggregate_metrics_by_single_version.csv"
OUTPUT_DIR = "output"
OUTPUT_DIR_AGG = "aggregate_outputs_csv"
AVGS_TOTAL_FILE = "avgs_total_metrics_for_all_pkgs.csv"
AVGS_TOTAL_FILE_DIR = os.path.join(OUTPUT_DIR_AGG, AVGS_TOTAL_FILE)
PLOT_OUTPUT_DIR = "plots"
AVG_PLOTS_DIR = os.path.join(PLOT_OUTPUT_DIR, "averages")
ALL_PKGS_PLOTS_DIR = os.path.join(PLOT_OUTPUT_DIR, "all_packages")

# Plot settings
MAX_VERSIONS = 20
FIGURE_SIZE = (12, 6)
DPI = 100

COLUMNS_TO_EXTRACT = [
    "generic.total_files",
    "generic.total_size_bytes", 
    "generic.total_size_chars",
    "generic.weighted_avg_blank_space_and_character_ratio",
    "generic.weighted_avg_shannon_entropy",
    "generic.longest_line_length",
    #"evasion.code_types",
    "evasion.obfuscation_patterns_count",
    "evasion.platform_detections_count",
    "payload.timing_delays_count",
    "payload.eval_count",
    "payload.shell_commands_count",
    #"payload.preinstall_scripts",
    "exfiltration.scan_functions_count",
    "exfiltration.sensitive_elements_count",
    "exfiltration.data_transmission_count",
    "crypto.crypto_addresses",
    #"crypto.list_crypto_addresses",
    "crypto.cryptocurrency_name",
    "crypto.wallet_detection",
    "crypto.replaced_crypto_addresses",
    "crypto.hook_provider",
    #"account.npm_maintainers",
    #"account.npm_hash_commit",
    #"account.npm_release_date"
]

'''
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
'''