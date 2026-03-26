from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .selectors import dashboard_summary_for
from .serializers import RepairListSerializer
from .selectors import repairs_visible_to


class DashboardView(LoginRequiredMixin, View):
    template_name = 'repairs/dashboard.html'

    def get(self, request):
        return render(request, self.template_name, {'page_title': 'Dashboard'})


class RepairsApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        repairs = repairs_visible_to(request.user)[:50]
        serializer = RepairListSerializer(repairs, many=True)
        return Response({'results': serializer.data})


class DashboardSummaryApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(dashboard_summary_for(request.user))


class HealthcheckView(View):
    def get(self, request):
        return JsonResponse({'ok': True})
