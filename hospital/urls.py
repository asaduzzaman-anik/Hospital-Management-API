from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    RegisterViewSet,
    DepartmentViewSet,
    DoctorViewSet,
    PatientViewSet,
    AppointmentViewSet,
    PrescriptionViewSet,
    MedicineViewSet,
    BillViewSet,
)


router = DefaultRouter()

router.register('users', RegisterViewSet, basename='users')
router.register('departments', DepartmentViewSet, basename='departments')
router.register('doctors', DoctorViewSet, basename='doctors')
router.register('patients', PatientViewSet, basename='patients')
router.register('appointments', AppointmentViewSet, basename='appointments')
router.register('prescriptions', PrescriptionViewSet, basename='prescriptions')
router.register('medicines', MedicineViewSet, basename='medicines')
router.register('bills', BillViewSet, basename='bills')


urlpatterns = [
    path('', include(router.urls)),
]