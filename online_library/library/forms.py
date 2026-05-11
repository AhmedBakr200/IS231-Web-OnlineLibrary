from django import forms
from django.forms import ModelForm
from .models import Book
from django.core.validators import MinValueValidator, MaxValueValidator
import datetime
CATEGORY_CHOICES = [
    ("Biography", "Biography"),
    ("History", "History"),
    ("Science & Technology", "Science & Technology"),
    ("Self-Help", "Self-Help"),
    ("Business", "Business"),
    ("Philosophy", "Philosophy"),
    ("Religion", "Religion"),
    ("Politics", "Politics"),
    ("Art", "Art"),
    ("Travel", "Travel"),
    ("Cooking", "Cooking"),
    ("Education", "Education"),
    ("Health", "Health"),
    ("Literary", "Literary Fiction"),
    ("Mystery", "Mystery"),
    ("Fantasy", "Fantasy"),
    ("Romance", "Romance"),
    ("Historical Fiction", "Historical Fiction"),
    ("Horror", "Horror"),
    ("Young Adult", "Young Adult"),
    ("Children's Books", "Children's Books"),
    ("Graphic Novels", "Graphic Novels"),
]
class BookForm(forms.ModelForm):
    year = forms.IntegerField(
        validators=[
            MinValueValidator(1000, message="The year cannot be less than 1000"),
            MaxValueValidator(datetime.date.today().year, message="Year cannot be in the future.")
        ]
    )
    copies = forms.IntegerField(
        validators=[
            MinValueValidator(1, message="The copies cannot be less than 1"),
        ]
    )
    class Meta:
        model=Book
        fields = ('title', 'author','category', 'year','description','copies','image')
        labels = {
			'title' : 'Title',
            'author' : 'Author',
            'category' : 'Category',
            'year' : 'Year of Publish',
            'copies' : 'Available Copies',
            'image' : 'Cover URL',
            'description' : 'Description',
        }
        widgets = {
			'title' : forms.TextInput(attrs={'placeholder':'Enter Book Title'}),
            'author' : forms.TextInput(attrs={'placeholder':'Enter Book Author'}),
            'category' : forms.Select(choices=CATEGORY_CHOICES),
            'year' : forms.TextInput(attrs={'placeholder':'Enter Book Year'}),
            'copies' : forms.TextInput(attrs={'placeholder':'Enter Book Number of Copies'}),
            'image' : forms.TextInput(attrs={'placeholder':'Enter Book Cover Image URL'}),
            'description' : forms.Textarea(attrs={'placeholder':'Enter Book Description'}),
        }
    
    def clean_author(self):
        author = self.cleaned_data["author"]
        if any(char.isdigit() for char in author):
            raise forms.ValidationError("The author name can't contain digits.")
        return author
    
    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        author = cleaned_data.get('author')
        if title and author and title.lower() == author.lower():
            raise forms.ValidationError("The book title and author cannot be the same.")
        return cleaned_data