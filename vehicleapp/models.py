from django.db import models

# Create your models here.

class User(models.Model):
    email=models.EmailField(unique=True,max_length=30,blank=False)
    password=models.CharField(max_length=30)
    firstname=models.CharField(max_length=30)
    lastname=models.CharField(max_length=30)
    contact=models.CharField(max_length=30)
    proof_image=models.ImageField(null=True, blank=True, upload_to="image/")
    pic=models.FileField(upload_to="media/upload",default="media/c_default.png")
    is_active=models.BooleanField(default=False)
    is_verify=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    

class Help(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    message=models.TextField(max_length=100)

    def __str__(self):
        return self.user_id.email
     
class HelpReply(models.Model):
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    help_id=models.ForeignKey(Help,on_delete=models.CASCADE)
    reply=models.TextField(null=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user_id.email 
    
class Ride(models.Model):
    r_email=models.EmailField(max_length=30,blank=False)
    sloc=models.CharField(max_length=50)
    dloc=models.CharField(max_length=50)
    address=models.CharField(max_length=100,default=1)
    date=models.DateField()
    time=models.TimeField()

    def __str__(self):
        return self.r_email 
    
class Drive(models.Model):
    d_email=models.EmailField(max_length=30,blank=False)
    vehicle_num=models.CharField(max_length=20)
    license_num=models.CharField(max_length=20)
    contact_number=models.CharField(max_length=30,default=0)
    sloc=models.CharField(max_length=50)
    dloc=models.CharField(max_length=50)
    date=models.DateField()
    time=models.TimeField()
    Price = models.IntegerField(default=0, null=True, blank=True)


    def __str__(self):
        return self.d_email

    def getFirstname(self):
        uid = User.objects.get(email = self.d_email)
        return uid.firstname

    def getLastname(self):
        uid = User.objects.get(email = self.d_email)
        return uid.lastname
    
    def getPic(self):
        uid = User.objects.get(email = self.d_email)
        return uid.pic.url 
    

class RideBook(models.Model):
    r_email=models.EmailField(max_length=30,blank=False)
    d_email=models.EmailField(max_length=30,blank=False)
    sloc=models.CharField(max_length=50)
    dloc=models.CharField(max_length=50)
    address=models.CharField(max_length=100,default=1)
    date=models.DateField()
    time=models.TimeField()
    status=models.CharField(max_length=20,default="PENDING")

    def __str__(self):
        return self.r_email
    
    def getFirstname(self):
        uid = User.objects.get(email = self.d_email)
        return uid.firstname
    
    def getLastname(self):
        uid = User.objects.get(email = self.d_email)
        return uid.lastname
    
    def getrFirstname(self):
        uid = User.objects.get(email = self.r_email)
        return uid.firstname
    
    def getrLastname(self):
        uid = User.objects.get(email = self.r_email)
        return uid.lastname
    
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)