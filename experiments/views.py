import logging
l = logging.getLogger(__name__)

from datetime import date, timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, RequestContext
from django.views.decorators.cache import never_cache

from experiments.models import (Experiment, Participant, GoalRecord,
                                      DailyActivityReport)
from experiments.reports import get_conversion_data
from experiments.util import WebUser

experiment_states= {"enabled": Experiment.ENABLED_STATE,
  "disabled": Experiment.DISABLED_STATE,
  "promoted": Experiment.PROMOTED_STATE}

TRANSPARENT_1X1_PNG = \
("\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d\x49\x48\x44\x52"
 "\x00\x00\x00\x01\x00\x00\x00\x01\x08\x03\x00\x00\x00\x28\xcb\x34"
 "\xbb\x00\x00\x00\x19\x74\x45\x58\x74\x53\x6f\x66\x74\x77\x61\x72"
 "\x65\x00\x41\x64\x6f\x62\x65\x20\x49\x6d\x61\x67\x65\x52\x65\x61"
 "\x64\x79\x71\xc9\x65\x3c\x00\x00\x00\x06\x50\x4c\x54\x45\x00\x00"
 "\x00\x00\x00\x00\xa5\x67\xb9\xcf\x00\x00\x00\x01\x74\x52\x4e\x53"
 "\x00\x40\xe6\xd8\x66\x00\x00\x00\x0c\x49\x44\x41\x54\x78\xda\x62"
 "\x60\x00\x08\x30\x00\x00\x02\x00\x01\x4f\x6d\x59\xe1\x00\x00\x00"
 "\x00\x49\x45\x4e\x44\xae\x42\x60\x82\x00")


@never_cache
def confirm_human(request):
    experiment_user = WebUser(request)
    experiment_user.confirm_human()
    return HttpResponse(status=204)


@never_cache
def record_experiment_goal(request, goal_name):
    try:
        GoalRecord.record(goal_name, WebUser(request))
    except Exception, e:
        l.warn("unknown goal type '%s': %s" % (goal_name, e))

    return HttpResponse(TRANSPARENT_1X1_PNG, mimetype="image/png")


@staff_member_required
def list_experiments(request, template_name='ListExperiments.html'):
    """docstring for list_experiments"""
    context_var = {"experiments": Experiment.objects.order_by("-start_date"),
                   "experiment_states": experiment_states}

    return render_to_response(template_name, context_var,
                              context_instance=RequestContext(request))


@staff_member_required
def experiment_details(request, experiment_name,
                       template_name="ExperimentDetails.html"):
    """
    Displays a view with details for a specific experiment.
    Exposes:
        "experiment" (the experiment model)
        "daily_data" (An array of dicts with:
            {"date",
             "activity_data": {
               "control_group_size",
               "control_group_score",
               "test_group_size",
               "test_group_score",
               "test_group_improvement",
               "confidence"
              },
              "conversion_data": {
                "test_group_size",
                "control_group_size",
                "goal_types": {
                  <goal-type-name>: {
                    "test_count",
                    "control_count",
                    "test_rate",
                    "control_rate",
                    "improvement",
                    "confidence"
                  }
                },
                "totals": {
                  "test_count",
                  "control_count",
                  "test_rate",
                  "control_rate",
                  "improvement",
                  "confidence"
                }
               }
             })

    """
    experiment = get_object_or_404(Experiment, name=experiment_name)

    daily_data = []

    start_date = experiment.start_date
    if experiment.start_date:
        if experiment.end_date:
            end_date = experiment.end_date
        else:
            end_date = date.today() - timedelta(days=1)
        current_date = end_date
        while current_date >= start_date:
            daily_activity_data = None
            daily_conversion_data = None
            activity_report = None
            conversion_report = None
            try:
                activity_report = DailyActivityReport.objects.get(experiment=experiment,
                                                                  date=current_date)
            except:
                l.warn("No activity report for date %s and experiment %s" %
                       (current_date, experiment.name))
            daily_conversion_data = get_conversion_data(experiment, current_date)
    
            if activity_report:
                improvement = None
    
                if activity_report.control_score > 0:
                    improvement = ((activity_report.test_score -
                                    activity_report.control_score) /
                                   activity_report.control_score) * 100
                daily_activity_data = {
                    "control_group_size": activity_report.control_group_size,
                    "control_group_score": activity_report.control_score,
                    "test_group_size": activity_report.test_group_size,
                    "test_group_score": activity_report.test_score,
                    "test_group_improvement": improvement,
                    "confidence": activity_report.confidence}
            daily_data.append({
                    "date": current_date,
                    "conversion_data": daily_conversion_data,
                    "activity_data": daily_activity_data})
            current_date = current_date - timedelta(1)
    context_var = {"experiment": experiment,
                   "daily_data": daily_data,
                   "experiment_states": experiment_states}

    return render_to_response(template_name, context_var,
                              context_instance=RequestContext(request))
