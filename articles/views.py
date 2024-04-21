from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
from.forms import ArticleForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST


def index(request):
	return render(request, "articles/index.html")

def articles(request):
	articles = Article.objects.all().order_by("-pk")
	context = {
		"articles" : articles,
	}
	return render(request, "articles/articles.html", context)

def article_detail(request, pk):
	article = get_object_or_404(Article, pk=pk)
	context = {"article" : article}

	return render(request, "articles/article_detail.html", context)

@login_required
def create(request):
  if request.method == "POST":
      form = ArticleForm(request.POST)
      if form.is_valid():
          article = form.save()
          return redirect("articles:article_detail", article.id)
  else:
      form = ArticleForm()

  context = {"form": form}
  return render(request, "articles/create.html", context)

@login_required
@require_http_methods(["GET", "POST"])
def update(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save()
            return redirect("articles:article_detail", article.pk)
    else:
        form = ArticleForm(instance=article)
    context = {
        "form": form,
        "article": article,
    }
    return render(request, "articles/update.html", context)

@require_POST
def delete(request, pk):
    if request.user.is_authenticated:
        article = get_object_or_404(Article, pk=pk)
        article.delete()
    return redirect("articles:articles")

def data_throw(request):
	return render(request, "articles/data_throw.html")

def data_catch(request):
	message = request.GET.get("message")
	context = {"message": message}
	return render(request, "articles/data_catch.html", context)