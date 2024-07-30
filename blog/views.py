from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from django.views import View

from .forms import PostForm, UserRegistrationForm, ProfileForm, PostImageFormSet
from .models import Post, Category, Comment, Subscriber, Profile, Tag, PostImage
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.db.models import Q


def get_categories():
    all = Category.objects.all()
    count = all.count()
    half = count // 2
    first_half = all[:half]
    second_half = all[half:]
    return {'cats1': first_half, 'cats2': second_half}


def index(request):
    posts = Post.objects.all().order_by("-published_date")
    # posts = Post.objects.filter(content__icontains="lorem")
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, "blog/index.html", context)


def category(request, c=None):
    cObj = get_object_or_404(Category, name=c)
    posts = Post.objects.filter(category=cObj).order_by("-published_date")
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, "blog/index.html", context)


def post(request, name=None):
    post = get_object_or_404(Post, title=name)
    comments = post.comments.filter(parent__isnull=True).order_by('created_date')
    context = {'post': post, 'comments': comments}
    context.update(get_categories())
    return render(request, "blog/post.html", context)


def tag_posts(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    posts = tag.post_set.all().order_by("-published_date")
    context = {
        'tag': tag,
        'posts': posts,
    }
    context.update(get_categories())
    return render(request, 'blog/tag_posts.html', context)


def contact(request):
    email_exists = False
    if request.method == 'POST':
        sub_email = request.POST.get('sub_email')
        if sub_email:
            if not Subscriber.objects.filter(email=sub_email).exists():
                Subscriber.objects.create(email=sub_email)
            else:
                email_exists = True
    context = {
        'email_exists': email_exists,
    }
    context.update(get_categories())
    return render(request, "blog/contact.html", context)


def about(request):
    context = {}
    context.update(get_categories())
    return render(request, "blog/about.html", context)


def services(request):
    context = {}
    context.update(get_categories())
    return render(request, "blog/services.html", context)


def search(request):
    query = request.GET.get('query')
    posts = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query)).order_by('-published_date')
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, "blog/index.html", context)


@login_required
def create(request):
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        image_formset = PostImageFormSet(request.POST, request.FILES, queryset=PostImage.objects.none())

        if post_form.is_valid() and image_formset.is_valid():
            post = post_form.save(commit=False)
            post.published_date = now()
            post.user = request.user
            post.save()
            post_form.save_m2m()

            for form in image_formset:
                if form.cleaned_data.get('DELETE'):
                    continue
                if form.cleaned_data:
                    image = form.cleaned_data['image']
                    PostImage.objects.create(post=post, image=image)

            return redirect('blog:index')
    else:
        post_form = PostForm()
        image_formset = PostImageFormSet(queryset=PostImage.objects.none())

    context = {
        'post_form': post_form,
        'image_formset': image_formset,
    }
    context.update(get_categories())
    return render(request, "blog/create.html", context)


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if not (request.user == post.user or request.user.is_superuser):
        return HttpResponseForbidden("You are not allowed to delete this post.")

    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')

    context = {'post': post}
    context.update(get_categories())
    return render(request, 'blog/delete_confirm.html', context)


@login_required
def add_comment(request, post_id, parent_id=None):
    post = get_object_or_404(Post, id=post_id)
    parent_comment = None
    if parent_id:
        parent_comment = get_object_or_404(Comment, id=parent_id)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            author = request.user.username
            profile = Profile.objects.filter(user=request.user).first()
            avatar = profile.avatar.url if profile and profile.avatar else '/static/blog/images/avatar.jpg'
            Comment.objects.create(post=post, author=author, text=text, image=avatar, parent=parent_comment)
        return redirect('blog:post', name=post.title)
    return redirect('blog:post', name=post.title)


@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post_title = comment.post.title

    if not (request.user.username == comment.author or request.user.is_staff):
        return HttpResponseForbidden("You are not allowed to delete this comment.")

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post', name=post_title)

    return HttpResponseRedirect(reverse('blog:post', args=[post_title]))


class MyLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('blog:index')


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('blog:index')
        else:
            messages.error(request, 'Registration failed. Please correct the errors below.')
    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
    }
    context.update(get_categories())
    return render(request, 'blog/register.html', context)


@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)
    user = request.user

    num_comments = Comment.objects.filter(author=user.username).count()
    num_posts = Post.objects.filter(user=user).count()
    num_images = PostImage.objects.filter(post__user=user).count()
    days_on_site = (now() - user.date_joined).days
    registration_date = user.date_joined

    context = {
        'profile': profile,
        'num_comments': num_comments,
        'num_posts': num_posts,
        'num_images': num_images,
        'days_on_site': days_on_site,
        'registration_date': registration_date,
    }
    context.update(get_categories())
    return render(request, 'blog/profile.html', context)


@login_required
def update_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('blog:profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileForm(instance=profile)

    context = {
        'form': form,
    }
    context.update(get_categories())
    return render(request, 'blog/update_profile.html', context)
