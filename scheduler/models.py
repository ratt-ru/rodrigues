
from django.db.models import Model, CharField, DateTimeField, TextField, ForeignKey
from django.contrib.auth.models import User


class Job(Model):
    name = TextField(blank=False)
    started = DateTimeField(blank=True, null=True)
    finished = DateTimeField(blank=True, null=True)
    log = TextField(blank=True, null=False)
    task_id = CharField(max_length=36, null=True, blank=True)
    config = TextField()
    docker_image = CharField(max_length=100, null=True, blank=True)
    results_dir = CharField(max_length=20, null=True, blank=True)
    owner = ForeignKey(User)

    # status of the task
    CREATED = 'I'
    SCHEDULED = 'S'
    RUNNING = 'R'
    CRASHED = 'C'
    FINISHED = 'F'

    STATE_TYPES = (
        (CREATED, 'CREATED'),
        (SCHEDULED, 'SCHEDULED'),
        (RUNNING, 'RUNNING'),
        (CRASHED, 'CRASHED'),
        (FINISHED, 'FINISHED'),
    )
    state = CharField(choices=STATE_TYPES, max_length=1, default=CREATED)

    def __str__(self):
        return "<simulation name='%s' id=%s>" % (self.name, self.id)

    def can_reschedule(self):
        """
        We want only to be able reschedule jobs that are finished
        """
        return self.state in (self.CRASHED, self.FINISHED)

    def duration(self):
        if self.finished and self.started:
            return str(self.finished - self.started)