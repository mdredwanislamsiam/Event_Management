from django import forms
from events.models import Event, Category

class StyledFormMixin: 
    
    default_style = "mx-auto shadow-lg px-3 py-2 my-2 rounded-md"
    def apply_styled_widgets(self): 
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    'class': f" w-full  {self.default_style}",
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    'class': f" w-full  {self.default_style}",
                    'placeholder': f"Enter {field.label.lower()}"
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    'class': self.default_style
                })
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({
                    'class': self.default_style
                })
            elif isinstance(field.widget, forms.ClearableFileInput):
                field.widget.attrs.update({
                    'class': f"w-full {self.default_style} bg-white",
                })
           

class CategoryModelForm(StyledFormMixin,forms.ModelForm):
    class Meta: 
        model = Category
        fields = ['category_name', 'category_description']
        widgets = {
            'category_description': forms.Textarea
        }
       
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()

# django model form
class EventModelForm( StyledFormMixin, forms.ModelForm):
    class Meta: 
        model = Event
        fields = ['name', 'description', 'image', 'date', 'time', 'location']
        widgets = {
            'date': forms.SelectDateWidget, 
            'time': forms.TimeInput(attrs={'type':'time'}),
            'description': forms.Textarea, 
            'image': forms.ClearableFileInput()
            
        }
        
    def __init__(self, *arg, **kwarg):
        super().__init__(*arg, **kwarg)
        self.apply_styled_widgets()
        

      