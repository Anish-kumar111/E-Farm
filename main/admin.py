from django.contrib import admin
from .models import *
from django.db import models

class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Category", {'fields': ["category"]}),
        ("SubCategory", {'fields': ["subcategory"]}),
        ("Sold By", {'fields': ["sold_by"]}),
        ("Title", {'fields': ["title"]}),
        ("Image", {'fields': ["image"]}),
        ("Overview", {'fields': ["description"]}),
        ("Price", {'fields': ["price"]}),
        ("MOQ", {'fields': ["moq"]}),
        ("Instructions", {'fields': ["instructions"]}),
        ("Measurement", {'fields': ["labels"]}),
        ("Slug", {'fields': ["slug"]}),
        ("Ships From", {'fields': ["ships_from"]}),
        ("Deliver Within", {'fields': ["delivered_within"]}),
        ("Pattern", {'fields': ["pattern"]}),
        ("Length", {'fields': ["length"]}),
        ("Ocassion", {'fields': ["ocassion"]}),
        ("Material", {'fields': ["material"]}),
        ("End Use", {'fields': ["end_use"]}),
        ("Ply", {'fields': ["ply"]}),
        ("Fabric Stage", {'fields': ["fabric_stage"]}),
        # ("Quantity", {'fields': ["quantity"]}),
    ]
    list_display = ('id','sold_by','title','description','price','type')

class CartItemsAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Order Status", {'fields' : ["status"]}),
        ("Delivery Date", {'fields' : ["delivery_date"]}),
         ("Delivery Address", {'fields' : ["addresses"]}),
         ("Quantity", {'fields': ["quantity"]}),


    ]
    list_display = ('id','user','item','ordered','ordered_date','delivery_date','status','quantity')
    list_filter = ('ordered','ordered_date','status')

class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('user','item','review','posted_on')

admin.site.register(Item,
# ItemAdmin
)
admin.site.register(CartItems,
# CartItemsAdmin
)
admin.site.register(Reviews,ReviewsAdmin)
admin.site.register(SuperCategory)
admin.site.register(Category)
admin.site.register(SubCategory)
# admin.site.register(ProductAttribute)
# admin.site.register(Color)
# admin.site.register(Size)
# admin.site.register(ProductReview)
# admin.site.register(Address)

# admin.site.register(Enquiry)