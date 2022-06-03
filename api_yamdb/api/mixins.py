from rest_framework import mixins, viewsets
from rest_framework.exceptions import MethodNotAllowed


class CreateListRetrievDeletePatchViewSet(mixins.CreateModelMixin,
                                          mixins.UpdateModelMixin,
                                          mixins.ListModelMixin,
                                          mixins.RetrieveModelMixin,
                                          mixins.DestroyModelMixin,
                                          viewsets.GenericViewSet):
    def update(self, *args, **kwargs):
        raise MethodNotAllowed("PUT", detail="Use PATCH")

    def partial_update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs, partial=True)


class NoRetriveUpdateViewSet(mixins.CreateModelMixin,
                             mixins.DestroyModelMixin,
                             mixins.ListModelMixin,
                             viewsets.GenericViewSet):
    pass
