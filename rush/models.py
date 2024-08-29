from django.db import models
from django.urls import reverse
from django.conf import settings


# Create your models here.
class Rushee(models.Model):
    STATUSES = (
        ('n', 'None'),
        ('a', 'Awaiting Bid'),
        ('b', 'Bid Delivered'),
        ('p', 'Pledged'),
    )

    name = models.CharField(max_length=100)
    dorm = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    discord = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUSES, default='None')
    bidder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    last_contact = models.DateField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['status', 'name']

    @property
    def filings(self):
        return len(self.filing_set.all())

    @property
    def short_filings_desc(self):
        text = ''
        for i in Filing.FILING_TYPES:
            text += f'{len(self.filing_set.filter(type__exact=i[0]))}{i[0]} '
        if len(text) > 0:
            return text[:-1]
        else:
            return text

    @property
    def long_filings_desc(self):
        text = ''
        for i in Filing.FILING_TYPES:
            text += f'{len(self.filing_set.filter(type__exact=i[0]))} {i[1]}, '
        if len(text) > 0:
            return text[:-2]
        else:
            return text

    @property
    def autobid(self):
        autobid = Settings.objects.all()[0]

        if self.w > autobid.w or self.f > autobid.f:
            return False
        if self.b >= autobid.b:
            return True
        if self.b + self.n >= autobid.n:
            return True
        return False

    @property
    def b(self):
        return len(self.filing_set.filter(type__exact='b'))

    @property
    def n(self):
        return len(self.filing_set.filter(type__exact='n'))

    @property
    def w(self):
        return len(self.filing_set.filter(type__exact='w'))

    @property
    def f(self):
        return len(self.filing_set.filter(type__exact='f'))

    @property
    def weak(self):
        autobid = Settings.objects.get(id=1)
        return self.w > autobid.w

    @property
    def flush(self):
        autobid = Settings.objects.get(id=1)
        return self.f > autobid.f

    def get_absolute_url(self):
        return reverse('rushee-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.name}'


class Filing(models.Model):
    FILING_TYPES = (
        ('b', 'Bid'),
        ('n', 'No Objection'),
        ('w', 'Weak'),
        ('f', 'Flush'),
    )

    type = models.CharField(max_length=1, choices=FILING_TYPES)

    rushee = models.ForeignKey(Rushee, on_delete=models.CASCADE)
    active = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.type}: {self.rushee}'


class Discord(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    id = models.CharField(max_length=50, primary_key=True)


class Settings(models.Model):
    autobid = models.CharField(max_length=50)

    @property
    def b(self):
        return int(self.autobid.split(',')[0])

    @property
    def n(self):
        return int(self.autobid.split(',')[1])

    @property
    def w(self):
        return int(self.autobid.split(',')[2])

    @property
    def f(self):
        return int(self.autobid.split(',')[3])


class Signin(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    heard = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}: {self.timestamp}'
