from __future__ import unicode_literals

import tagulous
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from tunga import settings
from tunga_utils.constants import VISIBILITY_ALL, VISIBILITY_DEVELOPERS, VISIBILITY_PROJECT_OWNERS

VISIBILITY_CHOICES = (
    (VISIBILITY_ALL, 'Everyone'),
    (VISIBILITY_DEVELOPERS, 'Developers'),
    (VISIBILITY_PROJECT_OWNERS, 'Project Owners')
)


@python_2_unicode_compatible
class SupportSection(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=20, unique=True, help_text='url path for this section')
    order = models.PositiveSmallIntegerField(default=0, help_text='0 is the highest order')
    visibility = models.CharField(
        max_length=20, choices=VISIBILITY_CHOICES, default=VISIBILITY_ALL,
        help_text=', '.join(['%s - %s' % (item[0], item[1]) for item in VISIBILITY_CHOICES])
    )
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='support_sections_created', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'section'
        verbose_name_plural = 'sections'
        ordering = ['order', 'title', '-created_at']

    def tags(self):
        return SupportTag.objects.filter(supportpage__section=self)


class SupportTag(tagulous.models.TagModel):

    class TagMeta:
        initial = None
        space_delimiter = False


@python_2_unicode_compatible
class SupportPage(models.Model):
    section = models.ForeignKey(SupportSection, related_name='pages', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=20, help_text="url path for this page (should not include the section slug)")
    content = models.TextField()
    order = models.PositiveSmallIntegerField(default=0, help_text='0 is the highest order')
    visibility = models.CharField(
        max_length=20, choices=VISIBILITY_CHOICES, default=VISIBILITY_ALL,
        help_text=', '.join(['%s - %s' % (item[0], item[1]) for item in VISIBILITY_CHOICES])
    )
    tags = tagulous.models.TagField(to=SupportTag, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='support_pages_created', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'page'
        verbose_name_plural = 'pages'
        ordering = ['order', 'title', '-created_at']
        unique_together = ('section', 'slug')
