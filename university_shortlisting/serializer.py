from rest_framework import serializers

class UniversityShortlistInputSerializer(serializers.Serializer):
    cgpa = serializers.FloatField(min_value=0, max_value=4)
    current_college = serializers.CharField(max_length=255)
    current_country = serializers.CharField(max_length=100)
    destination_country = serializers.CharField(max_length=100)
    field_of_study = serializers.CharField(max_length=255, required=False, allow_blank=True)
    estimated_budget = serializers.IntegerField(min_value=0)

    def validate_cgpa(self, value):
        if value < 0 or value > 4:
            raise serializers.ValidationError("CGPA must be between 0 and 4.")
        return value

    def validate_estimated_budget(self, value):
        if value < 0:
            raise serializers.ValidationError("Estimated budget must be a positive integer.")
        return value