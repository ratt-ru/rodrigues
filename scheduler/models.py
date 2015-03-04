
from django.db.models import Model, CharField, DateTimeField, TextField
from celery.result import AsyncResult
import celery.states


class Job(Model):
    name = TextField(blank=False)
    started = DateTimeField(blank=True, null=True)
    finished = DateTimeField(blank=True, null=True)
    log = TextField(blank=True, null=False)
    task_id = CharField(max_length=36, null=True, blank=True)
    config = TextField()
    docker_image = CharField(max_length=100, null=True, blank=True)
    results_dir = CharField(max_length=20, null=True, blank=True)

    # status of the task
    SCHEDULED = 'S'
    RUNNING = 'R'
    CRASHED = 'C'
    FINISHED = 'F'

    STATE_TYPES = (
        (SCHEDULED, 'scheduled'),
        (RUNNING, 'running'),
        (CRASHED, 'crashed'),
        (FINISHED, 'finished'),
    )
    state = CharField(choices=STATE_TYPES, max_length=1, default=SCHEDULED)

    def __str__(self):
        return "<simulation name='%s' id=%s>" % (self.name, self.id)

    def set_crashed(self, error):
        self.state = self.CRASHED
        self.log = error
        self.started = None
        self.finished = None
        self.save(update_fields=["state", "log", "started", "finished"])

    def set_scheduled(self):
        self.state = self.SCHEDULED
        self.started = None
        self.finished = None
        self.log = ""
        self.save(update_fields=["state", "started", "finished"])

    def get_task_status(self):
        if not self.task_id:
            return 'NO TASK ID'
        try:
            broker_status = AsyncResult(self.task_id).status
            # somehow the job is running but status is PENDING
            if broker_status == celery.states.PENDING and \
                            self.state == self.RUNNING:
                return celery.states.STARTED
            elif broker_status == celery.states.SUCCESS and \
                self.state == self.CRASHED:
                return celery.states.FAILURE
            return broker_status
        except OSError as e:
            return "BROKER DOWN: " + str(e)

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