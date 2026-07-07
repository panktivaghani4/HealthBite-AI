from django import forms
from .models import Order, Review



class SearchForm(forms.Form):

    search = forms.CharField(
        required=False,
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': '🔍 Search Healthy Food...'
            }
        )
    )

    food_type = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'All Foods'),
            ('Weight Loss', 'Weight Loss'),
            ('Weight Gain', 'Weight Gain'),
            ('Maintain', 'Maintain'),
        ],
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    sort_by = forms.ChoiceField(
    required=False,
    label='',
    choices=[
        ('', 'Sort By'),
        ('low_calories', '🔥 Low Calories'),
        ('high_protein', '🥩 High Protein'),
        ('low_price', '💰 Lowest Price'),
        ('high_price', '💎 Highest Price'),
    ],
    widget=forms.Select(
        attrs={
            'class': 'form-control'
        }
    )
)


class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['contact'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['count'].widget.attrs.update({
            'class': 'form-control'
        })

        self.fields['address'].widget.attrs.update({
            'class': 'form-control'
        })

    class Meta:
        model = Order
        fields = [
            'count',
            'name',
            'contact',
            'address',
        ]


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review

        fields = [
            "rating",
            "comment",
        ]

        widgets = {

            "rating": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),

            "comment": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Write your review..."
                }
            ),
        }