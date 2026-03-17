from django import forms

from catalog.models import Title

from .models import Review


class ReviewForm(forms.ModelForm):
    """Форма для создания и редактирования отзыва"""

    title_name = forms.CharField(
        max_length=100,
        label='Название произведения',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите название фильма, сериала или игры...'
        })
    )

    category = forms.ChoiceField(
        choices=Title.CATEGORY_CHOICES,
        label='Категория',
        initial='film',
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = Review
        fields = ['title_name', 'category', 'text', 'rating', 'image']
        labels = {
            'text': 'Текст отзыва',
            'rating': 'Оценка (от 1 до 10)',
            'image': 'Фото',
        }
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Напишите ваш отзыв...'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 10,
                'step': 1,
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.title:
            self.fields['title_name'].initial = self.instance.title.title
            self.fields['category'].initial = self.instance.title.category

    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 10:
            raise forms.ValidationError('Оценка должна быть от 1 до 10')
        return rating

    def clean_image(self):
        """Валидация изображения"""
        image = self.cleaned_data.get('image')
        if image:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError(
                    'Размер файла не должен превышать 5MB'
                )

            allowed_extensions = ['jpg', 'jpeg', 'png', 'gif', 'webp']
            ext = image.name.split('.')[-1].lower()
            if ext not in allowed_extensions:
                raise forms.ValidationError(
                    f'Поддерживаются только форматы:{", ".join(allowed_extensions)}'
                )
        return image
