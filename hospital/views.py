from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import (
    User,
    Doctor,
    Patient,
    Department,
    Appointment,
    Prescription,
    Medicine,
    Bill,
)
from .serializers import (
    UserRegisterSerializer,
    UserSerializer,
    DoctorSerializer,
    PatientSerializer,
    DepartmentSerializer,
    AppointmentSerializer,
    PrescriptionSerializer,
    MedicineSerializer,
    BillSerializer,
)
from .permissions import IsAdmin, IsAdminOrReceptionist


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return UserSerializer
        return UserRegisterSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.select_related('user', 'department').all()
    serializer_class = DoctorSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['department', 'is_available']
    search_fields = [
        'user__first_name',
        'user__last_name',
        'specialization',
        'phone',
    ]

    @action(detail=False, methods=['get'])
    def available(self, request):
        doctors = self.get_queryset().filter(is_available=True)
        serializer = self.get_serializer(doctors, many=True)
        return Response(serializer.data)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.select_related('user').all()
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'user__first_name',
        'user__last_name',
        'phone',
        'blood_group',
    ]


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related(
        'patient',
        'patient__user',
        'doctor',
        'doctor__user',
        'doctor__department',
    ).all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['doctor', 'patient', 'appointment_date', 'status']

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset

        if user.role == 'doctor':
            return queryset.filter(doctor__user=user)

        if user.role == 'patient':
            return queryset.filter(patient__user=user)

        return queryset

    @action(detail=True, methods=['patch'])
    def cancel(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = 'cancelled'
        appointment.save()

        serializer = self.get_serializer(appointment)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def approve(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = 'approved'
        appointment.save()

        serializer = self.get_serializer(appointment)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'])
    def complete(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = 'completed'
        appointment.save()

        serializer = self.get_serializer(appointment)
        return Response(serializer.data)


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.select_related(
        'appointment',
        'appointment__patient',
        'appointment__patient__user',
        'appointment__doctor',
        'appointment__doctor__user',
    ).prefetch_related('medicines', 'medicines__medicine').all()
    serializer_class = PrescriptionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset

        if user.role == 'doctor':
            return queryset.filter(appointment__doctor__user=user)

        if user.role == 'patient':
            return queryset.filter(appointment__patient__user=user)

        return queryset


class MedicineViewSet(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'unit']


class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.select_related('patient', 'patient__user').all()
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['patient', 'paid']

    def get_queryset(self):
        user = self.request.user
        queryset = self.queryset

        if user.role == 'patient':
            return queryset.filter(patient__user=user)

        return queryset

    @action(detail=True, methods=['patch'])
    def mark_as_paid(self, request, pk=None):
        bill = self.get_object()
        bill.paid = True
        bill.save()

        serializer = self.get_serializer(bill)
        return Response(serializer.data)