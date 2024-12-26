from django.contrib import admin
from .models import Villa, Apartment, Penthouse, PropertyImage, PropertyVisit
from django.utils.html import format_html


# Inline model to manage images associated with the property
class PropertyImageInline(admin.TabularInline):  # or admin.StackedInline for vertical layout
    model = PropertyImage
    extra = 1  # Number of empty image forms to display by default
    fields = ['image']

@admin.register(Villa)
class VillaAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'price', 'location', 'bedrooms', 'bathrooms', 'area', 'floor', 'parking', 'description')
    inlines = [PropertyImageInline]  # Display PropertyImages inline for Villa

@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code','price', 'location', 'bedrooms', 'bathrooms', 'area', 'floor', 'parking', 'description')
    inlines = [PropertyImageInline]  # Display PropertyImages inline for Apartment

@admin.register(Penthouse)
class PenthouseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code','price', 'location', 'bedrooms', 'bathrooms', 'area', 'floor', 'parking', 'description')
    inlines = [PropertyImageInline]  # Display PropertyImages inline for Penthouse


class PropertyVisitAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'user_email', 'user_phone', 'visit_datetime', 'get_property_name', 'get_property_code')
    list_filter = ('visit_datetime',)
    search_fields = ('user_name', 'user_email', 'user_phone', 'property__name', 'property__code')
    date_hierarchy = 'visit_datetime'
    ordering = ('visit_datetime',)

    # This method retrieves the name of the related property using GenericForeignKey
    def get_property_name(self, obj):
        return obj.property.name if obj.property else 'No Property'
    get_property_name.admin_order_field = 'property__name'  # Allow ordering by property name
    get_property_name.short_description = 'Property Name'

    def get_property_code(self, obj):
        return obj.property.code if obj.property else 'No Code'
    get_property_code.admin_order_field = 'property__code'  # Allow ordering by property code
    get_property_code.short_description = 'Property Code'


admin.site.register(PropertyVisit, PropertyVisitAdmin)


# Register the PropertyImage model to manage images
admin.site.register(PropertyImage)
