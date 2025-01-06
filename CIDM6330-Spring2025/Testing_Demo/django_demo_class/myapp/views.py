from django.shortcuts import render, redirect, get_object_or_404
from .models import Item
from .forms import ItemForm


def home(request):
    items = Item.objects.all()
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = ItemForm()

    return render(request, "home.html", {"form": form, "items": items})


def item_list(request):
    items = Item.objects.all()
    return render(request, "item_list.html", {"items": items})


def edit_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect("item_list")
    else:
        form = ItemForm(instance=item)

    return render(request, "edit_item.html", {"form": form, "item": item})


def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    if request.method == "POST":
        item.delete()
        return redirect("item_list")
    return render(request, "confirm_delete.html", {"item": item})
