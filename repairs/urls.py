from django.urls import path

from .views import (
    DashboardSummaryApiView,
    DashboardView,
    HealthcheckView,
    MyWorkApiView,
    MyWorkView,
    RepairAssignApiView,
    RepairCommentsApiView,
    RepairCreateView,
    RepairDetailApiView,
    RepairDetailView,
    RepairExportCsvView,
    RepairHistoryApiView,
    RepairListView,
    RepairPriorityChangeApiView,
    RepairStatusChangeApiView,
    RepairUpdateView,
    RepairsApiView,
)

app_name = 'repairs'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('repairs/', RepairListView.as_view(), name='repair-list'),
    path('repairs/new/', RepairCreateView.as_view(), name='repair-create'),
    path('repairs/my-work/', MyWorkView.as_view(), name='my-work'),
    path('repairs/<int:pk>/', RepairDetailView.as_view(), name='repair-detail'),
    path('repairs/<int:pk>/edit/', RepairUpdateView.as_view(), name='repair-update'),
    path('health/', HealthcheckView.as_view(), name='health'),
    path('api/repairs/', RepairsApiView.as_view(), name='api-repairs'),
    path('api/repairs/export/', RepairExportCsvView.as_view(), name='api-repairs-export'),
    path('api/repairs/my-work/', MyWorkApiView.as_view(), name='api-my-work'),
    path('api/repairs/<int:pk>/', RepairDetailApiView.as_view(), name='api-repair-detail'),
    path('api/repairs/<int:pk>/assign/', RepairAssignApiView.as_view(), name='api-repair-assign'),
    path('api/repairs/<int:pk>/change-status/', RepairStatusChangeApiView.as_view(), name='api-repair-change-status'),
    path('api/repairs/<int:pk>/change-priority/', RepairPriorityChangeApiView.as_view(), name='api-repair-change-priority'),
    path('api/repairs/<int:pk>/comments/', RepairCommentsApiView.as_view(), name='api-repair-comments'),
    path('api/repairs/<int:pk>/history/', RepairHistoryApiView.as_view(), name='api-repair-history'),
    path('api/dashboard/summary/', DashboardSummaryApiView.as_view(), name='api-dashboard-summary'),
]
