from django.db import transaction, IntegrityError
from django.db.models import Q
from rest_framework import serializers, exceptions

from boards.models import Board, BoardParticipant
from core.models import User


class BoardCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated", 'is_deleted')
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(user=user, board=board, role=BoardParticipant.Role.owner)
        return board


class BoardParticipantSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(required=True, choices=BoardParticipant.Role.choices[1:])
    user = serializers.SlugRelatedField(slug_field="username", queryset=User.objects.all())

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardSerializer(serializers.ModelSerializer):
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")

    # Yes, I know may look stranger than the provided one, but I wanted to write my own
    # (and I do think it's more efficient, at least for PATCH)
    def update(self, instance, validated_data):
        # changes to make patch work as intended
        new_participants = validated_data.get("participants") # if "participants" in validated_data else []
        new_by_id = {item['user'].id: item for item in new_participants} if new_participants else {}
        old_participants = instance.participants.exclude(role=BoardParticipant.Role.owner)


        # the front uses only PUT, but I want PATCH to work as well
        if not self.partial:
            with transaction.atomic():
                for old_p in old_participants:
                    if old_p.user_id not in new_by_id:
                        old_p.delete()

        old_ids = [item.user_id for item in old_participants]

        # not sure atomic is needed here, as only the owner can update, but if the PM wants it, let it be
        with transaction.atomic():
            for item_id, item_contents in new_by_id.items():
                try:
                    with transaction.atomic():
                        BoardParticipant.objects.create(
                            board=instance, user=item_contents["user"], role=item_contents["role"]
                        )
                except IntegrityError:
                    old_participants[old_ids.index(item_id)].role = item_contents["role"]
                    old_participants[old_ids.index(item_id)].save()

            if title := validated_data.get("title"):
                instance.title = title
                instance.save()

        return instance

    # This is the provided code.
    # Keeping it here for possible future use and reference

    # def updateX(self, instance, validated_data):
    #     owner = validated_data.pop("user")
    #     new_participants = validated_data.pop("participants")
    #     new_by_id = {part["user"].id: part for part in new_participants}
    #
    #     old_participants = instance.participants.exclude(user=owner)
    #     with transaction.atomic():
    #         for old_participant in old_participants:
    #             if old_participant.user_id not in new_by_id:
    #                 old_participant.delete()
    #             else:
    #                 if (
    #                         old_participant.role
    #                         != new_by_id[old_participant.user_id]["role"]
    #                 ):
    #                     old_participant.role = new_by_id[old_participant.user_id][
    #                         "role"
    #                     ]
    #                     old_participant.save()
    #                 new_by_id.pop(old_participant.user_id)
    #         for new_part in new_by_id.values():
    #             BoardParticipant.objects.create(
    #                 board=instance, user=new_part["user"], role=new_part["role"]
    #             )
    #
    #         if title := validated_data.get("title"):
    #             instance.title = title
    #             instance.save()
    #
    #     return instance


class BoardListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = "__all__"
