from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from ctf_gameserver.web.registration.models import Team


class Service(models.Model):
    """
    Database representation of a service from the competition.
    """

    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


class Flag(models.Model):
    """
    Database representation of a flag. The actual flag string needn't be stored, as its relevant parts can be
    reconstructed from this information.
    """

    service = models.ForeignKey(Service)
    protecting_team = models.ForeignKey(Team)
    tick = models.PositiveSmallIntegerField()
    # NULL means the flag has been generated, but not yet placed
    placement_start = models.DateTimeField(null=True, blank=True, default=None)
    placement_end = models.DateTimeField(null=True, blank=True, default=None)

    class Meta:
        unique_together = ('service', 'protecting_team', 'tick')
        index_together = (
            ('service', 'tick'),
            ('service', 'protecting_team', 'tick')
        )

    def __str__(self):
        return 'Flag {:d}'.format(self.id)


class Capture(models.Model):
    """
    Database representation of a capture, i.e. the (successful) submission of a particular flag by one team.
    """

    flag = models.ForeignKey(Flag)
    capturing_team = models.ForeignKey(Team)
    tick = models.PositiveSmallIntegerField()
    # Number of times the flag has been attempted to submit after the intial capture, to punish repeated
    # submission
    count = models.PositiveSmallIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('flag', 'capturing_team')
        index_together = ('flag', 'capturing_team')

    def __str__(self):
        return 'Capture {:d}'.format(self.id)


class StatusCheck(models.Model):
    """
    Storage for the result from a status check. We store the checker script's result for every service and
    team per tick.
    """

    # Mapping from human-readable status texts to their integer values in the database
    # For a discussion on the plural form of "status", refer to https://english.stackexchange.com/q/877
    STATUSES = {
        _('up'): 0,
        _('down'): 1,
        _('faulty'): 2,
        _('flag not found'): 3,
        _('recovering'): 4
    }

    service = models.ForeignKey(Service)
    team = models.ForeignKey(Team)
    tick = models.PositiveSmallIntegerField(db_index=True)
    status = models.PositiveSmallIntegerField(choices=[(i, t) for t, i in STATUSES.items()])
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('service', 'team', 'tick')
        index_together = (
            ('service', 'tick', 'status'),
            ('service', 'team', 'status')
        )

    def __str__(self):
        return 'Status check {:d}'.format(self.id)


class GameControl(models.Model):
    """
    Single-row database table to store control information for the competition.
    """

    # Start and end times for the whole competition: Make them NULL-able (for the initial state), but not
    # blank-able (have to be set upon editing)
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    paused = models.BooleanField(default=False)
    # Tick duration in seconds
    tick_duration = models.PositiveSmallIntegerField(default=180)
    # Number of ticks a flag is valid for including the one it was generated in
    valid_ticks = models.PositiveSmallIntegerField(default=5)
    current_tick = models.SmallIntegerField(default=-1)
    registration_open = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Game control'

    class GetOrCreateManager(models.Manager):
        def get_queryset(self):
            queryset = super().get_queryset()

            if not queryset.exists():
                game_control = queryset.model()
                game_control.save()

            return queryset

    # Change default manager to create the single GameControl instance if it's not already present
    objects = GetOrCreateManager()

    def clean(self):
        """
        Ensures that only one instance of the class gets created.
        Inspired by https://stackoverflow.com/a/6436008.
        """
        cls = self.__class__

        if cls.objects.count() > 0 and self.id != cls.objects.get().id:
            # pylint: disable=no-member
            raise ValidationError(_('Only a single instance of {cls} can be created')
                                  .format(cls=cls.__name__))

    def competition_running(self):
        """
        Indicates whether the competition is currently active.
        """
        if self.start is None or self.end is None or self.paused:
            return False

        return self.start < timezone.now() < self.end

    def competition_over(self):
        """
        Indicates whether the competition is already over.
        """
        if self.start is None or self.end is None:
            return False

        return self.end < timezone.now()
