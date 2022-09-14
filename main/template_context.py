from .models import Item,ProductAttribute, SuperCategory
from accounts.models import Profile
from django.db.models import Min,Max
from django.contrib.auth.decorators import login_required
def get_filters(request):
	cats=Item.objects.distinct().values('category__name','category__id')
	# brands=Item.objects.distinct().values('brand__title','brand__id')
	colors=ProductAttribute.objects.distinct().values('color__title','color__id','color__color_code')
	sizes=ProductAttribute.objects.distinct().values('size__title','size__id')
	minMaxPrice=ProductAttribute.objects.aggregate(Min('price'),Max('price'))
	supcategory=SuperCategory.objects.all()
	data={
		'cats':cats,
		# 'brands':brands,
		'colors':colors,
		'sizes':sizes,
		'minMaxPrice':minMaxPrice,
		 'supcategory' : supcategory,
	}
	return data

def get_navitems(request):
	profile=''
	supcategory=SuperCategory.objects.all()
	try:
		profile = Profile.objects.filter(user=request.user)
	except :
		pass
	data={
			'profile' : profile,
		 'supcategory' : supcategory,
	}
	return data	