from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import RepairCommentForm, RepairCreateForm, RepairUpdateForm
from .models import Department, Repair
from .permissions import DashboardAccessMixin, RepairApiPermission, can_create_repairs
from .selectors import (
    dashboard_oldest_open_repairs_for,
    dashboard_summary_for,
    filter_repairs_for_user,
    repairs_visible_to,
)
from .serializers import (
    RepairCommentSerializer,
    RepairCreateSerializer,
    RepairDetailSerializer,
    RepairListSerializer,
    RepairStatusLogSerializer,
)
from .services import create_repair


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


class RepairCreateView(LoginRequiredMixin, View):
    template_name = 'repairs/repair_form.html'

    def get(self, request):
        if not can_create_repairs(request.user):
            messages.error(request, 'Sul puudub õigus parandusi luua.')
            return redirect('repairs:repair-list')
        return render(request, self.template_name, {'form': RepairCreateForm(), 'page_title': 'Uus parandus', 'mode': 'create'})

    def post(self, request):
        if not can_create_repairs(request.user):
            messages.error(request, 'Sul puudub õigus parandusi luua.')
            return redirect('repairs:repair-list')
        form = RepairCreateForm(request.POST)
        if form.is_valid():
            try:
                repair = create_repair(created_by=request.user, **form.cleaned_data)
                messages.success(request, f'Parandus #{repair.id} loodud.')
                return redirect('repairs:repair-detail', pk=repair.pk)
            except ValidationError as exc:
                form.add_error(None, exc.message)
        return render(request, self.template_name, {'form': form, 'page_title': 'Uus parandus', 'mode': 'create'})


class RepairDetailView(LoginRequiredMixin, View):
    template_name = 'repairs/repair_detail.html'

    def get(self, request, pk):
        repair = get_object_or_404(repairs_visible_to(request.user), pk=pk)
        return render(
            request,
            self.template_name,
            {
                'page_title': f'Parandus #{repair.pk}',
                'repair': repair,
                'comment_form': RepairCommentForm(),
            },
        )


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

    def post(self, request):
        serializer = RepairCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            repair = create_repair(created_by=request.user, **serializer.validated_data)
        except ValidationError as exc:
            return Response({'detail': exc.message}, status=status.HTTP_403_FORBIDDEN)
        return Response(RepairDetailSerializer(repair).data, status=status.HTTP_201_CREATED)


class RepairDetailApiView(APIView):
    permission_classes = [RepairApiPermission]

    def get(self, request, pk):
        repair = get_object_or_404(repairs_visible_to(request.user), pk=pk)
        return Response(RepairDetailSerializer(repair).data)


class RepairCommentsApiView(APIView):
    permission_classes = [RepairApiPermission]

    def get(self, request, pk):
        repair = get_object_or_404(repairs_visible_to(request.user), pk=pk)
        return Response({'results': RepairCommentSerializer(repair.comments.select_related('author'), many=True).data})


class RepairHistoryApiView(APIView):
    permission_classes = [RepairApiPermission]

    def get(self, request, pk):
        repair = get_object_or_404(repairs_visible_to(request.user), pk=pk)
        return Response({'results': RepairStatusLogSerializer(repair.status_logs.select_related('changed_by'), many=True).data})


class DashboardSummaryApiView(APIView):
    permission_classes = [RepairApiPermission]

    def get(self, request):
        oldest = RepairListSerializer(dashboard_oldest_open_repairs_for(request.user), many=True).data
        return Response({**dashboard_summary_for(request.user), 'oldest_open': oldest})


class HealthcheckView(View):
    def get(self, request):
        return JsonResponse({'ok': True})
