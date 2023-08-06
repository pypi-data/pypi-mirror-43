from edc_subject_model_wrappers import (
    AppointmentModelWrapper as BaseAppointmentModelWrapper,
)

from .subject_visit_model_wrapper import SubjectVisitModelWrapper


class AppointmentModelWrapper(BaseAppointmentModelWrapper):

    visit_model_wrapper_cls = SubjectVisitModelWrapper
