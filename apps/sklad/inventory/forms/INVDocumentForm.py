from django import forms

class INVDocumentForm(forms.Form):
    number = forms.CharField(label='Номер документа', max_length=50)
    date = forms.DateField(label='Дата документа')
    # Add more fields as required by Article 9 of Law No. 402-FZ

    def clean(self):
        cleaned_data = super().clean()
        # Add custom validation logic based on Article 9 requirements
        # Perform necessary checks on the form fields
        # Raise a validation error if the requirements are not met
        return cleaned_data
