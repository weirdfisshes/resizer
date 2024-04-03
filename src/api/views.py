import hashlib

import rest_framework.views
import rest_framework.response
import rest_framework
import PIL.Image
import drf_yasg.utils
import rest_framework.parsers
import drf_yasg.openapi

import resizer.logs
from . import serializers
from . import utils
from . import models


class ImageAPI(rest_framework.views.APIView):
    """
    Класс API View для работы с изображениями
    """
    parser_classes = (rest_framework.parsers.MultiPartParser,)

    @drf_yasg.utils.swagger_auto_schema(
        operation_id='Resize image',
        request_body=serializers.ResizeImageInputSerializer,
        responses={
            rest_framework.status.HTTP_200_OK: drf_yasg.openapi.Response(
                description='Path to image',
                schema=serializers.ResizeImageOutputSerializer
            )
        }
    )
    def post(self, request):
        """
        Метод для сжатия изображений
        """
        serializer = serializers.ResizeImageInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file = request.FILES.get('file')
        width = serializer.data['width']
        height = serializer.data.get('height')

        resizer.logs.debug(
            'Got new resize request',
            filename=file.name, width=width, height=height
        )

        name, extension = utils.parse_filename(file.name)

        with PIL.Image.open(file) as image:
            # Высчитаем хэш картинки и попробуем найти картинку по хэшу в БД
            image_hash = hashlib.md5(image.tobytes()).hexdigest()
            resized_image = utils.get_resized_image_or_none(image_hash, width, height)

            # Если не удалось найти изображение (то есть ранее мы его не сжимали),
            # то сожмем изображение
            if resized_image is not None:
                result = {'resized_file_path': resized_image}
                serializer = serializers.ResizeImageOutputSerializer(result)

                return rest_framework.response.Response(
                    serializer.data, status=rest_framework.status.HTTP_200_OK
                )

            if height is None:
                height = utils.get_height(image.size, width)

            resized_image = image.resize((width, height))
            resized_file_path = utils.get_resized_file_path(
                name, extension, width, height
            )
            resized_image.save(resized_file_path)

        result = {'resized_file_path': resized_file_path}
        serializer = serializers.ResizeImageOutputSerializer(result)

        # Сохраним путь до сжатой картинки в БД
        models.Image.objects.filter(hash=image_hash).update(path=resized_file_path)

        resizer.logs.debug(
            'Successfully resized image',
            resized_file_path=resized_file_path
        )

        return rest_framework.response.Response(
            serializer.data, status=rest_framework.status.HTTP_200_OK
        )
