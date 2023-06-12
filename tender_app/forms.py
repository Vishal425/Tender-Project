from dataclasses import fields
from django import forms
from .models import tender_keword_models
from .models import test_tender_model
import pandas as pd
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from tender_app import scrap

read_data = pd.DataFrame(list(tender_keword_models.objects.all().values()))

OPTIONS=[]
for i in range(len(read_data)):
    a=(tuple((read_data['keywords'][i],read_data['keywords'][i])))
    OPTIONS.append(a)
OPTIONS=tuple(OPTIONS)

class CountryForm(forms.Form):
    

    # OPTIONS = (
    #     ("AUT", "Austria"),
    #     ("DEU", "Germany"),
    #     ("NLD", "Neitherlands"),
    #     ('Hellow','World')
    # )
    KEYWORDS = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=OPTIONS)



class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','email','password1','password2']   
       
# read_data1 = pd.DataFrame(scrap)