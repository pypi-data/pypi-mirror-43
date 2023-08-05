from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers

from .helpers import map_payload
import importlib, timeit

TASK_TYPE = [
    ('sync', 'sync'),
    ('async', 'async'),
    ('scheduled', 'scheduled'),
]

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'first_name', 'last_name', 'email',)


class ActionInstance(models.Model):

    action_id = models.CharField(max_length=100)
    status = models.CharField(default='new', max_length=10)

    actor = JSONField(default=dict, blank=True, null=True)
    payload = JSONField(default=dict, blank=True, null=True)
    context = JSONField(default=dict, blank=True, null=True)
    resource = JSONField(default=dict, blank=True, null=True)

    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True, db_index=True)

    # def save(self, *args, **kwargs):
    #     created = self.pk is None

    #     if self.tasks is None or self.tasks.count() == 0:
    #         self.__generate_tasks()

    #     super(ActionInstance, self).save(*args, **kwargs)

    def __generate_tasks(self):
        if self.configuration is not None:
            tasks = self.configuration.get("tasks", [])
            new_tasks = []
            for task in tasks.get("sync", []):
                task = ActionInstanceTask.from_definition(self, "sync", task)
                task.save()
                new_tasks.append(task)
            return new_tasks

    @property
    def configuration(self):
        return settings.ACTION_MAP.get(self.action_id)

    @property
    def progress_summary(self):
        all_tasks = self.tasks.count()
        complete_tasks = self.tasks.filter(complete=True).count()
        return "{} of {} tasks complete".format(complete_tasks, all_tasks)

    def get_resource(self):
        config = self.configuration
        module_string = config.get('resource_module')
        resource_name = config.get('resource_name')
        filter_map = config.get('resource_filters')

        if module_string is None or resource_name is None or filter_map is None:
            if module_string is not None:
                raise Exception('This task defines a resource, but resource_module is not')
            if resource_name is not None:
                raise Exception('This task defines a resource, but resource_name is not')
            if filter_map is not None:
                raise Exception('This task defines a resource, but resource_filters is not set')
            return None

        module = importlib.import_module(module_string)
        model = getattr(module, resource_name)
        context = {
            "payload": self.payload
        }
        filters = map_payload(filter_map, context)
        instance = model.objects.get(**filters)

        return instance

    def get_resource_list(self):
        pass


    def run(self):
        '''
        Run any tasks that need running
        '''
        tasks = self.tasks.filter(complete=False)
        if len(tasks) == 0:
            tasks = self.__generate_tasks()
        for task in tasks:
            if task.should_run():
                task.run()

class ActionInstanceTask(models.Model):

    def __str__(self):
        return "{}: {}(**{})" .format(
            self.configuration.get('name'),
            self.configuration.get('execute'),
            self.calculated_payload
        )

    action_instance = models.ForeignKey(ActionInstance, on_delete=models.CASCADE, related_name='tasks')
    action_type = models.CharField(max_length=10, default='sync')

    scheduled_time = models.DateField(blank=True, null=True)

    status = models.TextField(default='new')
    configuration = JSONField(default=dict, blank=True, null=True)
    complete = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True, db_index=True)

    @property
    def run_attempts(self):
        return self.attempts.count()

    @property
    def calculated_payload(self):
        mapper = self.configuration.get('mapper', {})
        context = {
            "payload": self.action_instance.payload,
            "resource": self.action_instance.get_resource()
        }
        return map_payload(mapper, context)

    @classmethod
    def from_definition(cls, action_instance, action_type, task_definition):
        task = cls()
        task.action_instance = action_instance
        task_action_type = action_type
        task.configuration = task_definition
        return task

    def add_run_attempt(self, payload, output, success=True, with_save=False, execution_time = 0):
        run = ActionInstanceTaskRun()
        run.task = self
        run.input = payload
        run.output = output
        run.execution_time = execution_time
        run.ok = success
        if with_save:
            run.save()
        return run

    def should_run(self):
        '''
        Based on the config, determine if this should run
        '''
        return True

    def run(self):
        path = self.configuration.get('execute')
        if path is None:
            raise Exception('No execution path found for task: {}: {}'.format(self.id, self))

        bits = path.split('.')
        method_name = bits.pop()
        module_string = (".").join(bits)
        mod = importlib.import_module(module_string)
        payload = self.calculated_payload

        t0 = timeit.default_timer()
        try:
            result = getattr(mod, method_name)(**payload)
            t1 = timeit.default_timer()
            execution_time = t1-t0
        except Exception as ex:
            result = { "exception": str(ex) }
            t1 = timeit.default_timer()
            execution_time = t1-t0
        finally:
            self.add_run_attempt(
                payload,
                result,
                execution_time=execution_time,
                with_save=True
            )
            if self.complete:
                self.save()

        return result


class ActionInstanceTaskRun(models.Model):
    task = models.ForeignKey(ActionInstanceTask, on_delete=models.CASCADE, related_name='attempts')
    input = JSONField(default=dict, blank=True, null=True)
    output = JSONField(default=dict, blank=True, null=True)
    ok = models.BooleanField(default=False)
    execution_time = models.PositiveIntegerField(default=0)

    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    modified_date = models.DateTimeField(auto_now=True, db_index=True)
