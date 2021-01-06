from django import forms
FIELD_CHOICES = [('title','Movie Title'),
                 ('overview', 'Movie Overview'),
                 ('actor','Movie Actor')]
class SearchForm(forms.Form):
    search_field = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
        choices=FIELD_CHOICES,
        label="Search By:"
    )
    search_text = forms.CharField(label='Search')

class ClassifyForm(forms.Form):
    classify_plot = forms.CharField(widget=forms.Textarea)

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()