import mysql.connector
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.hashers import make_password, check_password


@login_required
def update_profile(request):
    if request.method == 'POST':
        # Handle the profile update logic
        username = request.POST.get('username')
        email = request.POST.get('email')
        bio = request.POST.get('bio')

        # Update the user fields
        request.user.username = username
        request.user.email = email
        
        # Handle the user profile if it exists
        if hasattr(request.user, 'userprofile'):
            request.user.userprofile.bio = bio
            request.user.userprofile.save()
        else:
            # Create a new user profile if not already created
            request.user.userprofile.create(bio=bio)
        
        request.user.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('accounts:profile')  # Redirect to the profile page

    return render(request, 'accounts/profile.html')


def signup(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        upass = request.POST.get('upass')  # Avoid storing passwords in plaintext
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')

        # Connect to the MySQL database
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="project13"  # Replace with your database name
        )

        cursor = mydb.cursor()

        # Check if the email already exists
        cursor.execute("SELECT * FROM usermast WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            messages.error(request, "Email already Used!")
            cursor.close()
            return redirect('accounts:signup')

        # Insert the new user into the database with hashed password
        cursor.execute(
            "INSERT INTO usermast (uname, upass, email, mobile) VALUES (%s, %s, %s, %s)",
            (uname, upass, email, mobile)
        )
        mydb.commit()  # Commit changes to the database
        cursor.close()

        messages.success(request, f'Account created for {uname}!')
        return redirect('accounts:login')
    return render(request, 'accounts/signup.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        upass = request.POST.get('upass')

        # Connect to the MySQL database
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="project13"  # Replace with your database name
        )

        cursor = mydb.cursor()

        try:
            # Check if the user exists using email
            cursor.execute("SELECT * FROM usermast WHERE email = %s", (email,))
            user = cursor.fetchone()

            cursor.fetchall()  # Explicitly consume any remaining results

            print(upass,user[3])


            if user:
                # Check if the password matches the hashed password
                if upass==user[3]:  # user[3] is the hashed password
                    
                    # Create session for the user
                    request.session['uid'] = user[0]  # Storing user UID in session
                    request.session['email'] = user[2]  # Storing email in session
                    request.session['uname'] = user[1]  # Storing username in session
                    return redirect('home')  # Redirect to home page after successful login
                else:
                    messages.error(request, "Invalid password")
            else:
                messages.error(request, "User does not exist")

        except mysql.connector.Error as e:
            messages.error(request, f"Database error: {str(e)}")
        finally:
            cursor.close()

    return render(request, 'accounts/login.html')


def logout_view(request):
    auth_logout(request)  # Log the user out
    request.session.flush()  # Clear the session data
    return redirect('home')  # Redirect to home page after logout


def profile_view(request):
    uid = request.session.get('uid')
    email = request.session.get('email')
    uname = request.session.get('uname')

    return render(request, 'accounts/profile.html', {'uname': uname, 'email': email})


from django.shortcuts import render, redirect
from django.contrib import messages

def subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")
        
        # Save the email to the database (Assuming a Subscriber model exists)
        # Subscriber.objects.create(email=email)

        request.session["subscribed"] = True  # Store in session
        messages.success(request, "Thanks for subscribing!")
        return redirect("home")  # Redirect to home or any page

    return render(request, "accounts/base.html", {"subscribed": request.session.get("subscribed", False)})

import random
import smtplib
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
import mysql.connector

# Store OTP temporarily (use database in production)
otp_storage = {}

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Connect to MySQL
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="",
            database="project13"
        )
        cursor = mydb.cursor()

        # Check if email exists
        cursor.execute("SELECT * FROM usermast WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            messages.error(request, "Email not registered!")
            return redirect('accounts:forgot_password')

        # Generate OTP
        otp = str(random.randint(100000, 999999))
        otp_storage[email] = otp  # Store OTP in dictionary

        # Send OTP via Email
        subject = "Password Reset OTP"
        message = f"Your OTP for password reset is: {otp}"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
            return render(request, 'accounts/verify_otp.html', {'email': email})
        except smtplib.SMTPException as e:
            messages.error(request, f"Error sending email: {str(e)}")

    return render(request, 'accounts/forgot_password.html')


def send_otp_email(email, otp):
    sender_email = "your-email@gmail.com"  # Update with your email
    sender_password = "your-email-password"  # Update with your email password

    subject = "Your Password Reset OTP"
    message = f"Your OTP for password reset is: {otp}"

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = email

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, email, msg.as_string())
        server.quit()
    except Exception as e:
        print("Error sending email:", e)

def verify_otp(request):
    email = request.GET.get('email')

    if request.method == "POST":
        otp_entered = request.POST.get('otp')
        new_password = request.POST.get('new_password')

        # Check if OTP is correct
        if email in otp_storage and otp_storage[email] == otp_entered:
            # Hash the new password
            hashed_password = new_password  # Use Django's make_password(new_password) for security

            # Update password in MySQL
            mydb = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="",
                database="project13"
            )
            cursor = mydb.cursor()

            cursor.execute("UPDATE usermast SET upass = %s WHERE email = %s", (hashed_password, email))
            mydb.commit()
            cursor.close()

            # Remove OTP after successful reset
            del otp_storage[email]

            messages.success(request, "Password reset successfully! Please login.")
            return redirect('accounts:login')

        else:
            messages.error(request, "Invalid OTP!")

    return render(request, 'accounts/verify_otp.html', {'email': email})



