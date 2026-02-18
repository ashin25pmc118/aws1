from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Photo, Profile, Comment
from .forms import PhotoForm, UserUpdateForm, ProfileUpdateForm, CustomUserCreationForm, CommentForm

def home(request):
    photos = Photo.objects.all().order_by('-created_at')
    return render(request, 'gallery/home.html', {'photos': photos})

@login_required
def my_gallery(request):
    photos = Photo.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'gallery/my_gallery.html', {'photos': photos})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        profile, created = Profile.objects.get_or_create(user=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('my_gallery')
    else:
        profile, created = Profile.objects.get_or_create(user=request.user)
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'gallery/edit_profile.html', context)

def signup(request):
    if request.method == 'POST':
        u_form = CustomUserCreationForm(request.POST)
        p_form = ProfileUpdateForm(request.POST, request.FILES)
        if u_form.is_valid() and p_form.is_valid():
            user = u_form.save()
            # Profile created by signal, now update it with form data
            user.profile.image = p_form.cleaned_data.get('image')
            user.profile.save()
            login(request, user)
            return redirect('home')
    else:
        u_form = CustomUserCreationForm()
        p_form = ProfileUpdateForm()
    return render(request, 'registration/signup.html', {'u_form': u_form, 'p_form': p_form})

@login_required
def photo_upload(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            return redirect('home')
    else:
        form = PhotoForm()
    return render(request, 'gallery/photo_upload.html', {'form': form})

def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'gallery/photo_detail.html', {'photo': photo})

@login_required
def photo_edit(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if photo.user != request.user:
        return redirect('photo_detail', pk=pk)
    
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            return redirect('photo_detail', pk=pk)
    else:
        form = PhotoForm(instance=photo)
    return render(request, 'gallery/photo_form.html', {'form': form, 'action': 'Edit'})

@login_required
def photo_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if photo.user != request.user:
        return redirect('photo_detail', pk=pk)
    
    if request.method == 'POST':
        photo.delete()
        return redirect('home')
    return render(request, 'gallery/photo_confirm_delete.html', {'photo': photo})

@login_required
def like_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.user in photo.likes.all():
        photo.likes.remove(request.user)
    else:
        photo.likes.add(request.user)
    return redirect('home')

@login_required
def add_comment(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.photo = photo
            comment.user = request.user
            comment.save()
            return redirect('photo_detail', pk=pk)
    return redirect('photo_detail', pk=pk)

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    photo_pk = comment.photo.pk
    if request.user == comment.user or request.user == comment.photo.user:
        comment.delete()
    return redirect('photo_detail', pk=photo_pk)
