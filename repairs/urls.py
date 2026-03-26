from django.urls import path

from .views import (
    DashboardSummaryApiView,
    DashboardView,
    HealthcheckView,
    RepairCommentsApiView,
    RepairCreateView,
    RepairDetailApiView,
    RepairDetailView,
    RepairHistoryApiView,
    RepairListView,
    RepairsApiView,
)

app_name = 'repairs'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('repairs/', RepairListView.as_view(), name='repair-list'),
    path('repairs/new/', RepairCreateView.as_view(), name='repair-create'),
    path('repairs/<int:pk>/', RepairDetailView.as_view(), name='repair-detail'),
    path('health/', HealthcheckView.as_view(), name='health'),
    path('api/repairs/', RepairsApiView.as_view(), name='api-repairs'),
    path('api/repairs/<int:pk>/', RepairDetailApiView.as_view(), name='api-repair-detail'),
    path('api/repairs/<int:pk>/comments/', RepairCommentsApiView.as_view(), name='api-repair-comments'),
    path('api/repairs/<int:pk>/history/', RepairHistoryApiView.as_view(), name='api-repair-history'),
    path('api/dashboard/summary/', DashboardSummaryApiView.as_view(), name='api-dashboard-summary'),
]
