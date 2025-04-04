import os

# Use absolute paths to avoid working directory issues
PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Change these paths to match where your data actually is
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
RAW_DATA_PATH = os.path.join(DATA_DIR, "raw", "raw_data.csv")
INGESTED_DATA_DIR = os.path.join(DATA_DIR, "ingested")
TRAIN_DATA_PATH = os.path.join(INGESTED_DATA_DIR, "train.csv")
TEST_DATA_PATH = os.path.join(INGESTED_DATA_DIR, "test.csv")
PROCESSED_DIR=os.path.join(DATA_DIR,"processed_data")
PROCCESSED_DATA_PATH=os.path.join(INGESTED_DATA_DIR,"processed_data","processed_train.csv")
# Create directories if they don't exist
os.makedirs(os.path.join(DATA_DIR, "raw"), exist_ok=True)
os.makedirs(INGESTED_DATA_DIR, exist_ok=True)
ENGINEERED_DIR=os.path.join(DATA_DIR,"engineered_data")
ENGINEERED_DATA_PATH=os.path.join(DATA_DIR,"engineered_data","final_df.csv")

print(f"Configuration loaded. RAW_DATA_PATH: {RAW_DATA_PATH}")