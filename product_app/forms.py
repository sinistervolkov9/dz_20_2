from django import forms
from django.forms import ModelForm
from product_app.models import Product, Version

FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class StyleMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields_style()

    def fields_style(self):
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


class ProductForm(StyleMixin, ModelForm):
    class Meta:
        model = Product
        # fields = ['name', 'price', 'description', 'photo']
        fields = '__all__'
        # exclude = ('price', )

    def clean_name(self):
        name = self.cleaned_data.get('name')

        for word in FORBIDDEN_WORDS:
            if word in name.lower():
                raise forms.ValidationError(f"'{word}' - это запрещенное слово")

        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')

        for word in FORBIDDEN_WORDS:
            if word in description.lower():
                raise forms.ValidationError(f"{word}' - это запрещенное слово")

        return description


class VersionForm(StyleMixin, forms.ModelForm):

    class Meta:
        model = Version
        fields = '__all__'
