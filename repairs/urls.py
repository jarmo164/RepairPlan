from django.urls import path

from .views import DashboardSummaryApiView, DashboardView, HealthcheckView, RepairListView, RepairsApiView

app_name = 'repairs'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('repairs/', RepairListView.as_view(), name='repair-list'),
    path('health/', HealthcheckView.as_view(), name='health'),
    path('api/repairs/', RepairsApiView.as_view(), name='api-repairs'),
    path('api/dashboard/summary/', DashboardSummaryApiView.as_view(), name='api-dashboard-summary'),
]
