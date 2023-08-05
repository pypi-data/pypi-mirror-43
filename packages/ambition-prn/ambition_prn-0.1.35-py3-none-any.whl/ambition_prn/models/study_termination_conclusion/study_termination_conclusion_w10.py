from django.db import models
from edc_action_item.managers import (
    ActionIdentifierSiteManager,
    ActionIdentifierManager,
)
from edc_action_item.models import ActionModelMixin
from edc_identifier.model_mixins import TrackingModelMixin
from edc_model.models import BaseUuidModel
from edc_model.validators import date_not_future
from edc_visit_schedule.model_mixins import OffScheduleModelMixin

from ...constants import STUDY_TERMINATION_CONCLUSION_ACTION_W10
from ...choices import REASON_STUDY_TERMINATED_W10


class StudyTerminationConclusionW10(
    OffScheduleModelMixin, ActionModelMixin, TrackingModelMixin, BaseUuidModel
):

    action_name = STUDY_TERMINATION_CONCLUSION_ACTION_W10

    tracking_identifier_prefix = "ST"

    subject_identifier = models.CharField(max_length=50, unique=True)

    last_study_fu_date = models.DateField(
        verbose_name="Date of last research follow up (if different):",
        validators=[date_not_future],
        blank=True,
        null=True,
    )

    termination_reason = models.CharField(
        verbose_name="Reason for study termination",
        max_length=75,
        choices=REASON_STUDY_TERMINATED_W10,
        help_text=("If included in error, be sure to fill in protocol deviation form."),
    )

    death_date = models.DateField(
        verbose_name="Date of Death",
        validators=[date_not_future],
        blank=True,
        null=True,
    )

    consent_withdrawal_reason = models.CharField(
        verbose_name="Reason for withdrawing consent",
        max_length=75,
        blank=True,
        null=True,
    )

    on_site = ActionIdentifierSiteManager()

    objects = ActionIdentifierManager()

    def natural_key(self):
        return (self.action_identifier,)

    class Meta:
        verbose_name = "W10 Study Termination/Conclusion"
        verbose_name_plural = "W10 Study Terminations/Conclusions"
