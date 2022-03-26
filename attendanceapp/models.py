from django.db import models
from gsheets import mixins
from uuid import uuid4
import datetime
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from gsheets.signals import sheet_row_processed


class Person(mixins.SheetPullableMixin, models.Model):
    spreadsheet_id = "51e28dd0b407332f14bdbd7002db1c5f21df9ed6"
    model_id_field = 'id'
    class Meta:
        verbose_name_plural = "people"  # Call them "people" rather than "persons"

    first_name = models.CharField(max_length=30,default = 'first name')
    last_name = models.CharField(max_length=45, default = 'last name')
    join_date = models.DateTimeField('date joined', default = datetime.date(2000, 1, 1))    
    APID = models.IntegerField(default = 123456789)
    id = models.BigAutoField(primary_key=True)
    birthday = models.DateField('birthday', default = 'YYYY-MM-DD')



    '''
    @receiver(sheet_row_processed, sender=Person)
    def tie_person(instance=None, created=None, row_data=None, **kwargs):
        try:
            instance.first_name = Person.objects.get(first_name__iexact=row_data['first_name'])
            instance.last_name = Person.objects.get(last_name__iexact=row_data['last_name'])
            instance.APID = Person.objects.get(id__iexact=row_data['id'])
            instance.save()
        except (ObjectDoesNotExist, KeyError):
            pass
    '''
    
    def __str__(self):
        return self.name


class Photo(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    # Images are uploaded to media/photos in development
    image = models.ImageField(upload_to='photos')

    def __str__(self):
        return 'Photo of %s' % self.person


class AttendanceEvent(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

    event_date = models.DateTimeField('date logged')

    def __str__(self) -> str:
        return '{} logged on {}'.format(self.person.name, self.event_date)
