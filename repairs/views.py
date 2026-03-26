from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import RepairCommentForm, RepairCreateForm, RepairUpdateForm
from .models import Department, Repair
from .permissions import DashboardAccessMixin, RepairApiPermission
from .selectors import (
    dashboard_oldest_open_repairs_for,
    dashboard_summary_for,
    filter_repairs_for_user,
    repairs_visible_to,
)
from .serializers import RepairDetailSerializer, RepairListSerializer


class DashboardView(DashboardAccessMixin, View):
    template_name = 'repairs/dashboard.html'

    def get(self, request):
        return render(request, self.template_name, {'page_title': 'Dashboard'})


class RepairListView(LoginRequiredMixin, View):
    template_name = 'repairs/repair_list.html'

    def get(self, request):
        context = {
            'page_title': 'Parandused',
            'departments': Department.objects.filter(is_active=True),
            'status_choices': Repair.Status.choices,
            'priority_choices': Repair.Priority.choices,
            'search': request.GET.get('search', ''),
            'filters': request.GET,
        }
        return render(request, self.template_name, context)


class RepairsApiView(APIView):
    permission_classes = [RepairApiPermission]

    def get(self, request):
        queryset = filter_repairs_for_user(request.user, request.query_params)
        paginator = Paginator(queryset, per_page=10)
        page_number = request.query_params.get('page', 1)
        page_obj = paginator.get_page(page_number)
        serializer = RepairListSerializer(page_obj.object_list, many=True)
        return Response({
            'results': serializer.data,
            'pagination': {
                'page': page_obj.number,
                'pages': paginator.num_pages,
                'count': paginator.count,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
            },
        })


class DashboardSummaryApiView(APIView):
    permission_classes = [RepairApiPermission]

    def get(self, request):
        oldest = RepairListSerializer(dashboard_oldest_open_repairs_for(request.user), many=True).data
        return Response({**dashboard_summary_for(request.user), 'oldest_open': oldest})


class HealthcheckView(View):
    def get(self, request):
        return JsonResponse({'ok': True})
