from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from gsheets.signals import sheet_row_processed
from .models import Person

@receiver(sheet_row_processed, sender=Person)
def tie_person(instance=None, created=None, row_data=None, **kwargs):
    try:
        instance.first_name = Person.objects.get(first_name__iexact=row_data['first_name'])
        instance.last_name = Person.objects.get(last_name__iexact=row_data['last_name'])
        instance.APID = Person.objects.get(id__iexact=row_data['id'])
        instance.save()
    except (ObjectDoesNotExist, KeyError):
        pass