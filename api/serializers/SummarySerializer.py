from rest_framework import serializers

class SummarySerializer(serializers.Serializer):
    # general
    total_income = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    total_expense = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    net_balance = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    
    # tags
    most_expensive_tag = serializers.CharField(max_length=255, required=False)
    most_expensive_tag_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    most_used_tag = serializers.CharField(max_length=255, required=False)
    most_used_tag_count = serializers.IntegerField(required=False)
    
    # miscs
    most_expensive_month_and_year = serializers.CharField(max_length=255, required=False)
    most_expensive_month_and_year_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    most_expensive_year = serializers.IntegerField(required=False)
    most_expensive_year_amount = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
