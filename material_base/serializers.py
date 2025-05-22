from rest_framework import serializers
from .models import Equipment, ClassroomEquipment, MaterialBase, SchoolMaterialBase


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'name', 'standard_quantity']

class ClassroomEquipmentSerializer(serializers.ModelSerializer):
    equipment_name = serializers.CharField(source='equipment.name', read_only=True)
    standard_quantity = serializers.IntegerField(source='equipment.standard_quantity', read_only=True)
    percent_equipped = serializers.SerializerMethodField()

    class Meta:
        model = ClassroomEquipment
        fields = ['id', 'school', 'equipment', 'equipment_name', 'standard_quantity', 'actual_quantity', 'percent_equipped']

    def get_percent_equipped(self, obj):
        return obj.percent_equipped()


class MaterialBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialBase
        fields = ['id', 'name']

class SchoolMaterialBaseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='material.name', read_only=True)
    class Meta:
        model = SchoolMaterialBase
        fields = ['id', 'school', 'material', 'name', 'is_available']
