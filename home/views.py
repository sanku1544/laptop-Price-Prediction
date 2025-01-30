from binascii import a2b_base64
from django.shortcuts import render
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt
import io
import base64
import mysql.connector
import pandas as pd
import mysql.connector
import mysql.connector
from django.http import HttpResponse





CSV_FILE_PATH = r'd:\laptop_data.csv'

# ... (rest of your code remains the same)


def home(request):
    return render(request, 'home/index.html')
def about(request):
    return render(request, 'home/about.html')

def contact(request):
    return render(request, 'home/contact.html')

def feedback(request):
    return render(request, 'home/feedback.html')

def profile(request):
    return render(request, 'home/profile.html')


CSV_FILE_PATH = r'd:\laptop_data.csv'  # Define the CSV file path




def ppredict(request):
    if request.method == 'POST':
        try:
            # Extract and validate inputs
            ram = int(request.POST.get('ram', 0))
            memory = int(request.POST.get('memory', 0))
            if ram <= 0 or memory <= 0:
                return render(request, 'predictor/predict1.html', {'error': 'RAM and Memory must be positive numbers.'})

            # Load and preprocess CSV data
            df = pd.read_csv(CSV_FILE_PATH)
            df['ram'] = df['Ram'].str.replace('GB', '', regex=True).astype(int)
            df['memory'] = df['Memory'].str.extract(r'(\d+)', expand=False).astype(int)
            df['predicted_price'] = df['ram'] * df['memory'] * 5  # Price Formula

            # Add user input to dataframe
            new_prediction = ram * memory * 5
            new_row = pd.DataFrame({'ram': [ram], 'memory': [memory], 'predicted_price': [new_prediction]})
            df = pd.concat([df, new_row], ignore_index=True)

            # **SORT DATA to ensure left-bottom to top-right**
            df = df.sort_values(by=['predicted_price'])  

            # Prepare Data for Graph
            x = np.arange(len(df))  # Sorted Indices
            y = df['predicted_price'].values  

            # **Ensure Correct X & Y Alignment**
            if len(x) != len(y):
                raise ValueError("X and Y lengths do not match. Data issue.")

            # Fit Linear Regression Trend Line
            coefficients = np.polyfit(x, y, 1)  
            trend_line = np.poly1d(coefficients)(x)  

            # Create Matplotlib Plot
            fig, ax = plt.subplots(figsize=(8, 5))
            
            # **Plot Green Data Points (Smaller Size)**
            ax.scatter(x, y, color="green", s=10, label="Data Points")  # 🔥 Reduced `s=10` for smaller dots
            
            # **Plot Red Trend Line**
            ax.plot(x, trend_line, color="red", linewidth=2, label="Trend Line")

            # **Highlight User's Prediction**
            ax.scatter(x[-1], new_prediction, color="blue", s=100, label="Prediction")
            ax.annotate(f"{new_prediction:.2f}",
                        xy=(x[-1], new_prediction),
                        xytext=(x[-1] - 2, new_prediction + 10),
                        fontsize=10, color="blue",
                        ha='center')

            # Set Titles and Labels
            ax.set_title("Laptop Price Prediction", fontsize=14)
            ax.set_xlabel("Sorted Data Index", fontsize=12)
            ax.set_ylabel("Predicted Price", fontsize=12)
            ax.legend()
            ax.grid(True)
            ax.set_facecolor('white')

            # **Save Graph to Base64**
            img_io = io.BytesIO()
            plt.savefig(img_io, format='png', bbox_inches='tight')
            img_io.seek(0)
            img_base64 = base64.b64encode(img_io.getvalue()).decode()
            plt.close(fig)

            return render(request, 'predictor/predict1.html', {
                'prediction': new_prediction,
                'img_base64': img_base64,
            })

        except ValueError:
            return render(request, 'predictor/predict1.html', {'error': 'Please enter valid numbers for RAM and Memory.'})
        except Exception as e:
            return render(request, 'predictor/predict1.html', {'error': str(e)})

    return render(request, 'predictor/predict1.html')

import pandas as pd
import numpy as np
import io
import base64
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from django.shortcuts import render


def predict2(request):
    if request.method == 'POST':
        try:
            print("Form submitted successfully.")

            # Debug inputs
            ram = request.POST.get('ram')
            memory = request.POST.get('memory')
            cpu = request.POST.get('cpu')
            print(f"RAM: {ram}, Memory: {memory}, CPU: {cpu}")

            # Ensure inputs are valid and convert to integers
            if not ram or not memory or not cpu:
                raise ValueError('Please provide valid RAM, Memory, and CPU values.')
            ram = int(ram)
            memory = int(memory)

            # Load CSV and check content
            df = pd.read_csv(CSV_FILE_PATH)
            print(f"CSV Loaded: {df.head()}")

            # Ensure necessary columns exist
            if 'Ram' not in df.columns or 'Memory' not in df.columns or 'Cpu' not in df.columns:
                raise ValueError('Missing necessary columns in the CSV.')

            # Convert columns to numeric, coercing errors to NaN
            df['Ram'] = pd.to_numeric(df['Ram'], errors='coerce')
            df['Memory'] = pd.to_numeric(df['Memory'], errors='coerce')

            # Filter out rows with invalid (NaN) values
            df = df.dropna(subset=['Ram', 'Memory'])
            print(f"Processed DataFrame: {df.head()}")

            # Add user input as a new row
            new_row = {'Ram': ram, 'Memory': memory, 'Cpu': cpu}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

            # CPU factor logic
            def calculate_cpu_factor(cpu_value):
                if 'intel' in cpu_value.lower():
                    return 1.5
                elif 'amd' in cpu_value.lower():
                    return 1.2
                return 1.0

            # Apply CPU factor
            df['cpu_factor'] = df['Cpu'].apply(calculate_cpu_factor)
            print(f"DataFrame with CPU Factor: {df.head()}")

            # Prediction logic
            df['predicted_price'] = df['Ram'] * df['Memory'] * 5 * df['cpu_factor']
            prediction = df['predicted_price'].iloc[-1]

            # Debug prediction
            print(f"Prediction: {prediction}")

            # Generate graph data
            x = df.index.values.reshape(-1, 1)  # Reshape to be compatible with LinearRegression
            y = df['predicted_price'].values

            # Linear regression model for the predicted price trend
            model = LinearRegression()
            model.fit(x, y)

            # Generate the trend line
            linear_trend = model.predict(x)

            # Debugging: Check if the linear trend is being calculated correctly
            print(f"Linear Trend: {linear_trend[:5]}")  # Debugging the first few values of the linear trend

            # Create graph
            fig, ax = plt.subplots(figsize=(10, 6))

            # Scatter plot for predicted price points
            ax.scatter(x, y, color='mediumseagreen', label='Predicted Prices', marker='o')

            # Plot the linear regression line (from bottom left to top right)
            ax.plot(x, linear_trend, color='red', linewidth=2, label='Price Trend Line')

            ax.set_title('Price Prediction Graph with Trend Line')
            ax.set_xlabel('Index')
            ax.set_ylabel('Predicted Price')
            ax.legend()

            # Save graph to base64
            img_io = io.BytesIO()
            plt.savefig(img_io, format='png', bbox_inches='tight')
            img_io.seek(0)
            img_base64 = base64.b64encode(img_io.getvalue()).decode()
            print(f"Image Base64 (first 50 chars): {img_base64[:50]}")  # Debug line
            plt.close(fig)

            # Debug graph generation
            print("Graph generated successfully.")

            # Convert DataFrame to HTML
            table_html = df.to_html(classes='table table-striped', index=False)

            # Render template
            return render(request, 'predictor/predict2.html', {
                'table_html': table_html,
                'img_base64': img_base64,
                'prediction': prediction,
                'cpu': cpu,  # Pass CPU info to the template
            })
        except Exception as e:
            print(f"Error in predict2: {str(e)}")
            return render(request, 'predictor/predict2.html', {'error': f"Error: {str(e)}"})

    return render(request, 'predictor/predict2.html')


def contact_form(request):
    if request.method == 'POST':
        # Retrieve data from POST request
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        query = request.POST.get('query')
        msg = request.POST.get('msg')

        # Check if the fields are not empty (basic validation)
        if not name or not mobile or not email or not query or not msg:
            return HttpResponse("All fields are required!", status=400)

        try:
            # Connect to the MySQL database
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",  # Use your database password here
                database="project13"
            )

            cursor = mydb.cursor()

            # Insert the contact form data into the 'contact' table
            cursor.execute(
                "INSERT INTO contact (name, mobile, email, query, msg) VALUES (%s, %s, %s, %s, %s)",
                (name, mobile, email, query, msg)
            )
            mydb.commit()  # Commit the changes to the database
            cursor.close()

            # Return a success message or redirect to a thank-you page
            return render(request, 'home/contact.html', {'message': 'Thank you for contacting us!'})

        except mysql.connector.Error as err:
            # Handle database errors
            return HttpResponse(f"Error: {err}", status=500)

        finally:
            # Ensure that the connection is closed even if an error occurs
            if mydb.is_connected():
                mydb.close()
    else:
        return render(request, 'home/contact.html')  # A form for GET request


def feedback_form(request):
    if request.method == 'POST':
        # Retrieve data from POST request
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        rate = request.POST.get('rate')
        msg = request.POST.get('msg')
        print(rate)

        # Check if the fields are not empty (basic validation)
        if not name or not mobile or not email or not rate or not msg:
            return HttpResponse("All fields are required!", status=400)

        try:
            # Connect to the MySQL database
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",  # Use your database password here
                database="project13"
            )

            cursor = mydb.cursor()

            # Insert the contact form data into the 'contact' table
            cursor.execute(
                "INSERT INTO feedback (name, mobile, email, rate, msg) VALUES (%s, %s, %s, %s, %s)",
                (name, mobile, email, rate, msg)
            )
            mydb.commit()  # Commit the changes to the database
            cursor.close()

            # Return a success message or redirect to a thank-you page
            return render(request, 'home/feedback.html', {'message': 'Thank you for your feedback!'})

        except mysql.connector.Error as err:
            # Handle database errors
            return HttpResponse(f"Error: {err}", status=500)

        finally:
            # Ensure that the connection is closed even if an error occurs
            if mydb.is_connected():
                mydb.close()
    else:
        return render(request, 'home/feedback.html')  # A form for GET request

