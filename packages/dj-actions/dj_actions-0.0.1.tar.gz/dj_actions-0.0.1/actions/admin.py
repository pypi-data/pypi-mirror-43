from django.contrib import admin
from .models import ActionInstance, ActionInstanceTask, ActionInstanceTaskRun

def run_action(modeladmin, request, queryset):
    for instance in queryset:
        instance.run()
run_action.short_description = "Run action"

class ActionInstanceTaskInline(admin.TabularInline):
    """AddressInline"""
    model = ActionInstanceTask
    extra = 0

class ActionInstanceAdmin(admin.ModelAdmin):
    """PractitionerAdmin"""
    inlines = (ActionInstanceTaskInline,)
    list_display = (
        'action_id',
        'progress_summary',
        'payload',
        'created_date',
    )
    list_filter = ('action_id', 'created_date',)

    actions = [
        run_action
    ]

class ActionInstanceTaskRunAdmin(admin.ModelAdmin):
    list_display = (
        'task',
        'ok',
        'input',
        'output',
        'created_date'
    )
    list_filter = ('ok', 'created_date',)



admin.site.register(ActionInstance, ActionInstanceAdmin)
admin.site.register(ActionInstanceTaskRun, ActionInstanceTaskRunAdmin)
# admin.site.register(ActionInstanceTask)

