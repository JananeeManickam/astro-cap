from django.shortcuts import render
from django.views import View

class PicturesHome(View):
    """
    This view renders the home page with options for 'Planets', 'Telescopes', and 'Others'.
    """
    def get(self, request):
        return render(request, "pictures_home.html")
