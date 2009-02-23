from django.db import models
from django.contrib import admin

class Page(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField("Page Location", max_length=400, help_text="A url to the page. Pages can be placed in the /media/ directory.")
    def __str__(self):
        return self.name

class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    search_fields = ('name', 'sysname')
    ordering = ('name',)

admin.site.register(Page, PageAdmin)

class Factor(models.Model):
    name = models.CharField(max_length=200)
    upper = models.CharField(max_length=200)
    lower = models.CharField(max_length=200)
    range = models.PositiveIntegerField()
    def __str__(self):
        return self.name

class FactorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)

admin.site.register(Factor, FactorAdmin)

class Rating(models.Model):
    ip = models.IPAddressField(blank=True, null=True)
    hostname = models.CharField(max_length=400, blank=True, null=True)
    taken = models.DateTimeField(auto_now=True)
    finished = models.BooleanField(default=False)
    def __str__(self):
        return "%s taken %s" % (self.ip, self.taken)

class RatingAdmin(admin.ModelAdmin):
    list_display = ('ip', 'hostname', 'taken', 'finished')
    list_filter = ('finished',)
    search_fields = ('ip', 'hostname')
    ordering = ('taken',)

admin.site.register(Rating, RatingAdmin)

class Score(models.Model):
    rating = models.ForeignKey(Rating)
    page = models.ForeignKey(Page)
    factor = models.ForeignKey(Factor)
    value = models.IntegerField()

class ScoreAdmin(admin.ModelAdmin):
    list_display = ('rating', 'page', 'factor', 'value')
    list_filter = ('page','factor')

admin.site.register(Score, ScoreAdmin)
