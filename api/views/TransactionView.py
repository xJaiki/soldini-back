import datetime
from django.db.models import Sum, Count
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from api.models.TransactionModel import Transaction
from api.serializers.TransactionSerializer import TransactionSerializer
from api.serializers.SummarySerializer import SummarySerializer

class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        date = serializer.validated_data['date']
        if date == datetime.date(1,1,1):
            date = datetime.datetime.now().date()
        serializer.save(user=self.request.user, date=date)
 
    # path('transactions/logic/summary/<int:user>/<int:month>/<int:year>', month_summary, name='month_summary'),
    # path('transactions/logic/summary/<int:user>/<int:year>', year_summary, name='year_summary'),
    # path('transactions/logic/summary/<int:user>/current', current_summary, name='current_summary'),
    # path('transactions/logic/summary/<int:user>/total', total_summary, name='total_summary'),
    # path('transactions/logic/history/<int:user>/<int:month>/<int:year>', month_history, name='month_history'),
    # path('transactions/logic/history/<int:user>/<int:year>', year_history, name='year_history'),
    # path('transactions/logic/history/<int:user>/current', current_history, name='current_history'),
    # path('transactions/logic/history/<int:user>/total', total_history, name='total_history'),
    
@api_view(['GET'])
def total_history(request, user):
    if request.user.is_authenticated:
        transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def current_history(request, user):
    if request.user.is_authenticated:
        date = datetime.datetime.now()
        transactions = Transaction.objects.filter(user=request.user, date__month=date.month, date__year=date.year)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def month_history(request, user, month, year):
    if request.user.is_authenticated:
        transactions = Transaction.objects.filter(user=request.user, date__month=month, date__year=year)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def year_history(request, user, year):
    if request.user.is_authenticated:
        transactions = Transaction.objects.filter(user=request.user, date__year=year)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    # # general
    # total_income = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    # total_expense = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    # net_balance = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    # 
    # # tags
    # most_expensive_tag = serializers.CharField(max_length=255, required=False)
    # most_expensive_tag_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    # most_used_tag = serializers.CharField(max_length=255, required=False)
    # most_used_tag_count = serializers.IntegerField(required=False)
    # 
    # # miscs
    # most_expensive_month_and_year = serializers.CharField(max_length=255, required=False)
    # most_expensive_month_and_year_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    # most_expensive_year = serializers.IntegerField(required=False)
    # most_expensive_year_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    
@api_view(['GET'])
def total_summary(request):
    if request.user.is_authenticated:
        transactions = Transaction.objects.filter(user=request.user)
        summary_data = calculateSummaryData(transactions)
        
        serializer = SummarySerializer(summary_data)
        return Response(serializer.data)
    return Response({'error': 'Unauthorized'}, status=401)

@api_view(['GET'])
def current_summary(request):
    if request.user.is_authenticated:
        date = datetime.datetime.now()
        transactions = Transaction.objects.filter(user=request.user, date__month=date.month, date__year=date.year)
        summary_data = calculateSummaryData(transactions)
        
        serializer = SummarySerializer(summary_data)
        return Response(serializer.data)
    return Response({'error': 'Unauthorized'}, status=401)

@api_view(['GET'])
def month_summary(request, month, year):
    if request.user.is_authenticated:
        transactions = Transaction.objects.filter(user=request.user, date__month=month, date__year=year)
        summary_data = calculateSummaryData(transactions)
        
        serializer = SummarySerializer(summary_data)
        return Response(serializer.data)
    return Response({'error': 'Unauthorized'}, status=401)

@api_view(['GET'])
def year_summary(request, year):
    if request.user.is_authenticated:
        transactions = Transaction.objects.filter(user=request.user, date__year=year)
        summary_data = calculateSummaryData(transactions)
        
        serializer = SummarySerializer(summary_data)
        return Response(serializer.data)
    return Response({'error': 'Unauthorized'}, status=401)

def calculateSummaryData(transactions):
    #SECTION - general
    total_income = transactions.filter(transaction_type='IN').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = transactions.filter(transaction_type='OUT').aggregate(Sum('amount'))['amount__sum'] or 0
    net_balance = total_income - total_expense
        
    #SECTION - most expensive tag
    most_expensive_tag_dict = transactions.filter(transaction_type='OUT').values('tags__name').annotate(Sum('amount'))
    most_expensive_tag = most_expensive_tag_dict.order_by('-amount__sum').first() or {'tags__name': 'none', 'amount__sum': 0}
    most_expensive_tag_name = most_expensive_tag['tags__name']
    most_expensive_tag_amount = most_expensive_tag['amount__sum']
    #SECTION - most used tag
    most_used_tag_dict = transactions.values('tags__name').annotate(Count('tags__name'))
    most_used_tag = most_used_tag_dict.order_by('-tags__name__count').first() or {'tags__name': 'none', 'tags__name__count': 0}
    most_used_tag_name = most_used_tag['tags__name']
    most_used_tag_count = most_used_tag['tags__name__count']
        
    #SECTION - most expensive month
    most_expensive_month_and_year_dict = transactions.filter(transaction_type='OUT').values('date__month', 'date__year').annotate(Sum('amount'))
    most_expensive_month_and_year_first = most_expensive_month_and_year_dict.order_by('-amount__sum').first() or {'date__month': 0, 'date__year': 0, 'amount__sum': 0}
    most_expensive_month_and_year = f"{most_expensive_month_and_year_first['date__month']}/{most_expensive_month_and_year_first['date__year']}"
    most_expensive_month_and_year_amount = most_expensive_month_and_year_first['amount__sum']
    #SECTION - most expensive year
    most_expensive_year_dict = transactions.filter(transaction_type='OUT').values('date__year').annotate(Sum('amount'))
    most_expensive_year_first = most_expensive_year_dict.order_by('-amount__sum').first() or {'date__year': 0, 'amount__sum': 0}
    most_expensive_year = most_expensive_year_first['date__year']
    most_expensive_year_amount = most_expensive_year_first['amount__sum']
        
    summary_data = {
            'total_income': total_income,
            'total_expense': total_expense,
            'net_balance': net_balance,
            'most_expensive_tag': most_expensive_tag_name,
            'most_expensive_tag_amount': most_expensive_tag_amount,
            'most_used_tag': most_used_tag_name,
            'most_used_tag_count': most_used_tag_count,
            'most_expensive_month_and_year': most_expensive_month_and_year,
            'most_expensive_month_and_year_amount': most_expensive_month_and_year_amount,
            'most_expensive_year': most_expensive_year,
            'most_expensive_year_amount': most_expensive_year_amount
        }
    
    return summary_data