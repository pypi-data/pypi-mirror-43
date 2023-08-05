from rest_framework import serializers
from .models import Client
from .utils.auth import generate_api_key


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'api_key']

    api_key = serializers.CharField(read_only=True)

    def create(self, validated_data):
        raw_api_key = generate_api_key()

        if 'request' in self.context:
            self.context['api_key'] = raw_api_key

        return Client.objects.create(api_key=raw_api_key,
                                     name=validated_data['name'],
                                     )
