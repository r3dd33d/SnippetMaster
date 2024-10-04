from rest_framework import serializers
from .models import Snippet
from django.contrib.auth.models import User


class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    # The 'owner' field will display the username of the user who owns the Snippet.
    owner = serializers.ReadOnlyField(source='owner.username')

    # The 'highlight' field will provide a link to the highlighted version of the Snippet in HTML format.
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

    class Meta:
        model = Snippet
        # The fields included in the serialized representation of the Snippet.
        fields = ['url', 'id', 'highlight', 'owner', 'title', 'code', 'linenos', 'language', 'style']

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # The 'snippets' field will provide a hyperlink to the Snippets associated with each user.
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        # The fields included in the serialized representation of the User.
        fields = ['url', 'id', 'username', 'snippets']
