from django import forms
from django.forms import ModelForm
from .models import Book
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
class BookForm(ModelForm):
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
            'description' : forms.TextInput(attrs={'placeholder':'Enter Book Description'}),
        }
		