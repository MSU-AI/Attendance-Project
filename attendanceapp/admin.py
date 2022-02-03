from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Person, Photo, AttendanceEvent

# The models listed here will appear in the admin panel
# (If we don't list them, they will exist in the database
# but be invisible from the Admin side.)


class PhotoAdmin(admin.StackedInline):
    """
    Represents an image in the admin panel.

    This class is designed to work as an inline in the admin panel,
    meaning that we will be displayed under the Person menu.

    We also define the 'image_preview' method which 
    allows the picture this class represents to be viewed.
    This method is a bit 'hackish', 
    as it inserts the necessary HTML to display the image
    directly into the admin menu.
    A better solution may lie elsewhere, but for now this works.

    We re-scale the image with a width of 350 pixels,
    and keep the height set to 'auto' to keep the aspect ratio.
    The width scaling can be defined using the 'scale' attribute.
    """

    readonly_fields = ["image_preview"]
    model = Photo
    extra = 0  # Makes sure we don't have empty extra responses
    scale = '350'  # Scale width by some amount, accepts 

    def image_preview(self, obj):

        # Return the image preview, but scale it down by an amount:

        return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
            url = obj.image.url,
            width=self.scale,
            height='auto'))

    image_preview.short_description = "Image Preview"


class AttendanceAdmin(admin.StackedInline):

    extra = 0
    model = AttendanceEvent


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):

    inlines = [PhotoAdmin, AttendanceAdmin]
