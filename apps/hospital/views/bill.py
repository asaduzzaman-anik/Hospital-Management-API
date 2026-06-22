from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.hospital.models import Bill
from apps.hospital.serializers import BillSerializer


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
        return Response(self.get_serializer(bill).data)