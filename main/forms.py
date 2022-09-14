
from django import forms
from .models import  ProductReview


class ReviewAdd(forms.ModelForm):
	class Meta:
		model=ProductReview
		fields=('review_text','review_rating')
       