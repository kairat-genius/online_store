from django import forms

from .models import Reviews, Rating, RatingStar


class ReviewForm(forms.ModelForm):
    """Формы отзывов"""

    class Meta:
        model = Reviews
        fields = ("name", "email", "text", 'avatar')
        widgets = {
            "name": forms.TextInput(attrs={"class": "blog-leave-comment-input", "placeholder": "name"}),
            "email": forms.EmailInput(attrs={"class": "blog-leave-comment-input", "placeholder": "email"}),
            "text": forms.Textarea(attrs={"class": "blog-leave-comment-textarea", "placeholder": "message"}),


        }


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star",)


class ProductFilterForm(forms.Form):
    price_min = forms.IntegerField(
        label="Минимальная цена",
        required=False,
        widget=forms.TextInput(attrs={"value": "2500", "class": "input-min", "type": "number"})
    )
    price_max = forms.IntegerField(
        label="Минимальная цена",
        required=False,
        widget=forms.TextInput(attrs={"value": "7500", "class": "input-max", "type": "number"})
    )
