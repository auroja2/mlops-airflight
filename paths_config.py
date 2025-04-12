import os

# Use absolute paths to avoid working directory issues
PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Define directories
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
CONFIG_DIR = os.path.join(PROJECT_ROOT, "config")  # Added config directory
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
INGESTED_DATA_DIR = os.path.join(DATA_DIR, "ingested")
PROCESSED_DIR = os.path.join(DATA_DIR, "processed")
ENGINEERED_DIR = os.path.join(DATA_DIR, "engineered_data")

# Define specific file paths
RAW_DATA_PATH = os.path.join(RAW_DATA_DIR, "raw_data.csv")
TRAIN_DATA_PATH = os.path.join(INGESTED_DATA_DIR, "train.csv")
TEST_DATA_PATH = os.path.join(INGESTED_DATA_DIR, "test.csv")
PROCESSED_DATA_PATH = os.path.join(PROCESSED_DIR, "processed_data.csv")
ENGINEERED_DATA_PATH = os.path.join(ENGINEERED_DIR, "final_df.csv")
MODEL_SAVE_DIR = os.path.join(DATA_DIR, "model", "trained_model.pkl")
PARAMS_PATH = os.path.join(CONFIG_DIR, "params.json")  # Added params path

# Create directories if they don't exist
os.makedirs(RAW_DATA_DIR, exist_ok=True)
os.makedirs(INGESTED_DATA_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(ENGINEERED_DIR, exist_ok=True)
os.makedirs(os.path.dirname(MODEL_SAVE_DIR), exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)  # Added config directory creation

print(f"Configuration loaded. RAW_DATA_PATH: {RAW_DATA_PATH}")