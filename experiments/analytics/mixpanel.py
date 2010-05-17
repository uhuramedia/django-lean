from __future__ import absolute_import

import time

from mixpanel.tasks import EventTracker

from experiments.analytics import IdentificationError
from experiments.analytics.base import BaseAnalytics
from experiments.models import Participant


class Mixpanel(BaseAnalytics):
    def __init__(self, tracker=None, tracker_class=EventTracker):
        if tracker is None:
            tracker = EventTracker()
        self.tracker = tracker
        self.remote_addr = None
        self.identity = None

    def _identify(self, experiment_user):
        self.identity = None
        self.remote_addr = None
        try:
            request = experiment_user.request
        except AttributeError:
            request = experiment_user
        if hasattr(request, 'META'):
            self.remote_addr = request.META.get('REMOTE_ADDR', None)
        try:
            self.identity = self._compute_id(experiment_user)
            return True
        except IdentificationError:
            # Ignore experiment_users who cannot be tied to sessions or users
            return False

    def _properties(self, properties):
        result = {'time': '%d' % time.mktime(time.gmtime())}
        for key, attr in (('ip', 'remote_addr'), ('distinct_id', 'identity')):
            if key not in properties:
                value = getattr(self, attr)
                if value:
                    result[key] = value
        result.update(properties)
        return result

    def enroll(self, experiment, experiment_user, group_id):
        if self._identify(experiment_user):
            properties = self._properties(
                {'Experiment': unicode(experiment),
                 'Group': dict(Participant.GROUPS)[group_id]}
            )
            self.tracker.run(event_name='Enrolled In Experiment',
                             properties=properties)

    def record(self, goal_record, experiment_user):
        if self._identify(experiment_user):
            properties = self._properties(
                {'Goal Type': unicode(goal_record.goal_type)}
            )
            self.tracker.run(event_name='Goal Recorded',
                             properties=properties)
