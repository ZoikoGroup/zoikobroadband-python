from rest_framework import serializers

from .models import FaultReport, FaultStatusHistory


class FaultStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FaultStatusHistory
        fields = (
            "status",
            "note",
            "created_at",
        )


class FaultReportSerializer(serializers.ModelSerializer):

    timeline = FaultStatusHistorySerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = FaultReport
        fields = "__all__"

        read_only_fields = (
            "id",
            "reference_number",
            "user",
            "status",
            "created_at",
            "updated_at",
            "timeline",
        )


class MyFaultSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )
    
    class Meta:
        model = FaultReport
        fields = (
            "id",
            "reference_number",
            "issue_type",
            "status",
            "status_display",
            "priority",
            "created_at",
        )


class FaultDetailSerializer(serializers.ModelSerializer):

    timeline = FaultStatusHistorySerializer(
        many=True,
        read_only=True
    )
    
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )

    class Meta:
        model = FaultReport
        fields = (
            "id",
            "reference_number",
            "issue_type",
            "status",
            "status_display",
            "priority",
            "problem_description",
            "created_at",
            "timeline",
        )