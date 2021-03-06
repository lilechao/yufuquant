from typing import Type

from core.mixins import ApiErrorsMixin
from django.utils import timezone
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from robots.serializers import RobotConfigSerializer
from rest_framework import serializers

from .models import Robot
from .serializers import RobotListSerializer, RobotRetrieveSerializer
from rest_framework.serializers import Serializer


class RobotStrategyParametersFieldsSerializer(Serializer):
    strategy_parameters_fields = serializers.JSONField(binary=True)


class RobotViewSet(
    ApiErrorsMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = RobotListSerializer
    permission_classes = [IsAdminUser]
    pagination_class = None
    action_serializer_map = {
        "retrieve": RobotRetrieveSerializer,
    }

    def get_queryset(self):
        return (
            Robot.objects.all()
            .select_related("credential__user", "credential__exchange", "asset_record")
            .order_by("-created_at")
        )

    def get_serializer_class(self) -> Type[BaseSerializer]:
        return self.action_serializer_map.get(
            self.action, super().get_serializer_class()
        )

    @action(
        methods=["GET"],
        detail=True,
        serializer_class=RobotConfigSerializer,
        permission_classes=[IsAdminUser],
        url_name="config",
        url_path="config",
    )
    def retrieve_config(self, request, *args, **kwargs) -> Response:
        robot = self.get_object()
        serializer = self.get_serializer(instance=robot)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=True,
        url_path="ping",
        permission_classes=[IsAdminUser],
    )
    def ping(self, request, *args, **kwargs) -> Response:
        robot = self.get_object()
        robot.ping_time = timezone.now()
        robot.save(update_fields=["ping_time"])
        return Response({"detail": "pong"}, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=True,
        url_path="strategy_parameters",
        url_name="strategy-parameters",
        permission_classes=[IsAdminUser],
        serializer_class=RobotStrategyParametersFieldsSerializer,
    )
    def update_strategy_parameters(self, request, *args, **kwargs) -> Response:
        robot = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        fields = serializer.validated_data["strategy_parameters_fields"]
        robot.strategy_parameters["fields"].update(fields)
        robot.save(update_fields=["strategy_parameters"])
        return Response({"detail": "ok"}, status=status.HTTP_200_OK)
