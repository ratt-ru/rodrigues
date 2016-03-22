
from django.db.models import Model, CharField, DateTimeField, TextField, ForeignKey
from django.contrib.auth.models import User
from django.conf import settings

import docker


docker_client = docker.Client(**settings.DOCKER_SETTINGS)


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

    class Meta:
        ordering = ["started"]

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


class KlikoImage(Model):
    """
    A kliko image
    """
    repository = CharField(blank=False, max_length=255)
    tag = CharField(default='latest', max_length=255)

    last_updated = DateTimeField(blank=True, null=True)
    error_message = TextField(blank=True, null=True)

    # status of the image
    NOT_PULLED = 'N'  # image not pulled yet
    PULLING = 'G'     # image is being pulled from the docker hub
    PULLED = 'P'      # image is downloaded, not verified yet
    INVALID = 'I'     # image is not a kliko container
    VALID = 'V'       # image is a valid kliko container and ready to use

    STATE_TYPES = (
        (NOT_PULLED, 'NOT_PULLED'),
        (PULLING, 'PULLING'),
        (PULLED, 'PULLED'),
        (INVALID, 'INVALID'),
        (VALID, 'VALID'),
    )
    state = CharField(choices=STATE_TYPES, max_length=1, default=NOT_PULLED)

    def __str__(self):
        return self.repository

    def __repr__(self):
        return str(self.id)

    def pulled(self):
        images = docker_client.images(self.repository + ":" + self.tag, quiet=True)
        return bool(images)
