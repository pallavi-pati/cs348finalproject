from django import forms
from django.utils import timezone
from .models import ToDoItem, ToDoList

class ToDoItemForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        fields = ['title', 'description', 'due_date', 'todo_list']
        widgets = {
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        input_formats = ['%Y-%m-%dT%H:%M']

    def __init__(self, *args, **kwargs):
        self.list_id = kwargs.pop('list_id', None)
        super(ToDoItemForm, self).__init__(*args, **kwargs)
        if self.list_id:
            self.fields['todo_list'].queryset = ToDoList.objects.filter(id=self.list_id)

    def clean(self):
        cleaned_data = super().clean()
        todo_list = ToDoList.objects.get(id=self.list_id)
        items = ToDoItem.objects.filter(todo_list=todo_list)
        due_date = cleaned_data.get('due_date')

        if due_date > timezone.now() + timezone.timedelta(days=10):
            raise forms.ValidationError("You cannot set the due date more than 10 days into the future.")

        # Checking if there are already existing items for the todo_list
        if items.exists():
            first_item = items.order_by('created_date').first()
            if first_item and due_date - first_item.created_date <= timezone.timedelta(days=10):
                return cleaned_data
            else:
                raise forms.ValidationError(
                    "You cannot add a task that is due 10 days after the first task created on " +
                    first_item.created_date.strftime('%m-%d-%Y')
                )
        else:
            return cleaned_data
