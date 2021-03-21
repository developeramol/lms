from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
# from colorfield.fields import ColorField
from django_countries.fields import CountryField

from colorful.fields import RGBColorField

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
status_choices = (
    ('1', 'active'),
    ('2', 'inactive')
)

countries = (
    ('1', 'India'),
)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
class lead_sources(models.Model):
    source_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    total_lead = models.IntegerField(default=0)
    user = models.CharField(max_length=50, default='SUPERADMIN')
    status = models.CharField(max_length=20, choices=status_choices, default='1')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
class lead_status(models.Model):
    status_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    background_color = RGBColorField(colors=['#FF0000', '#00FF00', '#0000FF'])
    text_color = RGBColorField(colors=['#FF0000', '#00FF00', '#0000FF'])
    total_lead = models.IntegerField(default=0)
    user = models.CharField(max_length=50, default='SUPERADMIN')
    status = models.CharField(max_length=20, choices=status_choices, default='1')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.name)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class user_admin(models.Model):
    admin_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10)
    image = models.ImageField(upload_to='Admin_images/%Y/%m/%d/', default='image/admin.png', blank=True)
    status = models.CharField(max_length=20, choices=status_choices, default='1')
    parent = models.CharField(max_length=20, default='SUPERADMIN')
    created = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=10, default='ADMIN')

    def __str__(self):
        return str(self.user.username)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class user_client(models.Model):
    client_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10)
    image = models.ImageField(upload_to='Admin_images/%Y/%m/%d/', default='image/admin.png', blank=True)
    status = models.CharField(max_length=20, choices=status_choices, default='1')
    parent = models.OneToOneField(user_admin, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    user_type = models.CharField(max_length=10, default='CLIENT')

    def __str__(self):
        return str(self.username)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class create_lead(models.Model):
    lead_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    query = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    email = models.EmailField(max_length=50, unique=True)
    lead_sour = models.ForeignKey(lead_sources, on_delete=models.CASCADE)
    lead_stat = models.ForeignKey(lead_status, on_delete=models.CASCADE)
    lead_assign = models.ForeignKey(user_admin, on_delete=models.CASCADE)
    description = models.TextField(max_length=200)
    remark = models.TextField(default='Created Lead')
    follow_up_date = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    class Meta:
        ordering = ['-lead_id', ]

    def __str__(self):
        return self.name + ' ' + str(self.lead_stat)


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

class Customer(models.Model):
    firstname = models.CharField(max_length=80)
    lastname = models.CharField(max_length=80)
    email = models.EmailField()
    phone = models.CharField(max_length=12)
    website = models.URLField(max_length=1000, blank=True, null=True)
    position = models.CharField(max_length=200)
    company = models.CharField(max_length=100)
    gst_number = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=10, choices=countries, default='1')
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    contact = models.CharField(max_length=12)

    def __str__(self):
        return self.firstname + ' ' + self.lastname + ' From ' + self.city
