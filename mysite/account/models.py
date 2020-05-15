from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from phone_field import PhoneField
from django.core.validators import RegexValidator
from django.conf import settings
from django.db.models.signals import pre_save
from .utils import unique_video_id_generator
from datetime import date


class MyAccountManager(BaseUserManager):
    def create_user(self, phone, email, username, password):
        if not phone:
            raise ValueError('Users must have a Phone Number')
        if not username:
            raise ValueError('Users must have a username')
        if not email:
            raise ValueError('Users must have an email')

        user = self.model(phone=phone,email=self.normalize_email(email),username=username,password=password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, email, username, password):
        user = self.create_user(phone=phone,email=self.normalize_email(email),password=password,username=username)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    phone_regex = RegexValidator(regex=r'^\d{10,10}$', message="Enter a 10 Digit Phone Number")
    phone = models.CharField(primary_key=True, unique=True,validators=[phone_regex], max_length=13)
    email_regex=RegexValidator(regex=r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)',message="Enter a Valid Email") 
    email=models.CharField(unique=True,validators=[email_regex],verbose_name="Email",max_length=60)
    username=models.CharField(max_length=30,unique=True)
    first_name=models.CharField(max_length=60,blank=True)
    last_name=models.CharField(max_length=60,blank=True)
    bio=models.TextField(blank=True)
    website=models.URLField(default='',blank=True)
    dob=models.DateField(blank=True, null=True)                            
    date_joined=models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login=models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    is_superuser=models.BooleanField(default=False)
    profile_pic=models.ImageField(upload_to='Profiles',default='default.jpg')
    followers=models.IntegerField(default=0)
    following=models.IntegerField(default=0)
    coins = models.IntegerField(default=100)
    streams = models.IntegerField(default=0)
    upvotes = models.IntegerField(default=0)
    coins_donated = models.IntegerField(default=0)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email','username']

    objects = MyAccountManager()
    
    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

	
    def has_module_perms(self, app_label):
        return True


# Create your models here.

'''class User(models.Model):
    phone = PhoneField(primary_key=True, blank=False)
    points = models.IntegerField(default=100)
    streams = models.IntegerField(default=30)
    upvotes = models.IntegerField(default=150)
    points_donated = models.IntegerField(default=120)'''

class Video(models.Model):
    phone = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    name= models.CharField(max_length=500)
    description= models.TextField()
    video= models.FileField(upload_to='videos/', null=True, verbose_name="")
    videoid= models.CharField(primary_key=True, max_length=120, blank=True)
    uploaded=models.DateField(verbose_name='uploaded', auto_now_add=True)
    time=models.TimeField(verbose_name='time', auto_now_add=True)
    likes=models.IntegerField(default=0)
    dislikes=models.IntegerField(default=0)
    shares=models.IntegerField(default=0)


    def __str__(self):
        return self.name + ": " + str(self.video)

def pre_save_video_id(instance, sender, *args, **kwargs):
    if not instance.videoid:
        instance.videoid= unique_video_id_generator(instance)


pre_save.connect(pre_save_video_id, sender=Video)


class Comment(models.Model):
    
    comment= models.TextField('Add a Comment')
    date=models.DateField(verbose_name='date', auto_now_add=True)
    post = models.ForeignKey(Video, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Like(models.Model):
    user=models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="linkingUser")
    post=models.OneToOneField(Video,on_delete=models.CASCADE)
    likes=models.IntegerField(default=0)

    @classmethod
    def liked(cls,post,liking_user):
        obj,create=cls.objects.get_or_create(post=post)
        obj.user.add(liking_user)

    @classmethod
    def dislike(cls,post,disliking_user):
        obj,create=cls.objects.get_or_create(post=post)
        obj.user.remove(disliking_user)

    def __self__(self):
        return str(self.post)
    

