from django.shortcuts import render, redirect
from common.models import Comment
from core.cleanup import clean_up_files
from pets.forms.comment_form import CommentForm
from pets.forms.edit_form import EditForm
from pets.models import Pet, Like


# Create your views here.
def pets_list(req):
    context = {
        'pets': Pet.objects.all(),
    }
    return render(req, 'pet_list.html', context)


def pets_details_or_comment(req, pk):
    pet = Pet.objects.get(pk=pk)
    if req.method == 'GET':
        context = {
            'pet': pet,
            'form': CommentForm
        }
        return render(req, 'pet_detail.html', context)
    else:
        form = CommentForm(req.POST)
        if form.is_valid():
            comment = Comment(comment=form.cleaned_data['text'])
            comment.pet = pet
            comment.save()
            pet.comment_set.add(comment)
            pet.save()
            return redirect('pet details or comment', pk)
        context = {
            'pet': pet,
            'form': form
        }
        return render(req, 'pet_detail.html', context)


def pets_like(req, pk):
    pet = Pet.objects.get(pk=pk)
    like = Like(field=str(pk))
    like.pet = pet
    like.save()
    return redirect('pet list')


def pets_edit(req, pk):
    pet = Pet.objects.get(pk=pk)
    if req.method == 'GET':
        form = EditForm(instance=pet)
        context = {
            'form': form,
            'pet': pet,
        }
        return render(req, 'pet_edit.html', context)
    else:
        old_image = pet.image
        form = EditForm(req.POST, req.FILES, instance=pet)
        if form.is_valid():
            clean_up_files(old_image.path)
            form.save()
            return redirect('pet details or comment', pet.pk)
        context = {
            'form': form,
            'pet': pet,
        }
        return render(req, 'pet_edit.html', context)


def pets_delete(req, pk):
    pet = Pet.objects.get(pk=pk)
    if req.method == 'GET':
        context = {
            'pet': pet,
        }
        return render(req, 'pet_delete.html', context)
    else:
        pet.delete()
        return redirect('pet list')


def pets_create(req):
    pet = Pet()
    if req.method == 'GET':
        form = EditForm(instance=pet)
        context = {
            'form': form,
            'pet': pet,
        }
        return render(req, 'pet_create.html', context)
    else:
        form = EditForm(req.POST, req.FILES, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('pet details or comment', pet.pk)
        context = {
            'form': form,
            'pet': pet,
        }
        return render(req, 'pet_create.html', context)
