from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.shortcuts import redirect
from django.utils import timezone
from .models import ToDoItem, ToDoList
from .forms import ToDoItemForm

class ListListView(ListView):
    model = ToDoList
    template_name = "todo_app/index.html"

class ItemListView(ListView):
    model = ToDoItem
    template_name = "todo_app/todo_list.html"

    def get_queryset(self):
        return ToDoItem.objects.filter(todo_list_id=self.kwargs["list_id"])

    def get_context_data(self):
        context = super().get_context_data()
        context["todo_list"] = ToDoList.objects.get(id=self.kwargs["list_id"])
        return context

class ListCreate(CreateView):
    model = ToDoList
    fields = ["title"]

    def get_context_data(self):
        context = super(ListCreate, self).get_context_data()
        context["title"] = "Add a new list"
        return context


class ItemCreate(CreateView):
    model = ToDoItem
    form_class = ToDoItemForm # custom form

    def get_form_kwargs(self):
        kwargs = super(ItemCreate, self).get_form_kwargs()
        kwargs['list_id'] = self.kwargs['list_id']
        return kwargs

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])

    def get_initial(self):
        initial_data = super(ItemCreate, self).get_initial()
        initial_data['todo_list'] = ToDoList.objects.get(id=self.kwargs['list_id'])
        return initial_data

    def get_context_data(self, **kwargs):
        context = super(ItemCreate, self).get_context_data(**kwargs)
        context['todo_list'] = ToDoList.objects.get(id=self.kwargs['list_id'])
        context['title'] = "Create a new task"
        return context

class ItemUpdate(UpdateView):
    model = ToDoItem
    form_class = ToDoItemForm  # Use your custom form for the fields
    template_name = "todo_app/todoitem_form.html"

    def get_object(self, queryset=None):
        list_id = self.kwargs.get('list_id')
        pk = self.kwargs.get('pk')
        item = get_object_or_404(ToDoItem, pk=pk, todo_list_id=list_id)
        return item

    def get_context_data(self, **kwargs):
        context = super(ItemUpdate, self).get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        context["title"] = "Edit task"
        return context

    def get_success_url(self):
        return reverse("list", args=[self.object.todo_list_id])

    def get_form_kwargs(self):
        kwargs = super(ItemUpdate, self).get_form_kwargs()
        kwargs['list_id'] = self.kwargs['list_id']
        return kwargs

class ListDelete(DeleteView):
    model = ToDoList
    success_url = reverse_lazy("index") #reverse_lazy() because urls are not loaded when the file is imported

class ItemDelete(DeleteView):
    model = ToDoItem

    def get_success_url(self):
        return reverse_lazy("list", args=[self.kwargs["list_id"]])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["todo_list"] = self.object.todo_list
        return context