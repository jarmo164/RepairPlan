import csv
import json
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .forms import RepairCommentForm, RepairCreateForm, RepairUpdateForm
from .models import Department, Repair
from .permissions import (
    DashboardAccessMixin,
    RepairApiPermission,
    can_assign_repairs,
    can_change_priority,
    can_change_status,
    can_create_repairs,
    get_repair_action_flags,
    is_administrator,
    is_department_manager,
    is_repair_master,
    is_repairer,
)
from .selectors import (
    dashboard_high_priority_open_repairs_for,
    dashboard_oldest_open_repairs_for,
    dashboard_repair_counts_by_repairer,
    dashboard_summary_for,
    dashboard_unassigned_repairs_for,
    repair_list_summary_for,
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
from .services import add_comment, assign_repair, change_priority, change_status, create_repair, update_repair


def build_navigation_context(user):
    is_dept_manager = is_department_manager(user)
    is_master = is_repair_master(user)
    is_rep = is_repairer(user)
    is_admin = is_administrator(user)
    if is_admin:
        role_label = 'Administraator'
        role_intro = 'Halda süsteemi, vaata koormust ja kasuta admin-paneeli.'
        role_theme = 'role-admin'
    elif is_master:
        role_label = 'Paranduse meister'
        role_intro = 'Juhi tööde jaotust, prioriteete ja tööseisu.'
        role_theme = 'role-master'
    elif is_rep:
        role_label = 'Parandaja'
        role_intro = 'Keskendu oma tööjärjekorrale ja järgmisele tegevusele.'
        role_theme = 'role-repairer'
    elif is_dept_manager:
        role_label = 'Osakonna juht'
        role_intro = 'Lisa uusi parandusi ja jälgi oma osakonna kirjeid.'
        role_theme = 'role-manager'
    else:
        role_label = 'Kasutaja'
        role_intro = 'Kasuta süsteemi vastavalt oma õigustele.'
        role_theme = 'role-generic'

    return {
        'is_department_manager': is_dept_manager,
        'is_repair_master': is_master,
        'is_repairer': is_rep,
        'is_administrator': is_admin,
        'can_create_repairs': can_create_repairs(user),
        'role_label': role_label,
        'role_intro': role_intro,
        'role_theme': role_theme,
        'show_admin_link': is_admin or getattr(user, 'is_superuser', False),
    }


class HomeRedirectView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.is_superuser or request.user.groups.filter(name__in=['repair_master', 'administrator']).exists():
            return redirect('repairs:dashboard')
        if request.user.groups.filter(name='repairer').exists():
            return redirect('repairs:my-work')
        return redirect('repairs:repair-list')


class DashboardView(DashboardAccessMixin, View):
    template_name = 'repairs/dashboard.html'

    def get(self, request):
        return render(request, self.template_name, {'page_title': 'Dashboard', 'nav_key': 'dashboard', **build_navigation_context(request.user)})


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
            'list_summary': repair_list_summary_for(request.user),
            'nav_key': 'repair-list',
            **build_navigation_context(request.user),
        }
        return render(request, self.template_name, context)


class MyWorkView(LoginRequiredMixin, View):
    template_name = 'repairs/my_work.html'

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                'page_title': 'Minu tööd',
                'status_choices_json': json.dumps(list(Repair.Status.choices)),
                'nav_key': 'my-work',
                'nav_key': 'repair-list',
                **build_navigation_context(request.user),
            },
        )


class RepairCreateView(LoginRequiredMixin, View):
    template_name = 'repairs/repair_form.html'

    def get(self, request):
        if not can_create_repairs(request.user):
            messages.error(request, 'Sul puudub õigus parandusi luua.')
            return redirect('repairs:repair-list')
        return render(request, self.template_name, {'form': RepairCreateForm(), 'page_title': 'Uus parandus', 'mode': 'create', 'nav_key': 'repair-create', **build_navigation_context(request.user)})

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
        return render(request, self.template_name, {'form': form, 'page_title': 'Uus parandus', 'mode': 'create', 'nav_key': 'repair-create', **build_navigation_context(request.user)})


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
                'action_flags': get_repair_action_flags(request.user, repair),
                'status_choices_json': json.dumps(list(Repair.Status.choices)),
                'priority_choices_json': json.dumps(list(Repair.Priority.choices)),
                'assignee_choices_json': json.dumps(
                    [
                        {'id': user.id, 'label': user.get_username()}
                        for user in get_user_model().objects.filter(is_active=True).order_by('username')
                    ]
                ),
                'nav_key': 'repair-list',
                **build_navigation_context(request.user),
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
        return render(request, self.template_name, {'form': form, 'page_title': f'Muuda parandust #{repair.pk}', 'mode': 'update', 'repair': repair, 'nav_key': 'repair-list', **build_navigation_context(request.user)})

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
        return render(request, self.template_name, {'form': form, 'page_title': f'Muuda parandust #{repair.pk}', 'mode': 'update', 'repair': repair, 'nav_key': 'repair-list', **build_navigation_context(request.user)})


class RepairExportCsvView(LoginRequiredMixin, View):
    def get(self, request):
        queryset = filter_repairs_for_user(request.user, request.GET)
        response = HttpResponse(content_type='text/csv; charset=utf-8')
        response['Content-Disposition'] = 'attachment; filename="repairplan-repairs.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Tootekood', 'Kogus', 'Klient/grupp', 'Osakond', 'Staatus', 'Prioriteet', 'Parandaja', 'Loodud'])
        for repair in queryset:
            writer.writerow([
                repair.id,
                repair.product_code,
                repair.quantity,
                repair.client_or_group,
                repair.department.name,
                repair.get_status_display(),
                repair.get_priority_display(),
                repair.assigned_to.username if repair.assigned_to else '',
                repair.created_at.isoformat(),
            ])
        return response


class RepairsApiView(APIView):
    permission_classes = [RepairApiPermission]

    def get(self, request):
        queryset = filter_repairs_for_user(request.user, request.query_params)
        paginator = Paginator(queryset.only('id', 'product_code', 'quantity', 'client_or_group', 'created_at', 'updated_at', 'priority', 'status', 'department__name', 'created_by__username', 'assigned_to__username').select_related('department', 'created_by', 'assigned_to'), per_page=10)
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
        try:
            comment = add_comment(repair=repair, author=request.user, comment=serializer.validated_data['comment'])
        except ValidationError as exc:
            return Response({'detail': exc.message}, status=status.HTTP_403_FORBIDDEN)
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
        high_priority_open = RepairListSerializer(dashboard_high_priority_open_repairs_for(request.user), many=True).data
        unassigned_open = RepairListSerializer(dashboard_unassigned_repairs_for(request.user), many=True).data
        return Response(
            {
                **dashboard_summary_for(request.user),
                'oldest_open': oldest,
                'high_priority_open': high_priority_open,
                'unassigned_open': unassigned_open,
                'by_repairer': dashboard_repair_counts_by_repairer(request.user),
            }
        )


class HealthcheckView(View):
    def get(self, request):
        return JsonResponse({'ok': True})
