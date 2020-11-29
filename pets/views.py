from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.decorators import user_required
from common.models import Comment
from core.cleanup import clean_up_files
from pets.forms.comment_form import CommentForm
from pets.forms.edit_form import EditForm
from pets.models import Pet, Like


def pets_list(req):
    context = {
        'pets': Pet.objects.all(),
    }
    return render(req, 'pet_list.html', context)


@login_required
def pets_details_or_comment(req, pk):
    pet = Pet.objects.get(pk=pk)
    if req.method == 'GET':
        context = {
            'pet': pet,
            'form': CommentForm,
            'can_delete': req.user == pet.user.user,
            'can_edit': req.user == pet.user.user,
            'can_like': req.user != pet.user.user,
            'has_likes': pet.like_set.filter(user_id=req.user.userprofile.id).exists(),
            'can_comment': req.user != pet.user.user,
        }
        return render(req, 'pet_detail.html', context)
    else:
        form = CommentForm(req.POST)
        if form.is_valid():
            comment = Comment(comment=form.cleaned_data['text'])
            comment.pet = pet
            comment.user = req.user.userprofile
            comment.save()
            pet.comment_set.add(comment)
            return redirect('pet details or comment', pk)
        context = {
            'pet': pet,
            'form': form
        }
        return render(req, 'pet_detail.html', context)


@login_required
def pets_like(req, pk):
    like = Like.objects.filter(user_id=req.user.userprofile.id, pet_id=pk).first()
    if like:
        like.delete()
    else:
        pet = Pet.objects.get(pk=pk)
        like = Like(field=str(pk), user=req.user.userprofile)
        like.pet = pet
        like.save()
    return redirect('pet details or comment', pk)


@user_required(Pet)
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


@login_required
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


@login_required
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
