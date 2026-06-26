from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import (
    FaultReport,
    FaultStatusHistory,
)

from .serializers import (
    FaultReportSerializer,
    MyFaultSerializer,
    FaultDetailSerializer,
)


class FaultReportView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = FaultReportSerializer(data=request.data)

        if serializer.is_valid():

            fault = serializer.save(
                user=request.user
            )

            FaultStatusHistory.objects.create(
                fault=fault,
                status=fault.status,
                note="Fault report submitted successfully.",
                updated_by=request.user,
            )

            return Response(
                {
                    "success": True,
                    "message": "Fault reported successfully.",
                    "data": FaultReportSerializer(fault).data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {
                "success": False,
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class MyFaultsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        faults = FaultReport.objects.filter(
            user=request.user
        ).order_by("-created_at")

        serializer = MyFaultSerializer(
            faults,
            many=True
        )

        return Response(
            {
                "success": True,
                "data": serializer.data,
            }
        )
        
# class FaultDetailView(RetrieveAPIView):

#     permission_classes = [IsAuthenticated]

#     serializer_class = FaultDetailSerializer

#     lookup_field = "id"

#     def get_queryset(self):

#         return FaultReport.objects.filter(
#             user=self.request.user
#         )

class FaultDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        fault = get_object_or_404(
            FaultReport,
            id=id,
            user=request.user
        )

        serializer = FaultDetailSerializer(fault)

        return Response(
            {
                "success": True,
                "data": serializer.data,
            }
        )