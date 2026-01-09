import os

# Path
JSON_FILE = "list_pkg.json"
ANALYSIS_DIR = "analysys_results"
CSV_FILENAME = "aggregate_metrics_by_single_version.csv"

OUTPUT_DIR_AGG = "aggregate_outputs_csv"
PLOT_OUTPUT_DIR = "plots"
AVG_PLOTS_DIR = os.path.join(PLOT_OUTPUT_DIR, "numerical_averages")
ALL_PKGS_PLOTS_DIR = os.path.join(PLOT_OUTPUT_DIR, "all_packages")
OUTPUT_DIR_OTH_CSV = "others_csv"
OTH_FILE_DIR_AVG = os.path.join(OUTPUT_DIR_OTH_CSV, "avgs_total_metrics_for_all_pkgs.csv")

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
    "evasion.obfuscation_patterns_count",
    "evasion.platform_detections_count",
    "payload.timing_delays_count",
    "payload.eval_count",
    "payload.shell_commands_count",         # 0 value always
    "exfiltration.scan_functions_count",
    "exfiltration.sensitive_elements_count",
    "exfiltration.data_transmission_count",
    "crypto.crypto_addresses",
    "crypto.cryptocurrency_name",
    "crypto.wallet_detection",              # 0 value always
    "crypto.replaced_crypto_addresses",     # 0 value always
    "crypto.hook_provider"                  # 0 value always
]

OTH_FILE_DIR_PRE = os.path.join(OUTPUT_DIR_OTH_CSV, "presence_total_metrics_for_all_pkgs.csv")
OTH_FILE_DIR_AVG_PRES = os.path.join(OUTPUT_DIR_OTH_CSV, "presence_avg_total_metrics_for_all_pkgs.csv")
PLOTS_PRES_DIR = os.path.join(PLOT_OUTPUT_DIR, "presence")
PLOTS_PRES_AVG_DIR = os.path.join(PLOT_OUTPUT_DIR, "presence_averages")

COLUMNS_PRESENCE = [
    "crypto.crypto_addresses",
    "evasion.obfuscation_patterns_count",
    "evasion.platform_detections_count",
    "payload.timing_delays_count",
    "payload.eval_count",
    #"payload.shell_commands_count",        # 0 value always
    "exfiltration.scan_functions_count",
    "exfiltration.sensitive_elements_count",
    "exfiltration.data_transmission_count",
    "crypto.crypto_addresses",
    "crypto.cryptocurrency_name",
    #"crypto.wallet_detection",             # 0 value always
    #"crypto.replaced_crypto_addresses",    # 0 value always
    #"crypto.hook_provider",                # 0 value always
]

COLUMNS_NUMERIC = [
    "generic.total_files",
    "generic.total_size_bytes", 
    "generic.total_size_chars",
    "generic.weighted_avg_blank_space_and_character_ratio",
    "generic.weighted_avg_shannon_entropy",
    "generic.longest_line_length",
]