from django import forms
from django.forms import ModelForm
from .models import Venue
from .models import ReceiptsIds
from .models import Items
from .models import Category
from .models import SubCategory_01


try:
	import simplejson as json
except ImportError:
	import json



def get_sub_class_choices():

	sub_class = (
		('Bez podkategórie','Bez podkategórie'),
		('Zelenina','Zelenina'),
		('Ovocie','Ovocie'),
		('Pečivo','Pečivo'),
		('Mlieko a mliečne výrobky','Mlieko a mliečne výrobky'),
		('Mäso a mäsové výrobky','Mäso a mäsové výrobky'),
		('Korenie a dochucovadlá','Korenie a dochucovadlá'),
		('Dlhodobé potraviny','Dlhodobé potraviny'),
		('Pivo','Pivo'),
		('Víno','Víno'),
		('Tvrdý alkohol','Tvrdý alkohol'),
		('Čaj','Čaj'),
		('Káva','Káva'),
		('Sirup','Sirup'),
		('Sladené','Sladené'),
		('Nesladené','Nesladené'),
		('Osobná hygiena','Osobná hygiena'),

	)
	return sub_class

def getFieldChoices(key_field=None):
	"""
	Return a tuple of field choices from a json file.

	"""
	with open('C:\\Users\\Marcel\\Desktop\\PYTHON\\projekty\\django codemy\\myclub_website\\events\\somefile.json') as f:
		json_data = json.load(f)
		choices_list = []
		if key_field and key_field in json_data:
			fields = json_data[key_field]
			for field in fields:
				choices_list.append((field, field))
	return tuple(choices_list)



# create a venue form
class VenueForm(ModelForm):
	class Meta:
		model = Venue
		#fields = '__all__'
		fields = ('name', 'address', 'zip_code', 'phone', 'web', 'email_address')
		labels = {
			'name': 'Názov',
			'address': 'Miesto podujatia',
			'zip_code': 'PSČ',
			'phone': 'Číslo na usporiadavateľa',
			'web': 'Webová stránka',
			'email_address': 'mail kontakt'
		}
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control'}),
			'address': forms.TextInput(attrs={'class':'form-control'}),
			'zip_code': forms.TextInput(attrs={'class':'form-control'}),
			'phone': forms.TextInput(attrs={'class':'form-control'}),
			'web': forms.TextInput(attrs={'class':'form-control'}),
			'email_address': forms.EmailInput(attrs={'class':'form-control'})
		}

class ReceiptsIdsForm(ModelForm):
	class Meta:
		model = ReceiptsIds
		fields = ('uid', 'owner')


class ItemsForm(ModelForm):
	class Meta:
		model = Items
		fields = '__all__'


base_class = (
	('Bez kategórie','Bez kategórie'),
	('Potraviny','Potraviny'),
	('Drogéria','Drogéria'),
	('Nápoje','Nápoje'),
	('Alkohol','Alkohol'),
	('Chovatelské potreby a krmivo','Chovatelské potreby a krmivo'),
	('Elektronika','Elektronika'),
	('Dom, byt, záhrada','Dom, byt, záhrada'),
	('Auto','Auto'),
	('Zdravie a lieky','Zdravie a lieky'),
)


sub_class = (
	('Bez podkategórie','Bez podkategórie'),
	('Zelenina','Zelenina'),
	('Ovocie','Ovocie'),
	('Pečivo','Pečivo'),
	('Mlieko a mliečne výrobky','Mlieko a mliečne výrobky'),
	('Mäso a mäsové výrobky','Mäso a mäsové výrobky'),
	('Korenie a dochucovadlá','Korenie a dochucovadlá'),
	('Dlhodobé potraviny','Dlhodobé potraviny'),
	('Pivo','Pivo'),
	('Víno','Víno'),
	('Tvrdý alkohol','Tvrdý alkohol'),
	('Čaj','Čaj'),
	('Káva','Káva'),
	('Sirup','Sirup'),
	('Sladené','Sladené'),
	('Nesladené','Nesladené'),
	('Osobná hygiena','Osobná hygiena'),

)




class ItemsUpdateForm(ModelForm):
	#item_class = forms.ChoiceField(label='Kategória (Potraviny, Dorgéria, Alkohol, ...)', choices=base_class, widget=forms.Select(attrs={'class':'form-select'}))
	#item_sub_class = forms.ChoiceField(label='Podkategória (Zelenina, Osobná hygiena, Pivo)', choices=sub_class, widget=forms.Select(attrs={'class':'form-select'}))
	quantity = forms.DecimalField()
	price_per_one = forms.FloatField()
	price_per_all = forms.FloatField()

	class Meta:
		model = Items
		fields = ('item', 'quantity', 'price_per_one', 'price_per_all')
		labels = {
			'item': 'Položka',
			'quantity': 'Množstvo',
			'price_per_one': 'Cena za kus / kilo / liter / meter a pod.',
			'price_per_all': 'Celková cena za položku',
		}
		widgets = {
			'item': forms.TextInput(attrs={'class':'form-control'}),
		}

class ItemsUpdateCategoryForm(ModelForm):
	#item_class = forms.ChoiceField(label='Kategória (Potraviny, Dorgéria, ...)', choices=base_class, widget=forms.Select(attrs={'class':'form-select'}))
	#item_sub_class = forms.ChoiceField(label='Podkategória (Zelenina, Osobná hygiena, ...)', choices=sub_class, widget=forms.Select(attrs={'class':'form-select'}))

	class Meta:
		model = Items
		#fields = ('item_class', 'item_sub_class', 'item_pretty', 'ean')
		fields = ('category', 'sub_category_01', 'item_pretty', 'ean')

		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			self.fields['sub_category_01'].queryset = SubCategory_01.objects.none()

			if 'category' in self.data:
				try:
					category_id = int(self.data.get('category'))
					self.fields['sub_category_01'].queryset = SubCategory_01.objects.filter(category_id=category_id).order_by('name')
				except Exception as E:
					print(E.__class__.__name__, str(E))
			elif self.instance.pk:
				self.fields['sub_category_01'].queryset = self.instance.category.sub_category_01_set.order_by('name')



		labels = {

			'category': 'Kategória',
			'sub_category_01': 'Podkategória',

			'item_pretty': 'Môj názov produktu',
			'ean': 'EAN kód',
		}
		widgets = {
			'category': forms.Select(attrs={'class':'form-select'}),
			'sub_category_01': forms.Select(attrs={'class':'form-select'}),
			'item_pretty': forms.TextInput(attrs={'class':'form-control'}),
			'ean': forms.TextInput(attrs={'class':'form-control'}),
		}



class ReceiptUidManual(forms.Form):
	receipt_uid = forms.CharField(label='UID',  widget=forms.TextInput(attrs={'placeholder': 'O-3C2BE10AC9C84D98ABE10AC9C84D98AB', 'class':'form-control'}))