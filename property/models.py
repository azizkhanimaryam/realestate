from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import migrations, IntegrityError
import random
import string



class Villa(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=100, unique=True, null=True)  # Make it nullable temporarily
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    area = models.DecimalField(max_digits=6, decimal_places=2)  # in m2
    floor = models.IntegerField()
    parking = models.IntegerField()
    # image = models.ImageField(upload_to='properties/villas/')  # for property images
    description = models.CharField(max_length=255, null=True, blank=True)
    payment_process = models.CharField(max_length=255, null=True, blank=True)

    def generate_unique_code(self):
        """Generate a unique code for the property."""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not Villa.objects.filter(code=code).exists():
                return code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()  # Generate unique code if not set
        super(Villa, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code})"

    def main_image(self):
        # Get the first related image from the PropertyImage model
        first_image = PropertyImage.objects.filter(villa=self).first()
        if first_image:
            return first_image.image.url
        return None




class Apartment(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=100, unique=True, null=True)  # Make it nullable temporarily
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    area = models.DecimalField(max_digits=6, decimal_places=2)  # in m2
    floor = models.IntegerField()
    parking = models.IntegerField()
    # image = models.ImageField(upload_to='properties/apartments/')  # for property images
    description = models.CharField(max_length=255, null=True, blank=True)
    payment_process = models.CharField(max_length=255, null=True, blank=True)


    def generate_unique_code(self):
        """Generate a unique code for the property."""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not Apartment.objects.filter(code=code).exists():
                return code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()  # Generate unique code if not set
        super(Apartment, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code})"

    def main_image(self):
        # Get the first related image from the PropertyImage model
        first_image = PropertyImage.objects.filter(apartment=self).first()
        if first_image:
            return first_image.image.url
        return None




class Penthouse(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=100, unique=True, null=True)  # Make it nullable temporarily
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=200)
    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()
    area = models.DecimalField(max_digits=6, decimal_places=2)  # in m2
    floor = models.IntegerField()
    parking = models.IntegerField()
    # image = models.ImageField(upload_to='properties/penthouses/')  # for property images
    description = models.CharField(max_length=255, null=True, blank=True)
    payment_process = models.CharField(max_length=255, null=True, blank=True)

    def generate_unique_code(self):
        """Generate a unique code for the property."""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not Penthouse.objects.filter(code=code).exists():
                return code

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = self.generate_unique_code()  # Generate unique code if not set
        super(Penthouse, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code})"

    def main_image(self):
        # Get the first related image from the PropertyImage model
        first_image = PropertyImage.objects.filter(penthouse=self).first()
        if first_image:
            return first_image.image.url
        return None


class PropertyImage(models.Model):
    villa = models.ForeignKey(Villa, related_name='images', null=True, blank=True, on_delete=models.CASCADE)
    apartment = models.ForeignKey(Apartment, related_name='images', null=True, blank=True, on_delete=models.CASCADE)
    penthouse = models.ForeignKey(Penthouse, related_name='images', null=True, blank=True, on_delete=models.CASCADE)

    image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        # Display the name of the related property if it exists
        if self.villa:
            return f"Image for {self.villa.name}"
        elif self.apartment:
            return f"Image for {self.apartment.name}"
        elif self.penthouse:
            return f"Image for {self.penthouse.name}"
        return "Image without property"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"

# PropertyVisit model that links to any of the property models
class PropertyVisit(models.Model):
    user_name = models.CharField(max_length=200, default="Guest")  # Set a default value for the name
    user_email = models.EmailField(null=True)  # Make it non-nullable after migration
    user_phone = models.CharField(max_length=15, blank=True, null=True)  # Optional phone number
    visit_datetime = models.DateTimeField()

    # Use contenttypes to link to any of the property models
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    property = GenericForeignKey('content_type', 'object_id')  # This allows linking to any property model

    def __str__(self):
        return f"Visit for {self.property.name} ({self.property.code}) scheduled on {self.visit_datetime}"
