from threading import Thread

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.mail import send_mail
from django.conf import settings

from .models import BusinessBroadbandInquiry
from .serializers import BusinessBroadbandInquirySerializer
import logging

logger = logging.getLogger(__name__)

def send_inquiry_email(inquiry):

    try:

        subject = "New Business Broadband Inquiry"

        message = f"""
New Business Inquiry Received

Business Name: {inquiry.business_name}

Contact Name: {inquiry.contact_name}

Email: {inquiry.email}

Phone Number: {inquiry.phone_number}

Business Postcode: {inquiry.business_postcode}

Business Size: {inquiry.business_size}

Additional Requirements:
{inquiry.additional_requirements}
"""

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )

        inquiry.email_sent = True
        inquiry.save()

        logger.info(f"Email sent for inquiry: {inquiry.business_name}")
        inquiry.email_status = 'sent'
        inquiry.email_error = ''
        inquiry.save()

    except Exception as e:
        logger.error(f"Error sending email for inquiry {inquiry.business_name}: {e}")

        inquiry.email_status = 'failed'
        inquiry.email_error = str(e)
        inquiry.save()


class BusinessBroadbandInquiryView(APIView):

    def post(self, request):

        serializer = BusinessBroadbandInquirySerializer(
            data=request.data
        )

        if serializer.is_valid():

            inquiry = serializer.save()

            # Run email sending in background thread
            Thread(
                target=send_inquiry_email,
                args=(inquiry,),
                daemon=True
            ).start()

            return Response(
                {
                    "success": True,
                    "message": "Inquiry submitted successfully"
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "success": False,
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )