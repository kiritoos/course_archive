from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count, Avg, Q
from .forms import WorkForm
from .models import Work, Discipline, Keyword
from .services import get_discipline_stats

def index(request):
    works = Work.objects.select_related("discipline", "author").prefetch_related("keywords")[:50]
    return render(request, "archive/work_list.html", {"works": works})

def work_create(request):
    if request.method == "POST":
        form = WorkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("archive:index")
    else:
        form = WorkForm()
    return render(request, "archive/work_form.html", {"form": form, "title": "Новая работа"})

def work_update(request, pk):
    work = get_object_or_404(Work, pk=pk)
    if request.method == "POST":
        form = WorkForm(request.POST, instance=work)
        if form.is_valid():
            form.save()
            return redirect("archive:index")
    else:
        form = WorkForm(instance=work)
    return render(request, "archive/work_form.html", {"form": form, "title": "Редактирование"})

def work_delete(request, pk):
    work = get_object_or_404(Work, pk=pk)
    if request.method == "POST":
        work.delete()
        return redirect("archive:index")
    return render(request, "archive/work_confirm_delete.html", {"work": work})

def search(request):
    works = Work.objects.select_related("discipline", "author").prefetch_related("keywords")
    query = request.GET.get("q")
    year = request.GET.get("year")
    supervisor = request.GET.get("supervisor")
    
    if query:
        works = works.filter(keywords__name__icontains=query)
    if year:
        works = works.filter(year=year)
    if supervisor:
        works = works.filter(supervisor__icontains=supervisor)
        
    works = works.distinct()[:100]
    return render(request, "archive/search.html", {"works": works})

def stats(request):
    disciplines = get_discipline_stats()
    return render(request, "archive/stats.html", {"disciplines": disciplines})