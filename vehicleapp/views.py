from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import User, Ride, Drive, RideBook, Help, HelpReply, Payment
from django.core.mail import send_mail
from django.conf import settings

# Home View
def home(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        context = {'uid': uid}
        return render(request, "vehicleapp/index.html", context)
    return redirect("login")

# Logout View
def logout(request):
    if "email" in request.session:
        del request.session['email']
    return redirect("home")

# Login View
def login(request):
    if "email" in request.session:
        return redirect("home")
    
    if request.method == 'POST':
        p_email = request.POST['email']
        p_password = request.POST['password']
        try:
            uid = User.objects.get(email=p_email)
            if uid.password == p_password:
                request.session['email'] = uid.email

                # Send email on successful login
                send_mail(
                    'Login Success - WERide',
                    f'Hi {uid.firstname},\n\nYou have successfully logged in to WERide. We hope you enjoy our service!',
                    settings.EMAIL_HOST_USER,
                    [uid.email],
                    fail_silently=False,
                )

                return redirect("home")
            else:
                context = {'e_msg': "Invalid Password !!"}
                return render(request, "vehicleapp/login.html", context)
        except User.DoesNotExist:
            context = {'e_msg': "Invalid Email Address !!"}
            return render(request, "vehicleapp/login.html", context)
    
    return render(request, "vehicleapp/login.html")

# Signup View
def signup(request):
    if request.method == 'POST':
        uid = User.objects.create(
            firstname=request.POST['firstname'],
            lastname=request.POST['lastname'],
            email=request.POST['email'],
            password=request.POST['password'],
            contact=request.POST['contact'],
            proof_image=request.POST.get('proof_image')
        )
        context = {'msg': "Successfully Account Created !!", 'uid': uid}
        return render(request, "vehicleapp/login.html", context)
    
    return render(request, "vehicleapp/signup.html")

# Profile View
def profile(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        context = {'uid': uid}
        return render(request, "vehicleapp/profile.html", context)
    return redirect("login")

# Change Profile View
def change_profile(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        if request.method == 'POST':
            # Track old values
            old_firstname = uid.firstname
            old_lastname = uid.lastname
            old_contact = uid.contact
            old_picture = uid.pic

            # Update profile fields
            if "picture" in request.FILES:
                uid.pic = request.FILES['picture']
            uid.firstname = request.POST['firstname']
            uid.lastname = request.POST['lastname']
            uid.contact = request.POST['contact']
            uid.save()

            # Prepare email content based on changes
            changes = []
            if old_firstname != uid.firstname:
                changes.append(f"First Name: {old_firstname} -> {uid.firstname}")
            if old_lastname != uid.lastname:
                changes.append(f"Last Name: {old_lastname} -> {uid.lastname}")
            if old_contact != uid.contact:
                changes.append(f"Contact Number: {old_contact} -> {uid.contact}")
            if old_picture != uid.pic:
                changes.append("Profile Picture: Updated")

            # Send email notification
            send_mail(
                'Your Profile Has Been Updated - URide',
                f'Hi {uid.firstname},\n\n'
                f'Your profile has been successfully updated. Here are the changes made:\n\n'
                f"{chr(10).join(changes)}\n\n"
                f'If you did not make these changes or if you believe there is an error, please contact us immediately.\n\n'
                f'Thank you for keeping your profile updated!\n\n'
                f'Best regards,\nURide Team',
                settings.EMAIL_HOST_USER,
                [uid.email],
                fail_silently=False,
            )

            context = {'uid': uid}
            return render(request, "vehicleapp/profile.html", context)
        
        context = {'uid': uid}
        return render(request, "vehicleapp/account.html", context)
    
    return redirect("login")

# Help View
def help(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        if request.method == 'POST':
            # Create help and help reply entries
            hid = Help.objects.create(user_id=uid, message=request.POST['message'])
            reid = HelpReply.objects.create(help_id=hid, user_id=uid)
            
            # Send email when user sends help message
            send_mail(
                'Thank You for Contacting URide',
                f'Hi {uid.firstname},\n\nThank you for reaching out to us! We have received your message:\n\n"{request.POST["message"]}"\n\nWe will get back to you as soon as possible.\n\nBest regards,\nURide Team',
                settings.EMAIL_HOST_USER,
                [uid.email],
                fail_silently=False,
            )

            context = {'uid': uid, 'hid': hid, 'msg': "Successfully Added !!", 'reid': reid}
            return render(request, "vehicleapp/help.html", context)
        
        context = {'uid': uid}
        return render(request, "vehicleapp/help.html", context)
    
    return redirect("login")

# Help Reply View
def helpreply(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        rid = HelpReply.objects.filter(user_id=uid)

        context = {'uid': uid, 'rid': rid}
        return render(request, "vehicleapp/helpreply.html", context)

    return redirect("login")

# Ride View
def ride(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        if request.method == 'POST':
            rid = Ride.objects.create(
                r_email=uid.email,
                sloc=request.POST['sloc'],
                dloc=request.POST['dloc'],
                address=request.POST['address'],
                date=request.POST['date'],
                time=request.POST['time']
            )
            did = Drive.objects.all()
            context = {'uid': uid, 'rid': rid, 'did': did}
            return render(request, "vehicleapp/showdrivers.html", context)
        
        context = {'uid': uid}
        return render(request, "vehicleapp/ride.html", context)
    
    return redirect("login")

# Drive View
def drive(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        if request.method == 'POST':
            did = Drive.objects.create(
                d_email=uid.email,
                vehicle_num=request.POST['vehicle_num'],
                license_num=request.POST['license_num'],
                contact_number=request.POST['contact_number'],
                sloc=request.POST['sloc'],
                dloc=request.POST['dloc'],
                date=request.POST['date'],
                time=request.POST['time'],
                Price=request.POST['Price']
            )
            context = {'uid': uid, 'did': did}
            return render(request, "vehicleapp/drive.html", context)
        
        context = {'uid': uid}
        return render(request, "vehicleapp/drive.html", context)
    
    return redirect("login")

# Book Ride View
def book(request, did):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        did = get_object_or_404(Drive, id=did)
        
        try:
            rid = Ride.objects.get(r_email=uid.email)
        except Ride.MultipleObjectsReturned:
            rides = Ride.objects.filter(r_email=uid.email)
            rid = rides.latest('date')
        except Ride.DoesNotExist:
            return HttpResponse("No ride found.")

        book = RideBook.objects.create(
            r_email=uid.email,
            d_email=did.d_email,
            sloc=rid.sloc,
            dloc=rid.dloc,
            address=rid.address,
            date=rid.date,
            time=rid.time,
            status='PENDING'  # Ensure the status is set to PENDING by default
        )

        context = {'uid': uid, 'book': book, 'rid': rid}
        return render(request, "vehicleapp/book.html", context)
    
    return redirect("login")

# Request View
def request(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        dinfo = RideBook.objects.filter(d_email=uid, status='PENDING')
        context = {'uid': uid, 'dinfo': dinfo}
        return render(request, "vehicleapp/request.html", context)
    
    return redirect("login")

# Driver Activity View
def d_activity(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        dinfo=RideBook.objects.filter(d_email=uid)
        context = {
                'uid': uid, 
                'dinfo':dinfo
            }
        return render(request, "vehicleapp/d_activity.html",context)
    
def r_activity(request):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        rinfo=RideBook.objects.filter(r_email=uid)  
        context = {
                'uid': uid, 
                'rinfo':rinfo
            }
        return render(request, "vehicleapp/r_activity.html",context)

def accept(request): 
    if "email" in request.session:
        uid=User.objects.get(email = request.session['email'])
        ainfo = RideBook.objects.filter(d_email=uid)
        
        if request.method == 'POST':
            for ride in ainfo:
                ride.status = "Accepted"
                ride.save()

            return redirect('home')  # Redirect to a success page after updating the statuses

        context = {
            'ainfo':ainfo
        }
        return render(request, "vehicleapp/request.html", context)
    else:
        return redirect('vehicleapp/request.html')  # Redirect the user to login page if email is not in session


def reject(request):
    if "email" in request.session:
        try:
            email = request.session['email']
            uid = User.objects.get(email=email)
            ainfo_queryset = RideBook.objects.filter(d_email=uid)

            if request.method == 'POST':
                for ainfo in ainfo_queryset:
                    ainfo.status = "Rejected"
                    ainfo.save()  # Call save() on each individual RideBook instance
            return redirect('home')  # Redirect to a success page after updating the statuses

            context = {
                'uid': uid,
                'ainfo_queryset': ainfo_queryset  # Pass the queryset to the context
            }
            return render(request, "vehicleapp/d_activity.html", context)
        except User.DoesNotExist:
            return HttpResponse("User does not exist.")
        except RideBook.DoesNotExist:
            return HttpResponse("Ride booking does not exist.")
        except Exception as e:
            return HttpResponse("An error occurred: " + str(e))
    else:
        return HttpResponse("User email not found in session.")





# Payment View
def payment_view(request, did):
    if "email" in request.session:
        uid = User.objects.get(email=request.session['email'])
        drive = get_object_or_404(Drive, id=did)
        
        if request.method == 'POST':
            amount = request.POST['amount']
            payment = Payment.objects.create(
                user=uid,
                amount=amount,
                status="Pending"
            )

            # Send email notification
            send_mail(
                'Payment Confirmation',
                f'Dear {uid.firstname} {uid.lastname},\n\n'
                f'Thank you for your payment of {amount} for your ride with {drive.d_email} on {drive.date} at {drive.time}.\n\n'
                f'Your booking is confirmed! Below are the details of your ride:\n\n'
                f'Driver Email: {drive.d_email}\n'
                f'Date: {drive.date}\n'
                f'Time: {drive.time}\n'
                f'Pickup Location: {drive.sloc}\n'
                f'Drop-off Location: {drive.dloc}\n'
                f'Amount: {amount}\n\n'
                f'If you have any questions or concerns, please don\'t hesitate to reach out to us.\n\n'
                f'Thank you for choosing URide!',
                settings.EMAIL_HOST_USER,  # Replace with your email
                [uid.email],  # Recipient email
                fail_silently=False,
            )

            return redirect('home')  # Redirect to a success page or home
        
        context = {
            'did': did,
            'amount': drive.Price  # Ensure `Price` field contains the amount
        }
        return render(request, 'vehicleapp/payment.html', context)
    
    return redirect("login")

