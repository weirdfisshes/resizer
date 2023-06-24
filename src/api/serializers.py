import rest_framework.serializers


class ResizeImageInputSerializer(rest_framework.serializers.Serializer):
    file = rest_framework.serializers.ImageField()
    width = rest_framework.serializers.IntegerField()
    height = rest_framework.serializers.IntegerField(required=False)


class ResizeImageOutputSerializer(rest_framework.serializers.Serializer):
    resized_file_path = rest_framework.serializers.FilePathField(path=None)
