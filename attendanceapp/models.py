from django.db import models


class Person(models.Model):
    class Meta:
        verbose_name_plural = "people"  # Call them "people" rather than "persons"

    name = models.CharField(max_length=200)
    join_date = models.DateTimeField('date joined')

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
