from django.shortcuts import render
import joblib
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import io
import base64
import numpy as np

# Load the saved model and encoders
model = joblib.load('predictor/laptop_price_model.pkl')
label_encoders = joblib.load('predictor/label_encoders.pkl')


def fetch_laptop_data():
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host="localhost", user="root", password="password", database="admin"
    )
    cursor = conn.cursor(dictionary=True)

    # Fetch data from the laptopdata table
    cursor.execute("SELECT * FROM laptopdata")
    rows = cursor.fetchall()
    conn.close()

    return pd.DataFrame(rows)


def predictor(request):
    return render(request, 'home/index.html')


def allinone(request):
    # Fetch data from the database
    laptop_data = fetch_laptop_data()

    # Extract unique values for dropdown lists
    unique_screen_resolutions = laptop_data['ScreenResolution'].unique()
    unique_screen_sizes = laptop_data['Inches'].unique()
    unique_cpus = laptop_data['Cpu'].unique()
    unique_gpus = laptop_data['Gpu'].unique()
    unique_opsys = laptop_data['OpSys'].unique()
    unique_companies = laptop_data['Company'].unique()
    unique_typename = laptop_data['TypeName'].unique()
    unique_ram_values = laptop_data['Ram'].unique()
    unique_memory_values = laptop_data['Memory'].unique()
    unique_weight_values = laptop_data['Weight'].unique()

    # Pass the values to the template
    context = {
        'screen_resolutions': unique_screen_resolutions,
        'screen_sizes': unique_screen_sizes,
        'cpus': unique_cpus,
        'gpus': unique_gpus,
        'opsys': unique_opsys,
        'companies': unique_companies,
        'typename_list': unique_typename,
        'ram_values': unique_ram_values,
        'memory_values': unique_memory_values,
        'weight_values': unique_weight_values,
    }
    return render(request, 'predictor/main.html', context)


def extend_label_encoder(encoder, value):
    """Extend the encoder classes to include unseen labels."""
    if value not in encoder.classes_:
        encoder.classes_ = np.append(encoder.classes_, value)
    return encoder.transform([value])[0]


def predict_price(request):
    if request.method == 'POST':
        # Extract form data
        screen_resolution = request.POST['screen_resolution']
        cpu = request.POST['cpu']
        ram = float(request.POST['ram'].replace('GB', '').strip())
        memory_str = request.POST['memory']
        memory = float(''.join(filter(str.isdigit, memory_str)))
        gpu = request.POST['gpu']
        opsys = request.POST['opsys']
        weight_str = request.POST['weight']
        weight = float(''.join(filter(str.isdigit, weight_str)))

        # Prepare the input data for prediction
        try:
            encoded_data = {
                'ScreenResolution': extend_label_encoder(label_encoders['ScreenResolution'], screen_resolution),
                'Cpu': extend_label_encoder(label_encoders['Cpu'], cpu),
                'Ram': ram,
                'Memory': memory,
                'Gpu': extend_label_encoder(label_encoders['Gpu'], gpu),
                'OpSys': extend_label_encoder(label_encoders['OpSys'], opsys),
                'Weight': weight,
            }
        except Exception as e:
            return render(request, 'predictor/error.html', {'error': f'Error encoding input: {e}'})

        # Convert to DataFrame
        input_data = pd.DataFrame([encoded_data])

        # Expected feature names
        expected_columns = ['ScreenResolution', 'Cpu', 'Ram', 'Memory', 'Gpu', 'OpSys', 'Weight']

        # Reorder and filter columns to match training features
        input_data = input_data[expected_columns]

        # Make prediction
        try:
            predicted_price = model.predict(input_data)[0]
        except Exception as e:
            return render(request, 'predictor/error.html', {'error': f'Error during prediction: {e}'})

        # Generate a graph with Y-axis focused on the predicted price
        plt.figure(figsize=(8, 5))
        sample_indices = range(5)
        sample_prices = [predicted_price - 50 + i * 25 for i in sample_indices]

        # Plotting the accurate predicted price line
        plt.plot(sample_indices, sample_prices, label="Price Trend", color="green", linewidth=2)
        plt.axhline(y=predicted_price, color='red', linestyle='--', label="Predicted Price")
        plt.ylim(min(sample_prices) - 10, max(sample_prices) + 10)
        plt.yticks(sample_prices)
        plt.title("Accurate Price Line Graph")
        plt.xlabel("Sample Index")
        plt.ylabel("Price (Rs)")
        plt.legend()
        plt.grid(alpha=0.3)

        # Save the graph to a BytesIO stream
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        graph_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        buffer.close()

        # Render the result
        return render(request, 'predictor/result.html', {
            'price': round(predicted_price, 2),
            'graph': graph_base64
        })

    return render(request, 'predictor/main.html')
