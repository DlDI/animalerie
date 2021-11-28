from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Animal, Equipement


# Create your views here.
def animal_list(request):
    animals = Animal.objects.filter()
    equipements = Equipement.objects.filter()
    return render(request, 'animalerie/animal_list.html', {'animals': animals, 'equipements': equipements})


def animal_detail(request, id_animal, self=None):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
    lieu = animal.lieu
    form = MoveForm(request.POST, instance=animal)
    if form.is_valid():
        form.save(commit=False)
        if animal.lieu.disponibilite == "libre":
            ancien_lieu.disponibilite = "libre"
            ancien_lieu.save()
            form.save(commit=False)
            nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
            if nouveau_lieu.id_equip != "litière":
                nouveau_lieu.disponibilite = "occupé"
            nouveau_lieu.save()
            lieu_id = nouveau_lieu.id_equip
            animal.etat = change_etat(lieu_id)
            form.save()
            return redirect('animal_detail', id_animal=id_animal)
        else :
            animal.lieu = ancien_lieu
            animal.save()
            return render(request,
                          'animalerie/animal_detail.html',
                          {'animal': animal, 'lieu': animal.lieu, 'form': form,
                           'message': "le lieu indiqué n'est pas disponible"})
    else:
        form = MoveForm()
        return render(request,
                  'animalerie/animal_detail.html',
                  {'animal': animal, 'lieu': lieu, 'form': form,  'message' : 'indiquer un lieu'})


def change_etat(animal):
    a=""
    if animal == "mangeoire":
        a = "repus"
    elif animal == "roue":
        a = "fatigué"
    elif animal == "nid":
        a = "endormi"
    else :
        a = "affamé"

    return a