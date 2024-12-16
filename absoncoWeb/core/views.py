from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView
from .models import Item

# Create your views here.


def landing_page(request):
    if 'q' in request.GET:
        q = request.GET['q']
        item = Item.objects.filter(title__icontains=q)
    else:
        Item.objects.all()[:7]
            
    context = {
        'dispitems' : Item.objects.all()[:3],
        'Featured'  : Item.objects.all()[:8]
        
    }
    return render(request, "landing_page.html" ,context)

# def item_description(request,item_id):
#     item = get_object_or_404(Item, id=item_id) 
#     return render(request,"item_description.html",{"item": item})


def search_page(request):
    items = []  # Default to an empty list if no query is provided
    if 'q' in request.GET:
        q = request.GET['q']
        items = Item.objects.filter(title__icontains=q)
    
    else:
        Item.objects.all()[:7]
    
    # Debugging: print the query and the number of items found
    print(f"Search Query: {q}")
    print(f"Number of items found: {len(items)}")
    
    paginator = Paginator(items, 10) 
    page_number = request.GET.get('page')  
    page_obj = paginator.get_page(page_number)  
    context = {
        'items': items ,
        'page_obj' :page_obj
    }
    return render(request, "search_page.html", context)
    

class ItemDescriptionView(DetailView): 
    model = Item
    template_name = "item_description.html"
    context_object_name = "item"
    
    
    def get_object(self, queryset=None):
        item_slug = self.kwargs.get('item_slug')
        pk = self.kwargs.get('pk')
        # Retrieve the item based on item_name and pk
        item = get_object_or_404(Item, slug=item_slug, pk=pk)
        return item
    
from django.http import HttpResponseRedirect

def whatsapp_redirect(request):
    return HttpResponseRedirect("https://wa.me/233275650233")


def twitter_redirect(request):
    return HttpResponseRedirect("https://x.com/absonco")


def facebook_redirect(request):
    return HttpResponseRedirect("https://facebook.com/AbsoncoEnterprise")
