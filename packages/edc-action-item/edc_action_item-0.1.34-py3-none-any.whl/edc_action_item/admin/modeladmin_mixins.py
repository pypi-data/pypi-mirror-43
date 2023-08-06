from django_revision.modeladmin_mixin import ModelAdminRevisionMixin

from edc_model_admin import (
    ModelAdminNextUrlRedirectMixin,
    ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin,
    ModelAdminAuditFieldsMixin,
    ModelAdminInstitutionMixin,
    ModelAdminRedirectOnDeleteMixin,
)


class ModelAdminMixin(
    ModelAdminNextUrlRedirectMixin,
    ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin,
    ModelAdminRevisionMixin,
    ModelAdminAuditFieldsMixin,
    ModelAdminInstitutionMixin,
    ModelAdminRedirectOnDeleteMixin,
):

    list_per_page = 10
    date_hierarchy = "modified"
    empty_value_display = "-"
