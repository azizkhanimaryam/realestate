from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .models import ContactMessage  # If you're saving messages to the database
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from datetime import datetime
from .models import Villa, Apartment, Penthouse, PropertyImage, PropertyVisit
from datetime import datetime
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail  # or your email function


# View for the homepage
def index(request):
    return render(request, 'index.html')

# View for the properties page
def properties(request):
    villas = Villa.objects.all()
    apartments = Apartment.objects.all()
    penthouses = Penthouse.objects.all()

    return render(request, 'properties.html', {
        'villas': villas,
        'apartments': apartments,
        'penthouses': penthouses,
    })

from django.shortcuts import render, redirect
from .models import Villa, Apartment, Penthouse, PropertyVisit
from django.contrib.contenttypes.models import ContentType
from datetime import datetime

def schedule_visit(request):
    if request.method == 'POST':
        property_code = request.POST.get('property_code')  # Get the property code from the form
        visit_date = request.POST.get('visit_date')
        visit_time = request.POST.get('visit_time')
        user_name = request.POST.get('user_name')  # Get user's name
        user_email = request.POST.get('user_email')  # Get user's email
        user_phone = request.POST.get('user_phone')  # Get user's phone number (optional)

        if not visit_date or not visit_time:
            return render(request, 'schedule_form.html', {'error': 'Both date and time are required.'})

        # Combine date and time into a datetime object
        try:
            visit_datetime = datetime.strptime(f"{visit_date} {visit_time}", "%Y-%m-%d %H:%M")
        except ValueError:
            return render(request, 'schedule_form.html', {'error': 'Invalid date or time format.'})

        # Determine the property type and get the corresponding property object
        property_type = request.POST.get('property_type')

        # Fetch the property by code
        if property_type == 'villa':
            property_obj = Villa.objects.get(code=property_code)
        elif property_type == 'apartment':
            property_obj = Apartment.objects.get(code=property_code)
        elif property_type == 'penthouse':
            property_obj = Penthouse.objects.get(code=property_code)
        else:
            return render(request, 'schedule_form.html', {'error': 'Invalid property type.'})

        # Get ContentType for the specific property type
        content_type = ContentType.objects.get_for_model(property_obj)

        # Create PropertyVisit instance with the user details and property code
        visit = PropertyVisit(
            user_name=user_name,
            user_email=user_email,
            user_phone=user_phone,
            visit_datetime=visit_datetime,
            content_type=content_type,
            object_id=property_obj.id
        )
        visit.save()

        # Send confirmation email with property details
        send_confirmation_email(user_email, visit_datetime, property_obj)

        # Redirect to confirmation page
        return render(request, 'schedule_confirmation.html', {'visit': visit})

    # Handle GET request (show form with available properties)
    property_type = request.GET.get('property_type', 'villa')  # Default to villa if not selected

    # Fetch properties based on the selected property type
    if property_type == 'villa':
        properties = Villa.objects.all()
    elif property_type == 'apartment':
        properties = Apartment.objects.all()
    elif property_type == 'penthouse':
        properties = Penthouse.objects.all()
    else:
        properties = []

    return render(request, 'schedule_form.html', {
        'properties': properties,
        'selected_property_type': property_type
    })

def send_confirmation_email(user_email, visit_datetime, property_obj):
    # Send a confirmation email
    subject = 'Your Property Visit Confirmation'
    message = f"""
    Dear user,

    Your visit to the property {property_obj.name} (Code: {property_obj.code}) is scheduled for 
    {visit_datetime.strftime('%Y-%m-%d %H:%M')}. We look forward to your visit!

    If you need to make any changes, please contact us.

    Best regards,
    Your Real Estate Team
    """
    send_mail(subject, message, 'from@example.com', [user_email])




def property_details(request, property_type, property_id):
    # Normalize the property_type to handle case-insensitivity
    property_type = property_type.lower()

    # Check the property type and get the appropriate object
    if property_type == 'villa':
        property_obj = get_object_or_404(Villa, id=property_id)
        images = property_obj.images.all()  # Fetch images for the villa
    elif property_type == 'apartment':
        property_obj = get_object_or_404(Apartment, id=property_id)
        images = property_obj.images.all()  # Fetch images for the apartment
    elif property_type == 'penthouse':
        property_obj = get_object_or_404(Penthouse, id=property_id)
        images = property_obj.images.all()  # Fetch images for the penthouse
    else:
        # If the property type is invalid, return an error page
        return render(request, '404.html', {'error': 'Property type not found'})

    # Pass the object and images to the template
    class_name = property_obj.__class__.__name__
    return render(request, 'property-details.html', {
        'property': property_obj,
        'class_name': class_name,
        'images': images
    })

# View for the contact page
def contact_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Optionally save the message to the database
        contact_message = ContactMessage(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        contact_message.save()

        # Send email
        send_mail(
            f"Message from {name} - {subject}",
            message,
            email,
            [settings.CONTACT_EMAIL],  # Specify the email to receive the messages
            fail_silently=False,
        )

        # Send confirmation to the user
        send_mail(
            "Thank you for contacting us!",
            "We have received your message and will get back to you shortly.",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return render(request, 'contact_success.html', {'name': name})
    return render(request, 'contact.html')