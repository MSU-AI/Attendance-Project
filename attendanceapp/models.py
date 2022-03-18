from django.db import models
from gsheets import mixins
from uuid import uuid4


class Person(mixins.SheetSyncableMixin, models.Model):
    spreadsheet_id = 'jeiy4io6M6_oi_0EdBBED969C_djl2ycnaHdCerkDlU'
    model_id_field = 'id'
    class Meta:
        verbose_name_plural = "people"  # Call them "people" rather than "persons"

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=45)
    join_date = models.DateTimeField('date joined')    
    APID = models.IntegerField()
    id = models.BigAutoField(primary_key=True)
    birthday = models.DateField('birthday')
    
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
