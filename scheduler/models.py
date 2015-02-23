from django.db.models import Model, CharField, FileField, DateTimeField, TextField
from celery.result import AsyncResult
import celery.states


class Job(Model):
    name = TextField(blank=False)
    started = DateTimeField(blank=True, null=True)
    finished = DateTimeField(blank=True, null=True)
    log = FileField(blank=True, null=True)
    task_id = CharField(max_length=36, null=True, blank=True)
    config = TextField()
    docker_image = TextField()

    def __str__(self):
        return "<simulation name='%s' id=%s>" % (self.name, self.id)

    def set_scheduled(self):
        self.started = None
        self.finished = None
        self.log = ""
        self.save(update_fields=["started", "finished"])

    def clear(self):
        self.started = None
        self.finished = None
        self.log = ""
        self.save()

    def get_task_status(self):
        if not self.task_id:
            return celery.states.FAILURE
        try:
            broker_status = AsyncResult(self.task_id).status
            return broker_status
        except OSError as e:
            return "can't connect to broker: " + str(e)

    def can_reschedule(self):
        """
        We want only to be able reschedule jobs that are finished
        """
        return self.get_task_status() in (celery.states.SUCCESS,
                                          celery.states.FAILURE,
                                          celery.states.REVOKED)

    def duration(self):
        if self.finished and self.started:
            return str(self.finished - self.started)