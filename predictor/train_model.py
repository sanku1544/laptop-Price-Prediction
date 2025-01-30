import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import joblib
import re

# Load the dataset
data = pd.read_csv('predictor/laptop_data.csv')

# Data preprocessing

# Function to clean 'Memory' column and extract numerical values
def clean_memory(value):
    total = 0
    # Handle NaN or missing values
    if pd.isna(value):
        return total
    # Split multiple storage types (e.g., '128GB SSD + 1TB HDD')
    for part in value.split('+'):
        part = part.strip()  # Remove whitespace
        if 'TB' in part:
            total += float(re.search(r'\d+', part).group()) * 1000  # Convert TB to GB
        elif 'GB' in part:
            total += float(re.search(r'\d+', part).group())  # Keep GB as is
    return total

# Clean 'Ram' column: Extract numeric values and convert to float
data['Ram'] = data['Ram'].astype(str).str.extract(r'(\d+)').astype(float)

# Clean 'Memory' column using the clean_memory function
data['Memory'] = data['Memory'].apply(clean_memory)

# Clean 'Weight' column: Remove 'kg' and convert to float
data['Weight'] = data['Weight'].astype(str).str.replace('kg', '').astype(float)

# Handle any missing values after cleaning
data = data.dropna()

# Encode categorical variables
label_encoders = {}
categorical_columns = ['ScreenResolution', 'Cpu', 'Gpu', 'OpSys']

for column in categorical_columns:
    le = LabelEncoder()
    data[column] = le.fit_transform(data[column])
    label_encoders[column] = le  # Save encoder for future use

# Define features and target
X = data[['ScreenResolution', 'Cpu', 'Ram', 'Memory', 'Gpu', 'OpSys', 'Weight']]
y = data['Price']  # Assuming 'Price' is the target column in your CSV

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Save the trained model and encoders
joblib.dump(model, 'predictor/laptop_price_model.pkl')
joblib.dump(label_encoders, 'predictor/label_encoders.pkl')

print("Model training complete! The model and encoders have been saved.")
