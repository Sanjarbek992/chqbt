from django.contrib import admin
from .models import MaterialBase, SchoolMaterialBase, Equipment, ClassroomEquipment

admin.site.register(MaterialBase)
admin.site.register(SchoolMaterialBase)
admin.site.register(Equipment)
admin.site.register(ClassroomEquipment)

# @admin.register(MaterialBase)
# class MaterialBaseAdmin(admin.ModelAdmin):
#     list_display = ("name",)
#     search_fields = ("name",)
#     ordering = ("name",)
#
#
# @admin.register(Equipment)
# class EquipmentAdmin(admin.ModelAdmin):
#     list_display = (
#         "name",
#         "standard_quantity",
#     )
#     search_fields = ("name",)
#     ordering = ("name",)
#
#
# @admin.register(ClassroomEquipment)
# class ClassroomEquipmentAdmin(admin.ModelAdmin):
#     list_display = (
#         "school",
#         "equipment",
#         "actual_quantity",
#         "get_standard",
#         "get_percentage",
#     )
#     search_fields = ("school__name", "equipment__name")
#     list_filter = ("school", "equipment")
#     ordering = ("school", "equipment")
#
#     def get_standard(self, obj):
#         return obj.equipment.standard_quantity
#
#     get_standard.short_description = "Norma (dona)"
#
#     def get_percentage(self, obj):
#         return f"{obj.percent_equipped()} %"
#
#     get_percentage.short_description = "Jihozlanish foizi"
#
#
# @admin.register(SchoolMaterialBase)
# class SchoolMaterialBaseAdmin(admin.ModelAdmin):
#     list_display = ("school", "material", "is_available")
#     list_filter = ("school", "material", "is_available")
#     search_fields = ("school__name", "material__name")
