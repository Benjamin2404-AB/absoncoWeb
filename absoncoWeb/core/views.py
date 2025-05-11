from datetime import timedelta
from django.utils import timezone 
import json
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView
from .models import Item, Order, OrderItem

# Create your views here.



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Item

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Item
import json
    

from django.http import HttpResponseRedirect

def landing_page(request):
    # Get current time and time 1 week ago
    now = timezone.now()
    one_week_ago = now - timedelta(days=7)

    # Fetch 2 most recently added items
    recently_added = Item.objects.order_by('-time_added')[:2]

    # Fetch 2 most recently updated items (within the last week)
    recently_updated = Item.objects.filter(
        time_updated__gte=one_week_ago
    ).exclude(
        id__in=[item.id for item in recently_added]  # Exclude items already in recently_added
    ).order_by('-time_updated')[:2]

    # Combine the items for Top Picks (max 4 items)
    top_picks = list(recently_added) + list(recently_updated)
    top_picks = top_picks[:4]  # Ensure we don't exceed 4 items

    # Fetch Featured items (you can keep your existing logic for this)
    featured_items = Item.objects.order_by('?')[:8]  # Example: random 8 items for Featured

    context = {
        'dispitems': top_picks,  # Top Picks (recently added + updated)
        'Featured': featured_items,
    }
    return render(request, 'landing_page.html', context)


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
    

# class ItemDescriptionView(DetailView): 
#     model = Item
#     template_name = "item_description.html"
#     context_object_name = "item"
    
    
#     def get_object(self, queryset=None):
#         item_slug = self.kwargs.get('item_slug')
#         pk = self.kwargs.get('pk')
#         # Retrieve the item based on item_name and pk
#         item = get_object_or_404(Item, slug=item_slug, pk=pk)
#         return item
    
class ItemDescriptionView(DetailView):
    model = Item
    template_name = 'core/item_description.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        public_id = self.kwargs.get('public_id')
        return get_object_or_404(Item, pk=pk, slug=public_id)



def instagram_redirect(request):
    return HttpResponseRedirect("https://instagram.com/absonco_enterprise")


def whatsapp_redirect(request):
    return HttpResponseRedirect("https://wa.me/233275650233")


def twitter_redirect(request):
    return HttpResponseRedirect("https://x.com/absonco")


def facebook_redirect(request):
    return HttpResponseRedirect("https://facebook.com/AbsoncoEnterprise")


@csrf_exempt  # Remove in production; use CSRF properly
@login_required
def add_to_cart(request):
    if request.method == 'POST':
        try:
            # Parse request body
            data = json.loads(request.body)
            item_id = data.get('item_id')
            quantity = int(data.get('quantity', 1))

            # Validate quantity
            if quantity < 1:
                return JsonResponse({
                    "success": False,
                    "message": "Quantity must be at least 1."
                }, status=400)

            # Get the item
            item = get_object_or_404(Item, id=item_id)

            # Get or create the user's active cart
            order, created = Order.objects.get_or_create(
                user=request.user,
                ordered=False,
                defaults={'start_date': timezone.now()}
            )

            # Check if the item already exists in the cart
            order_item = order.items.filter(item=item).first()
            if order_item:
                # Update quantity if item exists
                order_item.quantity += quantity
                order_item.save()
            else:
                # Create a new OrderItem
                order_item = OrderItem.objects.create(
                    item=item,
                    quantity=quantity
                )
                order.items.add(order_item)

            # Calculate total items
            total_items = order.get_total_items()

            # Prepare item details for response
            item_details = {
                "id": item.id,
                "title": item.title,
                "price": float(item.price),
                "image_url": item.image.url if item.image else '',
                "quantity": quantity,
                "total_items": total_items
            }

            return JsonResponse({
                "success": True,
                "message": "Item added to cart!",
                "item": item_details,
                "total_items": total_items
            })

        except json.JSONDecodeError:
            return JsonResponse({
                "success": False,
                "message": "Invalid JSON data."
            }, status=400)
        except Item.DoesNotExist:
            return JsonResponse({
                "success": False,
                "message": "Item not found."
            }, status=404)
        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": f"An error occurred: {str(e)}"
            }, status=500)

    return JsonResponse({
        "success": False,
        "message": "Invalid request method."
    }, status=405)

@csrf_exempt  # For testing purposes, handle CSRF properly in production
@login_required
def remove_from_cart(request):
    if request.method == 'POST':
        # Get item ID from the request body
        data = json.loads(request.body)
        item_id = data.get('item_id')

        # Get the item from the database
        item = get_object_or_404(Item, id=item_id)

        # Get the user's active cart
        order = get_object_or_404(Order, user=request.user, ordered=False)

        # Find the OrderItem in the cart
        order_item = order.items.filter(item__id=item_id).first()
        if order_item:
            order.items.remove(order_item)
            order_item.delete()  # Clean up the OrderItem

        # Calculate total items and total price
        total_items = order.get_total_items()
        total_price = order.get_total_price()

        return JsonResponse({
            "success": True,
            "message": f"Item '{item.title}' removed from cart.",
            "total_items": total_items,
            "total_price": float(total_price)
        })

    return JsonResponse({"success": False, "message": "Invalid request."})



from django.shortcuts import render
# from .models import Item
@login_required
def cart_view(request):
    if not request.user.is_authenticated:
        # Handle anonymous users (optional: use session-based cart)
        cart_items = []
        total_items = 0
    else:
        # Get the user's active cart
        try:
            order = Order.objects.get(user=request.user, ordered=False)
            cart_items = [
                {
                    'item': order_item.item,
                    'quantity': order_item.quantity,
                    'total_price': order_item.get_total_price()
                }
                for order_item in order.items.all()
            ]
            total_items = order.get_total_items()
        except Order.DoesNotExist:
            cart_items = []
            total_items = 0

    return render(request, 'cart_view.html', {
        'cart_items': cart_items,
        'total_items': total_items,
    })


# Update Cart Quantity View (New Endpoint)
@csrf_exempt
def update_cart_quantity(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        new_quantity = int(data.get('quantity', 1))

        # Validate quantity
        if new_quantity < 1:
            return JsonResponse({
                "success": False,
                "message": "Quantity must be at least 1.",
                "current_quantity": 1
            })

        # Get the item from the database
        item = get_object_or_404(Item, id=item_id)

        # Get the user's active cart
        order = get_object_or_404(Order, user=request.user, ordered=False)

        # Find the OrderItem in the cart
        order_item = order.items.filter(item__id=item_id).first()
        if not order_item:
            return JsonResponse({
                "success": False,
                "message": "Item not found in cart.",
                "current_quantity": 0
            })

        # Update the quantity
        order_item.quantity = new_quantity
        order_item.save()

        # Calculate totals
        total_items = order.get_total_items()
        total_price = order.get_total_price()
        item_total = order_item.get_total_price()

        return JsonResponse({
            "success": True,
            "message": f"Quantity updated for item '{item.title}'.",
            "total_items": total_items,
            "total_price": float(total_price),
            "item_total": float(item_total),
            "current_quantity": new_quantity
        })

    return JsonResponse({"success": False, "message": "Invalid request."})