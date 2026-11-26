from rest_framework import serializers
from .models import Skill, UserProfile


class SkillSerializer(serializers.ModelSerializer):
    instructor_username = serializers.CharField(source="instructor.username", read_only=True)
    discord_username = serializers.SerializerMethodField()

    class Meta:
        model = Skill
        fields = "__all__"

    def get_discord_username(self, obj):
        owner = obj.instructor or obj.user
        if not owner:
            return ""
        profile = UserProfile.objects.filter(user=owner).first()
        return profile.discord_username if profile else ""