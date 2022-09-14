
from datetime import datetime
from django.http import HttpResponseNotAllowed, HttpResponsePermanentRedirect, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Max,Min,Count,Avg,F,When,Case
from .models import Item, CartItems, Reviews
from django.contrib import messages
from django.core.mail import EmailMessage
from accounts.models import Enquiry, Profile
import sweetify
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .decorators import *
from django.db.models import Sum

def subcategory(request):
    supcategory=SuperCategory.objects.all()
    context = {
        'supcategory' : supcategory,
        # 'reviews' : reviews,
    }
    return render(request, 'main/layout.html', context)

def index(request):
    if request.method == "POST":
            name = request.POST.get('name')
            email = request.POST.get('email')
            firm = request.POST.get('firm')
            register = Enquiry(name=name, email=email, firm=firm, date=datetime.today())
            register.save()
    supcategory=SuperCategory.objects.all()
    subcategory = SubCategory.objects.all()[:10]
    menu_items = Item.objects.all()
    area_items=''
    try:
        profile = Profile.objects.filter(user=request.user,)
        pin = profile.values_list('pincode', flat=True)
    # pincode=[]
        for x in pin:
            print(x)
            # pincode.append(x)
        area_items = Item.objects.filter(type=x)
        print(area_items)
    except:
        pass    
   
    context = {
    'supcategory' : supcategory,
        'menu_items' : menu_items,
        'subcategory':subcategory,
        'area_items':area_items,
            }
    return render(request, 'main/home.html', context)
# class MenuListView(ListView):
#     supcategory=SuperCategory.objects.all()
#     model = Item
#     template_name = 'main/home.html'
#     context_object_name = 'menu_items'

def subCategory(request, slug):
    total_data=Item.objects.count()
    data=Item.objects.all().order_by('-id')[:3]
    min_price=ProductAttribute.objects.aggregate(Min('price'))
    max_price=ProductAttribute.objects.aggregate(Max('price'))
    supcategory=SuperCategory.objects.all()
    subcategory = SubCategory.objects.filter(slug=slug).order_by('-id')[:7] 
    reviews = Reviews.objects.filter(rslug=slug).order_by('-id')[:7] 
    menu_items = Item.objects.all()
    context = {
        'subcategory' : subcategory,
        'reviews' : reviews,
        'supcategory' : supcategory,
        'menu_items' : menu_items,
        			'data':data,
			'total_data':total_data,
			'min_price':min_price,
			'max_price':max_price,
    }
    return render(request, 'main/subcategory.html', context)
def category(request,slug):
    supcategory=SuperCategory.objects.all()
    category = Category.objects.filter(slug=slug).order_by('-id')[:7] 
    reviews = Reviews.objects.filter(rslug=slug).order_by('-id')[:7] 
    menu_items = Item.objects.all()
    context = {
        'category' : category,
        'reviews' : reviews,
        'menu_items' : menu_items,
        'supcategory' : supcategory,
    }
    return render(request, 'main/category.html', context)
def supcategory(request,slug):
    supcategory=SuperCategory.objects.all()
    spcategory = SuperCategory.objects.filter(slug=slug).order_by('-id')[:7] 
    reviews = Reviews.objects.filter(rslug=slug).order_by('-id')[:7] 
    menu_items = Item.objects.all()
    context = {
        'spcategory' : spcategory,
        'menu_items' : menu_items,
        'reviews' : reviews,
        'supcategory' : supcategory,
    }
    return render(request, 'main/supercategory.html', context)

def menuDetail(request, slug):
    supcategory=SuperCategory.objects.all()
   
    item = Item.objects.filter(slug=slug).first()
    
            
    reviews = Reviews.objects.filter(rslug=slug).order_by('-id')[:7] 
    context = {
        'supcategory' : supcategory,
        'item' : item,
        'reviews' : reviews,
        }
    return render(request, 'main/product.html', context)

@login_required
def add_reviews(request):
    if request.method == "POST":
        user = request.user
        rslug = request.POST.get("rslug")
        item = Item.objects.get(slug=rslug)
        review = request.POST.get("review")

        reviews = Reviews(user=user, item=item, review=review, rslug=rslug)
        reviews.save()
        messages.success(request, "Thank You for Reviewing this Item!!")
    return redirect(f"/product/{item.slug}")

class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    fields = ['category', 'subcategory',  'title',  'image', 'description', 'price', 'moq', 'instructions', 'ships_from', 'delivered_within', 'labels' ]
    query_pk_and_slug = True

    def form_valid(self, form):
        form.instance.sold_by = self.request.user
        return super().form_valid(form)

class ItemUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Item
    fields = ['category', 'subcategory',  'title',  'image', 'description', 'price', 'moq', 'instructions', 'ships_from', 'delivered_within', 'labels' ]

    def form_valid(self, form):
        form.instance.sold_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        item = self.get_object()
        if self.request.user == item.sold_by:
            return True
        return False

class ItemDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Item
    success_url = '/item_list'

    def test_func(self):
        item = self.get_object()
        if self.request.user == item.sold_by:
            return True
        return False

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    profile = Profile.objects.filter(user=request.user,)
    add = profile.values_list('addresses', flat=True)
    pin = profile.values_list('pincode', flat=True)
    phone = profile.values_list('phone', flat=True)
    
    cart_item = CartItems.objects.create(
        item=item,
        user=request.user,
        addresses=add,
        pincode=pin,
        phone=phone,
        ordered=False,
    )
    
    messages.info(request, "Added to Cart!!Continue Shopping!!")
    return redirect("main:cart")

@login_required
def get_cart_items(request):
 
    supcategory=SuperCategory.objects.all()
    cart_items = CartItems.objects.filter(user=request.user,ordered=False)
    # accept_items = CartItems.objects.filter(status=Accepted)
    bill = cart_items.aggregate(total=Sum('item__price')*Sum('quantity'))
    number = cart_items.aggregate(Sum('quantity'))
    profile = Profile.objects.filter(user=request.user,)
    add = profile.values_list('addresses', flat=True)
    # address = profile.get('addresses')
    # print(add)
    
    
    # pieces = cart_items.aggregate(Sum('item__pieces'))
    total = bill.get("item__price__sum")
    count = number.get("quantity__sum")
    # total_pieces = pieces.get("item__pieces__sum")
   
    context = {
        'supcategory' : supcategory,
        'cart_items':cart_items,
        'total': total,
        'bill':bill,
        'count': count,
        # 'address':add,
        # 'total_pieces': total_pieces
    }
    return render(request, 'main/cart.html', context)
@login_required
def get_cart_item(request):

    supcategory=SuperCategory.objects.all()
    cart_items = CartItems.objects.filter(user=request.user,ordered=False)
    # accept_items = CartItems.objects.filter(status=Accepted)
    bill = cart_items.aggregate(Sum('item__price'))
    # number = cart_items.aggregate(Sum('quantity'))
    # pieces = cart_items.aggregate(Sum('item__pieces'))
    total = bill.get("item__price__sum")
    # count = number.get("quantity__sum")
    # total_pieces = pieces.get("item__pieces__sum")
   
    context = {
        'supcategory' : supcategory,
        'cart_items':cart_items,
        'total': total,
        # 'count': count,
        # 'total_pieces': total_pieces
    }
    return render(request, 'main/cart0.html', context)
class CartDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CartItems
    success_url = '/cart'

    def test_func(self):
        cart = self.get_object()
        if self.request.user == cart.user:
            return True
        return False
class AddressUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = CartItems
    fields = [ 'addresses', 'pincode', 'phone','quantity' ]
    success_url = '/cart'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        item = self.get_object()
        if self.request.user == item.user:
            return True
        return False

@login_required
def payment(request):
    return render(request, 'main/payment.html')

@login_required
def order_item(request):
  
    cart_items = CartItems.objects.filter(user=request.user,ordered=False)
    ordered_date=timezone.now()
    cart_items.update(ordered=True,ordered_date=ordered_date)
    messages.info(request, "Item Ordered")
    return redirect("main:order_details")

@login_required
def order_details(request):
    supcategory=SuperCategory.objects.all()
    
    items = CartItems.objects.filter(user=request.user, ordered=True,status="Accepted").order_by('-ordered_date')
    cart_items_ready = CartItems.objects.filter(user=request.user, ordered=True,status="Ready").order_by('-ordered_date')
    cart_items = CartItems.objects.filter(user=request.user, ordered=True,status="Delivered").order_by('-ordered_date')
    cart_items_rejected = CartItems.objects.filter(user=request.user, ordered=True,status="Rejected").order_by('-ordered_date')

    bill = items.aggregate(Sum('item__price'))
    # number = items.aggregate(Sum('quantity'))
    # pieces = items.aggregate(Sum('item__pieces'))
    total = bill.get("item__price__sum")
    # count = number.get("quantity__sum")
    # total_pieces = pieces.get("item__pieces__sum")
    context = {
        'supcategory' : supcategory,
        'items':items,
        'cart_items':cart_items,
        'total': total,
        # 'count': count,
        # 'total_pieces': total_pieces,
        'cart_items_ready':cart_items_ready,
        'cart_items_rejected':cart_items_rejected
    }
    return render(request, 'main/order_details.html', context)

@login_required(login_url='/accounts/login/')
@seller_required
def admin_view(request):
    cart_items = CartItems.objects.filter(item__sold_by=request.user, ordered=True,status="Delivered").order_by('-ordered_date')
    context = {
        'cart_items':cart_items,
    }
    return render(request, 'main/admin_view.html', context)

@login_required(login_url='/accounts/login/')
@seller_required
def rejected_orders(request):
    cart_items = CartItems.objects.filter(item__sold_by=request.user, ordered=True,status="Rejected").order_by('-ordered_date')
    context = {
        'cart_items':cart_items,
    }
    return render(request, 'main/rejected_orders.html', context)

@login_required(login_url='/accounts/login/')
@seller_required
def item_list(request):
    items = Item.objects.filter(sold_by=request.user)
    context = {
        'items':items
    }
    return render(request, 'main/item_list.html', context)

@login_required
@seller_required
def update_status(request,pk):
        if request.method == 'POST':
            status = request.POST['status']
            cart_items = CartItems.objects.filter(item__sold_by=request.user, ordered=True,status="Accepted",pk=pk)
            delivery_date=timezone.now()
            if status == 'Ready':
                cart_items.update(status=status, delivery_date=delivery_date)
                return redirect("main:accepted_orders")  
            if status == 'Delivered':
                cart_items.update(status=status, delivery_date=delivery_date)
                return redirect("main:admin_view")  
            if status == 'Rejected':
                cart_items.update(status=status, delivery_date=delivery_date)
                return redirect("main:rejected_orders")    
        return render(request, 'main/pending_orders.html')
# edited
@login_required
@seller_required
def update_ready(request,pk):
    if request.method == 'POST':
        status = request.POST['status']
    cart_items = CartItems.objects.filter(item__sold_by=request.user, ordered=True,status="Ready",id=pk)
    delivery_date=timezone.now()
    if status == 'Accepted':
        cart_items.update(status=status, delivery_date=delivery_date)
    if status == 'Delivered':
        cart_items.update(status=status, delivery_date=delivery_date)
    if status == 'Rejected':
        cart_items.update(status=status, delivery_date=delivery_date)    
    return render(request, 'main/accepted_orders.html')

@login_required(login_url='/accounts/login/')
@seller_required
def pending_orders(request):
    items = CartItems.objects.filter(item__sold_by=request.user, ordered=True,status="Accepted").order_by('-ordered_date')
    context = {
        'items':items,
    }
    return render(request, 'main/pending_orders.html', context)

    # trying
@login_required(login_url='/accounts/login/')
@seller_required
def accepted_orders(request):
    r_items = CartItems.objects.filter(item__sold_by=request.user, ordered=True,status="Ready").order_by('-ordered_date')
    context = {
        'r_items':r_items,
    }
    return render(request, 'main/accepted_orders.html', context)

@login_required(login_url='/accounts/login/')
@seller_required
def admin_dashboard(request):
    cart_items = CartItems.objects.filter(item__sold_by=request.user, ordered=True)
    pending_total = CartItems.objects.filter(item__sold_by=request.user, ordered=True,status="Accepted").count()
    completed_total = CartItems.objects.filter(item__sold_by=request.user, ordered=True,status="Delivered").count()
    ready_total = CartItems.objects.filter(item__sold_by=request.user, ordered=True,status="Ready").count()
    rejected_total = CartItems.objects.filter(item__sold_by=request.user, ordered=True,status="Rejected").count()
    count1 = CartItems.objects.filter(item__sold_by=request.user, ordered=True,item="3").count()
    count2 = CartItems.objects.filter(item__sold_by=request.user, ordered=True,item="4").count()
    count3 = CartItems.objects.filter(item__sold_by=request.user, ordered=True,item="5").count()
    total = CartItems.objects.filter(item__sold_by=request.user, ordered=True,status="Delivered").aggregate(earn=Sum('item__price')*Sum('quantity')-Sum('item__price')*Sum('quantity')/10)
  
    income = total.get("item__price__sum")
    context = {
        'pending_total' : pending_total,
        'ready_total' : ready_total,
        'completed_total' : completed_total,
        'rejected_total' : rejected_total,
        'income' : income,
        'count1' : count1,
        'count2' : count2,
        'count3' : count3,
        'total'  :  total,   
    }
    return render(request, 'main/admin_dashboard.html', context)
@admin_required
def admin_dashboard2(request,):
    
    
    cart_items = CartItems.objects.filter(ordered=True)
    pending_total = CartItems.objects.filter(ordered=True,status="Accepted").count()
    completed_total = CartItems.objects.filter(ordered=True,status="Delivered").count()
    ready_total = CartItems.objects.filter(ordered=True,status="Ready").count()
    rejected_total = CartItems.objects.filter( ordered=True,status="Rejected").count()
    count1 = CartItems.objects.filter( ordered=True,item="3").count()
    count2 = CartItems.objects.filter( ordered=True,item="4").count()
    count3 = CartItems.objects.filter( ordered=True,item="5").count()
    total = CartItems.objects.filter( ordered=True,status="Delivered").aggregate(profit=Sum('item__price')*Sum('quantity')/10)
    
    # total = CartItems.objects.filter( ordered=True,status="Delivered").aggregate(
            
    #         default=(Sum(F('item__price')))/10
    #     )
    
    # profit = total.get("item__price__sum")
    income = total.get("item__price__sum")
    # ourcut  =  income//10.0
    enq = Enquiry.objects.all().order_by('-date')
    sellers = User.objects.filter(groups__name='farmer')
    active_sellers= sellers.filter(is_active = True)
    nonactive_sellers= sellers.filter(is_active = False)
    context={
        'sellers':sellers,
        'active_sellers':active_sellers,
        'nonactive_sellers':nonactive_sellers,
        'pending_total' : pending_total,
        'ready_total' : ready_total,
        'completed_total' : completed_total,
        'rejected_total' : rejected_total,
        'income' : income,
        'count1' : count1,
        'count2' : count2,
        'count3' : count3,
        # 'profit':profit,
        'enq':enq,
        'total':total
        
    }
    
    # if request.method == 'POST':
    #     is_active = request.POST['status']
    #     cart_items =  User.objects.filter(groups__name='farmer',)
    
    #     if is_active == 'Activate':
    #         cart_items.update(is_active=True )
    #     if is_active == 'Remove':
    #         cart_items.delete(user=request.user, )
    
    return render(request,'main/admin_dashboard2.html', context  )


     
class SellerUpdateView(UpdateView,):
    model = User
    fields = ['is_active']
    success_url = '/admin_dashboard2'
    
    
    


    # def get_object(self):
    #     return User.objects.get(pk=self.request.GET.get('pk'))

    def post(self,request, pk,*args ,**kwargs):
        rec=User.objects.filter(groups__name='farmer', is_active=False, pk=pk)
        # rec.is_active = True
        # rec.save()
        email = rec.values_list('email', flat=True)
    # to = [email]
        print(email)
        email_list=[]
        for x in email:
            print(x)
            email_list.append(x)

            sendemail=EmailMessage('About Your Account Activation','Your Account has been activated open the login page here http://localhost:8000/accounts/login/ ',to=[x])
            sendemail.send()


        return super(SellerUpdateView, self).post(request, *args, **kwargs)


    
    def test_func(self):
        # user = User.objects.filter(pk=pk).first()
        
        item = self.get_object()
        if self.request.user == item:
            return True
        return False          





# Search

def search(request):
    
	q=request.GET['q']
    
	data=Item.objects.filter(title__icontains=q).order_by('-id')
	return render(request,'search.html',{'data':data})



# Item List According to Brand
def brand_product_list(request,brand_id):
	brand=Brand.objects.get(id=brand_id)
	data=Item.objects.filter(brand=brand).order_by('-id')
	return render(request,'category_product_list.html',{
			'data':data,
			})

# Item Detail
def product_detail(request,slug,id):
	product=Item.objects.get(id=id)
	related_products=Item.objects.filter(category=product.category).exclude(id=id)[:4]
	colors=ProductAttribute.objects.filter(product=product).values('color__id','color__title','color__color_code').distinct()
	sizes=ProductAttribute.objects.filter(product=product).values('size__id','size__title','price','color__id').distinct()

	# End

	return render(request, 'product_detail.html',{'data':product,'related':related_products,'colors':colors,'sizes':sizes,})


# Filter Data
def filter_data(request,):
    
    
	colors=request.GET.getlist('color[]')
	categories=request.GET.getlist('category[]')
	brands=request.GET.getlist('brand[]')
	sizes=request.GET.getlist('size[]')
	minPrice=request.GET['minPrice']
	maxPrice=request.GET['maxPrice']
    
	data=Item.objects.all().order_by('-id').distinct()
	data=data.filter(productattribute__price__gte=minPrice)
	data=data.filter(productattribute__price__lte=maxPrice)
	if len(colors)>0:
		data=data.filter(productattribute__color__id__in=colors).distinct()
	if len(categories)>0:
		data=data.filter(category__id__in=categories).distinct()
	if len(brands)>0:
		data=data.filter(brand__id__in=brands).distinct()
	if len(sizes)>0:
		data=data.filter(productattribute__size__id__in=sizes).distinct()
        
	t=render_to_string('ajax/subcategory.html',{'data':data})
	return JsonResponse({'data':t})

# Load More
def load_more_data(request):
	offset=int(request.GET['offset'])
	limit=int(request.GET['limit'])
	data=Item.objects.all().order_by('-id')[offset:offset+limit]
	t=render_to_string('ajax/product-list.html',{'data':data})
	return JsonResponse({'data':t}
)

# Add to cart
# def add_to_cart(request,slug):
# 	# del request.session['cartdata']
# 	cart_p={}
# 	cart_p[str(request.GET['id'])]={
# 		'image':request.GET['image'],
# 		'title':request.GET['title'],
# 		'qty':request.GET['qty'],
# 		'price':request.GET['price'],
# 	}
# 	if 'cartdata' in request.session:
# 		if str(request.GET['id']) in request.session['cartdata']:
# 			cart_data=request.session['cartdata']
# 			cart_data[str(request.GET['id'])]['qty']=int(cart_p[str(request.GET['id'])]['qty'])
# 			cart_data.update(cart_data)
# 			request.session['cartdata']=cart_data
# 		else:
# 			cart_data=request.session['cartdata']
# 			cart_data.update(cart_p)
# 			request.session['cartdata']=cart_data
# 	else:
# 		request.session['cartdata']=cart_p
# 	return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})

# Cart List Page
def cart_list(request):
	total_amt=0
	if 'cartdata' in request.session:
		for p_id,item in request.session['cartdata'].items():
			total_amt+=int(item['qty'])*float(item['price'])
		return render(request, 'cart.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	else:
		return render(request, 'cart.html',{'cart_data':'','totalitems':0,'total_amt':total_amt})


# def enquiry(request):
    # if request.user.is_authenticated:
       
        # return render(request, 'main/home.html')      
