from load_data import load_data
from ml_model_3.map_data import generate_location_data

# Load dataset
train_df, dev_df, test_df = load_data()

# Generate results (limit for speed)
df_result = generate_location_data(test_df)

print(df_result.head(10))