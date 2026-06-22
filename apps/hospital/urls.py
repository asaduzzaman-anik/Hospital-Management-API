from rest_framework.routers import DefaultRouter

from .views import (
    DepartmentViewSet,
    DoctorViewSet,
    PatientViewSet,
    AppointmentViewSet,
    MedicineViewSet,
    PrescriptionViewSet,
    BillViewSet,
)


router = DefaultRouter()

router.register('departments', DepartmentViewSet, basename='departments')
router.register('doctors', DoctorViewSet, basename='doctors')
router.register('patients', PatientViewSet, basename='patients')
router.register('appointments', AppointmentViewSet, basename='appointments')
router.register('medicines', MedicineViewSet, basename='medicines')
router.register('prescriptions', PrescriptionViewSet, basename='prescriptions')
router.register('bills', BillViewSet, basename='bills')

urlpatterns = router.urls