from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.serializers import Serializer

# from rest_access_policy import AccessViewSetMixin

# todo (optional) add AccessViewSetMixin from rest_access_policy
class CustomModelViewSet(ModelViewSet):
    """Custom ModelViewSet class:
    - provides an extra endpoint 'meta' which provides serialized metadata for the resource.
        Note that the meta endpoint is used in combination with the CustomMetadata class.
        defined under config.metadata and has been wired in the backend via the DEFAULT_METADATA_CLASS
        setting.

    - Allows for dynamic selection of serializer class based on action.
        * If the action is 'list', and a list_serializer_class is found, it will be used.
        * If the action is 'retrieve', and a retrieve_serializer_class is found, it will be used.
        * If the custom action is 'choices', and a choices_serializer_class is found, it will be used.
        * If the action is 'detail', and a detail_serializer_class is found, it will be used.
     """
    list_serializer_class: Serializer = None # Set as serializer specifically for the list action.
    retrieve_serializer_class: Serializer = None # Set as serializer specifically for the retrieve action.
    readonly_serializer_class: Serializer = None # Serve as a detail view for a single object for read-only purposes.
    choices_serializer_class: Serializer = None # Set as serializer specifically for the choices action.

    def get_serializer_class(self):
        if self.action == 'list' and self.list_serializer_class is not None:
            return self.list_serializer_class
        elif self.action == 'retrieve' and self.retrieve_serializer_class is not None:
            return self.retrieve_serializer_class
        elif self.action == 'choices' and self.choices_serializer_class is not None:
            return self.choices_serializer_class
        elif self.action == 'readonly' and self.readonly_serializer_class is not None:
            return self.readonly_serializer_class
        else:
            assert self.serializer_class is not None, (
                    "'%s' should either include a `serializer_class` attribute, "
                    "or override the `get_serializer_class()` method."
                    % self.__class__.__name__
            )
            return self.serializer_class

    @action(methods=['GET'], detail=False)
    def meta(self, request):
        """This view action fetches field metadata for the resource.
        See also https://www.django-rest-framework.org/api-guide/metadata/
        """
        meta = self.metadata_class()
        serializer = self.get_serializer()
        data = {
            'fields': meta.get_serializer_info(serializer),
            'fieldsets': getattr(serializer.Meta, 'fieldsets', {}),
        }
        return Response(data)

    @action(methods=['GET'], detail=False)
    def choices(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=True)
    def readonly(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(data=serializer.data, status=200)



