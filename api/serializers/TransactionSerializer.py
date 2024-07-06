from rest_framework import serializers
from api.models.TransactionModel import Transaction
from api.models.TagModel import Tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']
        
class TransactionSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'date', 'amount', 'transaction_type', 'description', 'tags']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        transaction = Transaction.objects.create(**validated_data)
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_data['name'], user=transaction.user)
            transaction.tags.add(tag)
        return transaction

    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags')
        instance.amount = validated_data.get('amount', instance.amount)
        instance.transaction_type = validated_data.get('transaction_type', instance.transaction_type)
        instance.description = validated_data.get('description', instance.description)
        instance.date = validated_data.get('date', instance.date)
        instance.save()

        instance.tags.clear()
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_data['name'], user=instance.user)
            instance.tags.add(tag)

        return instance
