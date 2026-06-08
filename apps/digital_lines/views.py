from threading import Thread

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.core.mail import send_mail
from django.conf import settings

from .models import DigitalLineOrder
from .serializers import DigitalLineOrderSerializer


class DigitalLineOrderView(APIView):

    def send_admin_email(self, order):

        try:

            subject = f"New Digital Line Order #{order.id}"

            message = f"""
New Digital Line Order Received

Plan: {order.plan}

Duration: {order.duration}

Number Option: {order.number_option}

Number Sub Allocation: {order.number_sub_allocation}

Number Import: {order.number_import}

Equipment: {", ".join(order.equipment)}

Addons: {", ".join(order.addons)}

Charge Changes: {", ".join(order.charge_changes)}
"""

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )

            order.email_sent = True
            order.save(update_fields=["email_sent"])

        except Exception as e:
            print("Digital Line Email Error:", str(e))

    def post(self, request):

        serializer = DigitalLineOrderSerializer(data=request.data)

        if serializer.is_valid():

            order = serializer.save()

            Thread(
                target=self.send_admin_email,
                args=(order,),
                daemon=True,
            ).start()

            return Response(
                {
                    "success": True,
                    "message": "Order submitted successfully",
                    "order_id": order.id,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )