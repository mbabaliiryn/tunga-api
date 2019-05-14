from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from tunga import settings
from tunga_utils.constants import VISIBILITY_DEVELOPER, VISIBILITY_MY_TEAM, VISIBILITY_CUSTOM, VISIBILITY_ONLY_ME

VISIBILITY_CHOICES = (
    (VISIBILITY_DEVELOPER, 'Developers'),
    (VISIBILITY_MY_TEAM, 'My Team'),
    (VISIBILITY_CUSTOM, 'Custom'),
    (VISIBILITY_ONLY_ME, 'Only Me')
)


@python_2_unicode_compatible
class Setting(models.Model):
    slug = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100, verbose_name='display name')
    description = models.CharField(max_length=200, blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='%(class)s_created', on_delete=models.DO_NOTHING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


# @python_2_unicode_compatible
class SwitchSetting(Setting):
    default_value = models.BooleanField()


# @python_2_unicode_compatible
class VisibilitySetting(Setting):
    default_value = models.PositiveSmallIntegerField(choices=VISIBILITY_CHOICES)


@python_2_unicode_compatible
class UserSetting(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Settings - %s' % self.user.get_short_name()

    class Meta:
        abstract = True


# @python_2_unicode_compatible
class UserSwitchSetting(UserSetting):
    setting = models.ForeignKey(SwitchSetting, on_delete=models.PROTECT)
    value = models.BooleanField()

    class Meta:
        unique_together = ('user', 'setting')


# @python_2_unicode_compatible
class UserVisibilitySetting(UserSetting):
    setting = models.ForeignKey(VisibilitySetting,on_delete=models.PROTECT)
    value = models.PositiveSmallIntegerField(choices=VISIBILITY_CHOICES)

    class Meta:
        unique_together = ('user', 'setting')
