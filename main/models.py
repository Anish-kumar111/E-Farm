



from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.html import mark_safe
from django.db import models
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, reverse
from django.utils import timezone
from django.contrib.auth.models import User


from smart_selects.db_fields import ChainedForeignKey

# class Item(models.Model):
#     LABELS = (
#         ('Best Selling Foods', 'Best Selling Foods'),
#         ('New Food', 'New Food'),
#         ('Spicy Foods', 'Spicy Foods'),
#     )   

#     LABEL_COLOUR = (
#         ('danger', 'danger'),
#         ('success', 'success'),
#         ('primary', 'primary'),
#         ('info', 'info'),
#         ('warning', 'warning'),
#     )
#     title = models.CharField(max_length=150)
#     description = models.CharField(max_length=250,blank=True)
#     price = models.FloatField()
#     pieces = models.IntegerField(default=6)
#     instructions = models.CharField(max_length=250,default="Available")
#     image = models.ImageField(default='default.png', upload_to='images/')
#     labels = models.CharField(max_length=25, choices=LABELS, blank=True)
#     label_colour = models.CharField(max_length=15, choices=LABEL_COLOUR, blank=True)
#     slug = models.SlugField(default="foods")
#     sold_by = models.ForeignKey(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.title

#     def get_absolute_url(self):
#         return reverse("main:product", kwargs={
#             'slug': self.slug
#         })
    
#     def get_add_to_cart_url(self):
#         return reverse("main:add-to-cart", kwargs={
#             'slug': self.slug
#         })

#     def get_item_delete_url(self):
#         return reverse("main:item-delete", kwargs={
#             'slug': self.slug
#         })

#     def get_update_item_url(self):
#         return reverse("main:item-update", kwargs={
#             'slug': self.slug
        # })



class SuperCategory(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(default='Auto', null=False)
    class Meta:
        ordering = ('-id',)
        
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        # return  (f'{self.slug}')
        return reverse("main:supcategory", kwargs={
            'slug': f'/{self.slug}/'
        })
    def save(self, *args ,**kwargs): 
        value = self.name   
        self.slug = slugify(value, allow_unicode = True)
        super().save(*args, **kwargs)    

class Category(models.Model):
    SuperCategory = models.ForeignKey(SuperCategory, on_delete = models.CASCADE,related_name='sups',)
    name = models.CharField(max_length=255)
    slug = models.SlugField(default='Auto', null=False)
    class Meta:
        ordering = ('-id',)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        # return  (f'{self.slug}')
        return reverse("main:category", kwargs={
            'slug': f'/{self.slug}/'
        })
    def save(self, *args ,**kwargs): 
        value = self.name   
        self.slug = slugify(value, allow_unicode = True)
        super().save(*args, **kwargs)
class SubCategory(models.Model):
    SuperCategory = models.ForeignKey(SuperCategory, on_delete = models.CASCADE)
    Category = ChainedForeignKey(
        Category,
        chained_field="SuperCategory",
        chained_model_field="SuperCategory",
        show_all=False,
        auto_choose=True,
        sort=True,
        related_name='subs',)
    # area = ForeignKey(Area)
    title = models.CharField(max_length=50)
    image = models.ImageField(default='default.png', upload_to='images/subcategories/')
    slug = models.SlugField(default='Auto', null=False)
    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        # return  (f'{self.slug}')
        return reverse("main:subcategory", kwargs={
            'slug': f'/{self.slug}/'
        })
    def save(self, *args ,**kwargs): 
        value = self.title   
        self.slug = slugify(value, allow_unicode = True)
        super().save(*args, **kwargs)
           
# Brand
class Brand(models.Model):
    title=models.CharField(max_length=100)
    image=models.ImageField(upload_to="brand_imgs/")

    class Meta:
        verbose_name_plural='Brands'

    def __str__(self):
        return self.title

# Color
class Color(models.Model):
    title=models.CharField(max_length=100)
    color_code=models.CharField(max_length=100)

    class Meta:
        verbose_name_plural='Colors'

    def color_bg(self):
        return mark_safe('<div style="width:30px; height:30px; background-color:%s"></div>' % (self.color_code))

    def __str__(self):
        return self.title

# Size
class Size(models.Model):
    title=models.CharField(max_length=100)

    class Meta:
        verbose_name_plural='Sizes'

    def __str__(self):
        return self.title


class Item(models.Model):
    LABELS = (
        ('KG', 'KG'),
        ('grams', 'grams'),
        ('Dozen', 'Dozen'),
    )   

    LABEL_COLOUR = (
        ('danger', 'danger'),
        ('success', 'success'),
        ('primary', 'primary'),
        ('info', 'info'),
        ('warning', 'warning'),
    )
    
    category = models.ForeignKey(Category,related_name='products', on_delete=models.CASCADE)
    subcategory = ChainedForeignKey(
        SubCategory,
        chained_field="category",
        chained_model_field="Category",
        show_all=True,
        auto_choose=True,
        sort=True,
        related_name='subss',)

    title = models.CharField(max_length=150)
    description = models.CharField(max_length=250,blank=True,null=True)
    price = models.FloatField()
    moq = models.IntegerField(default=1)
    
    instructions = models.CharField(max_length=250,default="Available")
    image = models.ImageField(default='default.png', upload_to='images/')
    labels = models.CharField(max_length=25, choices=LABELS, blank=True)
    # label_colour = models.CharField(max_length=15, choices=LABEL_COLOUR, blank=True)
    slug = models.SlugField(default="Automatic",
    null=True)
    ships_from = models.CharField(max_length=100)
    delivered_within = models.CharField(max_length=50)
    sold_by = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=6,blank=True,null=True)
    # 


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # if Item.objects.filter(slug=self.slug).exists():
        #     return ('slug already exists')

        # else:
        
            return  (f'/product/{self.slug}')
        # return reverse("main:product", kwargs={
        #     'slug': self.slug
            # 'slug': f'/product/{self.slug}'
            
        # })
    def save(self, *args ,**kwargs): 
        value = self.title   
        self.slug = slugify(value, allow_unicode = True)
        super().save(*args, **kwargs)
    
    def get_add_to_cart_url(self):
        return reverse("main:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_item_delete_url(self):
        return reverse("main:item-delete", kwargs={
            'slug': self.slug
        })

    def get_update_item_url(self):
        return reverse("main:item-update", kwargs={
            'slug': self.slug
        })

class ProductAttribute(models.Model):
    product=models.ForeignKey(Item,on_delete=models.CASCADE)
    color=models.ForeignKey(Color,on_delete=models.CASCADE)
    size=models.ForeignKey(Size,on_delete=models.CASCADE)
    price=models.PositiveIntegerField(default=0)
    # image=models.ImageField(upload_to="product_imgs/",null=True)

    class Meta:
        verbose_name_plural=' ProductAttributes'

    def __str__(self):
        return self.product.title
class CartItems(models.Model):
    ORDER_STATUS = (
        ('Accepted', 'Accepted'),
        ('Ready', 'Ready'),
        ('Delivered', 'Delivered'),
        ('Rejected', 'Rejected'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE,related_name='itms')
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    ordered_date = models.DateField(default=timezone.now)
    
    # aslug= models.SlugField(null=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='Accepted')
    delivery_date = models.DateField(default=timezone.now)
    # price = models.IntegerField(default=1)
    addresses =models.CharField(max_length=200,null=True, blank=True)
    pincode =models.CharField(max_length=6,null=True, blank=True)
    phone =models.CharField(max_length=13,null=True, blank=True)




    
    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'

    def __str__(self):
        return self.item.title
    def get_address_from_cart_url(self):
        return reverse("main:address-from-cart", kwargs={
            'pk': self.pk
        })  
    def get_remove_from_cart_url(self):
        return reverse("main:remove-from-cart", kwargs={
            'pk' : self.pk
        })

    def update_status_url(self):
        return reverse("main:update_status", kwargs={
            'pk' : self.pk
        })
      
class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    item = models.ForeignKey(Item, on_delete = models.CASCADE)
    rslug = models.SlugField()
    review = models.TextField()
    posted_on = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.review        


# Item Review
RATING=(
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
)
class ProductReview(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Item,on_delete=models.CASCADE)
    review_text=models.TextField()
    review_rating=models.CharField(choices=RATING,max_length=150)

    class Meta:
        verbose_name_plural='Reviews'

    def get_review_rating(self):
        return self.review_rating 
class Address(models.Model):
    orderitem=models.ForeignKey(CartItems,on_delete=models.CASCADE) 
    address =models.CharField(max_length=200,null=True, blank=True)


# class Enquiry(models.Model):
#     # user = models.ForeignKey(User,on_delete=models.CASCADE)
#     name = models.CharField(max_length=121)
#     email = models.CharField(max_length=121)
#     firm  = models.CharField(max_length=111)
#     date = models.DateField()
 
#     def __str__(self):
#       return self.name    