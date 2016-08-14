from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin

from ctf_gameserver.web.admin import admin_site
from . import models, forms


admin_site.register(models.Service)


@admin.register(models.Flag, site=admin_site)
class FlagAdmin(admin.ModelAdmin):

    list_display = ('id', 'service', 'protecting_team', 'tick')
    list_filer = ('service', 'tick')
    search_fields = ('service__name', 'protecting_team__user__username', 'tick')


@admin.register(models.Capture, site=admin_site)
class CaptureAdmin(admin.ModelAdmin):

    class ServiceFilter(admin.SimpleListFilter):
        """
        Admin list filter which allows to filter the captures by their flag's service.
        """
        title = _('service')
        parameter_name = 'service'

        def lookups(self, request, model_admin):
            return models.Service.objects.values_list('pk', 'name')

        def queryset(self, request, queryset):
            if self.value():
                return queryset.filter(flag__service__pk=self.value())

    def protecting_team(self, capture):
        """
        Returns the protecing team of the capture's flag for usage in `list_display`.
        """
        return capture.flag.protecting_team

    def service(self, capture):
        """
        Returns the service of the capture's flag for usage in `list_display`.
        """
        return capture.flag.service

    def tick(self, capture):
        """
        Returns the tick of the capture's flag for usage in `list_display`.
        """
        return capture.flag.tick

    list_display = ('id', 'capturing_team', 'protecting_team', 'service', 'tick')
    list_filter = (ServiceFilter,)
    search_fields = ('capturing_team__user__username', 'flag__protecting_team__user__username',
                     'flag__service__name')
    ordering = ('timestamp',)


@admin.register(models.StatusCheck, site=admin_site)
class StatusCheckAdmin(admin.ModelAdmin):

    list_display = ('id', 'service', 'team', 'tick', 'status')
    list_filter = ('service', 'tick', 'status')
    search_fields = ('service__name', 'team__user__username')
    ordering = ('tick', 'timestamp')


@admin.register(models.GameControl, site=admin_site)
class GameControlAdmin(admin.ModelAdmin):
    """
    Admin object for the single GameControl object. Since at most one instance exists at any time, 'Add' and
    'Delete links' are hidden and a request for the object list will directly redirect to the instance.
    """

    form = forms.GameControlAdminForm

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, instance=None):
        return False

    def changelist_view(self, extra_context=None):
        game_control = models.GameControl.objects.get()
        return redirect('admin:scoring_gamecontrol_change', game_control.pk, permanent=True)
