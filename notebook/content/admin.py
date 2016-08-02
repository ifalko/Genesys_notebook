from django.contrib import admin
from .models import RecordNotebook
# Register your models here.

class RecordNotebookAdminModel(admin.ModelAdmin):
	list_display = ["pk", "owner", "full_name", "phone_number", "birthday"]
	list_filter = ["owner"]
	search_fields = ["owner__username", "full_name", "phone_number"]
	class Meta():
		model = RecordNotebook


admin.site.register(RecordNotebook, RecordNotebookAdminModel)
