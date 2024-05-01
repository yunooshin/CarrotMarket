from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

def users(request):
	return render(request, "users/users.html")

def profile(request, username):
	member = get_object_or_404(get_user_model(), username=username)
	context = {
		"member": member,
	}
	return render(request, "users/profile.html", context)

@require_POST
def follow(request, user_pk):
    if request.user.is_authenticated:
        member = get_object_or_404(get_user_model(), pk=user_pk)
        if request.user != member:
            if request.user in member.followers.all():
                member.followers.remove(request.user)
            else:
                member.followers.add(request.user)
        return redirect("users:profile", member.username)
    return redirect("accounts:login")