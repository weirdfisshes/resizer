import django.db


class Image(django.db.models.Model):
    hash = django.db.models.CharField(max_length=32)
    path = django.db.models.FilePathField(blank=True, null=True)
    width = django.db.models.IntegerField(blank=True, null=True)
    height = django.db.models.IntegerField(blank=True, null=True)
