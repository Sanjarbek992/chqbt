from django.db import models

class InventoryItem(models.Model):
    name = models.CharField(max_length=255, verbose_name='Vosita nomi')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Miqdori')
    def __str__(self):
        return f"{self.name} - {self.quantity} dona"
    class Meta:
        verbose_name = 'Vosita'
        verbose_name_plural = 'Vositalar'
        db_table = 'inventory_item'

