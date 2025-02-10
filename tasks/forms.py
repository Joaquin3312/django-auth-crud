from django.forms import ModelForm
from .models import Task

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','important','completed']
        # se puede personalizar con la propiedad "widget = "