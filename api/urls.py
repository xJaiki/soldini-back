from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.TransactionView import TransactionViewSet, total_summary, month_history, year_history, current_history, total_history, month_summary, year_summary, current_summary
from api.views.TagView import TagViewSet
from api.views.UserView import register, login

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router.urls)),
    # SECTION - auth
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    # SECTION - summary
    path('transactions/logic/summary/<int:month>/<int:year>', month_summary, name='month_summary'),
    path('transactions/logic/summary/<int:year>', year_summary, name='year_summary'),
    path('transactions/logic/summary/current', current_summary, name='current_summary'),
    path('transactions/logic/summary/total', total_summary, name='total_summary'),
    # SECTION - history
    path('transactions/logic/history/<int:month>/<int:year>', month_history, name='month_history'),
    path('transactions/logic/history/<int:year>', year_history, name='year_history'),
    path('transactions/logic/history/current', current_history, name='current_history'),
    path('transactions/logic/history/total', total_history, name='total_history'),
]