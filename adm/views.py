from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings
import random
import string
from django.contrib.auth.decorators import login_required
from .models import Cart, ItemDetails

#------------------------------------

#Home Page
def home(request):
    username = request.session.get("username")  # ✅ Get username from session
    return render(request, "index.html", {"username": username, 'messages': messages.get_messages(request)})

#------------------------------------

#User Login SignUp Setup
def LoginSignup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session["username"] = username  # ✅ Store username in session
            messages.success(request, "Login successful.")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'LoginSignup.html')

def Register(request):
    if request.method == 'POST':
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check for errors
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
        else:
            # Create User
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = fname
            user.last_name = lname
            user.save()

            # Save phone number in Profile model
            Profile.objects.create(user=user, phone=phone)

            send_email(email)  # Send welcome email

            messages.success(request, "Account created successfully. Please log in.")
            return redirect('LoginSignup')  # Redirect to login page

    return render(request, "Register.html")  # Show errors in Register page


def ForgetPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            reset_code = generate_reset_code()  # Generate a reset code
            request.session['reset_code'] = reset_code  # Store it in session
            request.session['reset_email'] = email  # Store email too
            send_reset_email(email, reset_code)  # Send email
            
            messages.success(request, "A password reset code has been sent to your email.")
            return redirect('OTPValidation')  # Redirect to reset password page
        else:
            messages.error(request, "Email is not registered.")

    return render(request, 'ForgetPassword.html')


def OTPValidation(request):
    reset_code = request.session.get('reset_code')  # Retrieve code from session
    email = request.session.get('reset_email')  # Retrieve email
    
    if request.method == 'POST':
        entered_code = request.POST.get('otp')

        if entered_code == reset_code:
            messages.success(request, "OTP verified! Please reset your password.")
            return redirect('ResetPassword')
        else:
            messages.error(request, "Invalid OTP. Please try again.")

    return render(request, 'OTPValidation.html')

def ResetPassword(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirmPassword = request.POST.get('confirmPassword')
        
        print(password)
        print(confirmPassword)

        if password == confirmPassword:
            email = request.session.get('reset_email')  # Retrieve email
            user = User.objects.filter(email=email).first()
            user.set_password(password)  # Set new password
            user.save()  # Save user

            messages.success(request, "Password reset successful. Please login.")
            return redirect('LoginSignup')  # Redirect to login page
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'ResetPassword.html')

def Logout(request):
    logout(request)
    request.session.flush()  # ✅ Clear session on logout
    return redirect("home")  # Redirect to login page after logout

#------------------------------------

# Cart Functions
@login_required
def CartPage(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.item.item_price * item.quantity for item in cart_items)

    return render(request, 'Cart.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, item_code):
    item = get_object_or_404(ItemDetails, item_code=item_code)
    cart_item, created = Cart.objects.get_or_create(user=request.user, item=item)

    if not created:
        cart_item.quantity += 1  # Increase quantity if item already exists
        cart_item.save()

    return redirect('AllItems') 

@login_required
def clear_cart(request):
    Cart.objects.filter(user=request.user).delete()
    return redirect('Cart')

def ProceedCart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.item.item_price * item.quantity for item in cart_items)

    UserDetails = User.objects.get(username=request.user)

    # Check if Profile exists before fetching phone number
    profile = Profile.objects.filter(user=request.user).first()
    phone = profile.phone if profile else "Not Provided"

    return render(request, 'ProceedCart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'UserDetails': UserDetails,
        'phone': phone
    })


def PurchaseConfirmation(request):
    return render(request, 'PurchaseConfirmation.html')

#------------------------------------

#All Items Display Page
def AllItems(request):
    items = ItemDetails.objects.all()  # Fetch all items from the database
    return render(request, 'AllItems.html', {'items': items})  # Pass them to the template

#------------------------------------

# Admin Login Setup
def AdminLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:  # Only superusers can login
                login(request, user)
                request.session['admin_name'] = user.username  # Store admin name in session
                messages.success(request, f"Hi {user.username}, welcome back!")
                return redirect('Dashboard')  # Redirect to admin dashboard
            else:
                messages.error(request, "Access denied! Only superusers can log in.")
        else:
            messages.error(request, "Invalid superuser credentials.")

    return render(request, 'AdminLogin.html')  # Render the admin login page

@login_required
def Dashboard(request):
    total_users = User.objects.count()  # Count total users in the database
    total_products = ItemDetails.objects.count()  # Count total products in the database
    return render(request, 'Dashboard.html', {'total_users': total_users, 'total_products': total_products})

@login_required
def ItemDetailsView(request):
     obj=ItemDetails.objects.all() #ORM - (Object Relational Mapping)
     return render(request, 'ItemDetailsView.html', {'obj':obj})

@login_required
def AddItem(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            print("data",request.POST)
            print("data2",request.FILES['image'])
            ItemDetails.objects.create(
                item_code=request.POST.get('item_code'),
                item_name=request.POST.get('item_name'),
                item_price=request.POST.get('item_price'),
                item_desc=request.POST.get('item_desc'),
                item_category=request.POST.get('item_category'),
                item_image=request.FILES['image'],
            )
            return redirect("/ItemDetailsView")
        else:
            messages.error(request, "You must be logged in to add an item.")
            return redirect("Admin")  # Redirect to login page

    return render(request, 'AddItem.html')

@login_required
def DeleteItem(request, pk):
    a = ItemDetails.objects.filter(item_code=pk).first()
    if a:
        a.delete()
    return redirect('/ItemDetailsView')

@login_required
def UserDetailsView(request):
    users = User.objects.select_related('profile').all()
    return render(request, 'UserDetailsView.html', {'users': users})

@login_required
def DeleteUser(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return redirect('UserDetailsView')

@login_required
def AdminLogout(request):
    logout(request)
    request.session.flush()  # Clear session
    return redirect('AdminLogin')  # Redirect to admin login page


#------------------------------------

def send_email(user_email):
    subject = "Welcome to Our Website!"
    message = f"Hello User,\n\n Welcome TO AgriGo."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    send_mail(subject, message, email_from, recipient_list)

    return True  # Return True if the email is sent

def generate_reset_code():
    """Generate a random 6-character reset code"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

def send_reset_email(email, reset_code):
    """Send password reset email"""
    subject = "Password Reset Request"
    message = f"Your password reset code is: {reset_code}\nUse this code to reset your password."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)

