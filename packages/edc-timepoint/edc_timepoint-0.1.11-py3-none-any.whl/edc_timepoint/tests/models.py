from django.db import models
from django.db.models.deletion import PROTECT
from edc_model.models import BaseUuidModel
from edc_utils import get_utcnow
from edc_visit_tracking.model_mixins import VisitModelMixin

from ..model_mixins import TimepointLookupModelMixin
from ..timepoint_lookup import TimepointLookup


class VisitTimepointLookup(TimepointLookup):
    timepoint_model = "edc_appointment.appointment"
    timepoint_related_model_lookup = "appointment"


class CrfTimepointLookup(TimepointLookup):
    timepoint_model = "edc_appointment.appointment"


class SubjectVisit(VisitModelMixin, TimepointLookupModelMixin, BaseUuidModel):

    timepoint_lookup_cls = VisitTimepointLookup

    class Meta(VisitModelMixin.Meta):
        pass


class CrfOne(TimepointLookupModelMixin, BaseUuidModel):

    timepoint_lookup_cls = CrfTimepointLookup

    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT)

    report_datetime = models.DateTimeField(default=get_utcnow)


class CrfTwo(TimepointLookupModelMixin, BaseUuidModel):

    timepoint_lookup_cls = CrfTimepointLookup

    subject_visit = models.ForeignKey(SubjectVisit, on_delete=PROTECT)

    report_datetime = models.DateTimeField(default=get_utcnow)
