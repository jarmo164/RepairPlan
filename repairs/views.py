import json
from django.contrib import messages
from django.contrib.auth import get_user_model
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
from .models import Department, Repair, RepairComment
from .permissions import (
    DashboardAccessMixin,
    RepairApiPermission,
    can_assign_repairs,
    can_change_priority,
    can_change_status,
    can_create_repairs,
)
from .selectors import (
    dashboard_oldest_open_repairs_for,
    dashboard_summary_for,
    filter_repairs_for_user,
    my_work_for,
    repairs_visible_to,
)
from .serializers import (
    RepairAssignSerializer,
    RepairCommentSerializer,
    RepairCreateSerializer,
    RepairDetailSerializer,
    RepairListSerializer,
    RepairPriorityChangeSerializer,
    RepairStatusChangeSerializer,
    RepairStatusLogSerializer,
    RepairUpdateSerializer,
)
from .services import assign_repair, change_priority, change_status, create_repair, update_repair


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


class MyWorkView(LoginRequiredMixin, View):
    template_name = 'repairs/my_work.html'

    def get(self, request):
        return render(request, self.template_name, {'page_title': 'Minu tööd', 'status_choices_json': json.dumps(list(Repair.Status.choices))})


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


class RepairUpdateView(LoginRequiredMixin, View):
    template_name = 'repairs/repair_form.html'

    def get_form(self, request, repair):
        form = RepairUpdateForm(instance=repair)
        if not can_assign_repairs(request.user):
            form.fields['assigned_to'].disabled = True
        if not can_change_priority(request.user):
            form.fields['priority'].disabled = True
        if not can_change_status(request.user, own_assigned_only=repair.assigned_to_id == request.user.id):
            form.fields['status'].disabled = True
        return form

    def get(self, request, pk):
        repair = get_object_or_404(repairs_visible_to(request.user), pk=pk)
        form = self.get_form(request, repair)
        return render(request, self.template_name, {'form': form, 'page_title': f'Muuda parandust #{repair.pk}', 'mode': 'update', 'repair': repair})

    def post(self, request, pk):
        repair = get_object_or_404(repairs_visible_to(request.user), pk=pk)
        form = RepairUpdateForm(request.POST, instance=repair)
        if form.is_valid():
            try:
                update_repair(repair=repair, changed_by=request.user, **form.cleaned_data)
                messages.success(request, f'Parandus #{repair.id} uuendatud.')
                return redirect('repairs:repair-detail', pk=repair.pk)
            except ValidationError as exc:
                form.add_error(None, exc.message)
        return render(request, self.template_name, {'form': form, 'page_title': f'Muuda parandust #{repair.pk}', 'mode': 'update', 'repair': repair})


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


class MyWorkApiView(APIView):
    permission_classes = [RepairApiPermission]

    def get(self, request):
        serializer = RepairListSerializer(my_work_for(request.user), many=True)
        return Response({'results': serializer.data})


class RepairDetailApiView(APIView):
    permission_classes = [RepairApiPermission]

    def get_object(self, request, pk):
        return get_object_or_404(repairs_visible_to(request.user), pk=pk)

    def get(self, request, pk):
        repair = self.get_object(request, pk)
        return Response(RepairDetailSerializer(repair).data)

    def patch(self, request, pk):
        repair = self.get_object(request, pk)
        serializer = RepairUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        try:
            repair = update_repair(repair=repair, changed_by=request.user, **serializer.validated_data)
        except ValidationError as exc:
            return Response({'detail': exc.message}, status=status.HTTP_403_FORBIDDEN)
        return Response(RepairDetailSerializer(repair).data)


class RepairAssignApiView(APIView):
    permission_classes = [RepairApiPermission]

    def post(self, request, pk):
        repair = get_object_or_404(repairs_visible_to(request.user), pk=pk)
        serializer = RepairAssignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        assigned_to = None
        assigned_to_id = serializer.validated_data.get('assigned_to')
        if assigned_to_id:
            assigned_to = get_object_or_404(get_user_model(), pk=assigned_to_id)
        try:
            assign_repair(repair=repair, assigned_to=assigned_to, changed_by=request.user)
        except ValidationError as exc:
            return Response({'detail': exc.message}, status=status.HTTP_403_FORBIDDEN)
        repair.refresh_from_db()
        return Response(RepairDetailSerializer(repair).data)


class RepairStatusChangeApiView(APIView):
    permission_classes = [RepairApiPermission]

    def post(self, request, pk):
        repair = get_object_or_404(repairs_visible_to(request.user), pk=pk)
        serializer = RepairStatusChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            change_status(repair=repair, status=serializer.validated_data['status'], changed_by=request.user)
        except ValidationError as exc:
            return Response({'detail': exc.message}, status=status.HTTP_403_FORBIDDEN)
        repair.refresh_from_db()
        return Response(RepairDetailSerializer(repair).data)


class RepairPriorityChangeApiView(APIView):
    permission_classes = [RepairApiPermission]

    def post(self, request, pk):
        repair = get_object_or_404(repairs_visible_to(request.user), pk=pk)
        serializer = RepairPriorityChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            change_priority(repair=repair, priority=serializer.validated_data['priority'], changed_by=request.user)
        except ValidationError as exc:
            return Response({'detail': exc.message}, status=status.HTTP_403_FORBIDDEN)
        repair.refresh_from_db()
        return Response(RepairDetailSerializer(repair).data)


class RepairCommentsApiView(APIView):
    permission_classes = [RepairApiPermission]

    def get(self, request, pk):
        repair = get_object_or_404(repairs_visible_to(request.user), pk=pk)
        return Response({'results': RepairCommentSerializer(repair.comments.select_related('author'), many=True).data})

    def post(self, request, pk):
        repair = get_object_or_404(repairs_visible_to(request.user), pk=pk)
        serializer = RepairCommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = RepairComment.objects.create(repair=repair, author=request.user, comment=serializer.validated_data['comment'])
        return Response(RepairCommentSerializer(comment).data, status=status.HTTP_201_CREATED)


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
