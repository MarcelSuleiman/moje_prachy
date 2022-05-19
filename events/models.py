from django.db import models

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=150)
	
	def __str__(self):
		return self.name


class SubCategory_01(models.Model):
	category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=150)

	def __str__(self):
		return self.name


class Items(models.Model):
	'''
	[1640198768.0, '22.12.2021', 'KELT 10ř 1,5l PET   ', 1.0, 0.99, 0.99, 20.0, 'K', 'TESCO STORES SR, a.s.', 'O-0D77D3B609D24285B7D3B609D2B2851A',
	 '31321828', '88820203011401673', '22.12.2021 19:46:08', '22.12.2021 19:46:08', None, '2020301140', 'SK7020000317', None, 
	 '6A8610E4-2B6CC2D2-3BECDE92-D37BA05F-C82E41C9', False, None, 
	 'IAdDuQv9pzoqpptKmf7WmAfY87nrT06pwRj4LJO0qRG+e1X2Gbb7E8jbY3OXM5BjOTXgskM3MnE+WokQWIf1ckcbi2YxqL4bGVynvjcn0eWM7Jadx
		Ku4f90vO1RmWoay2Zmv55oBiETr4sdLSRwzLnbZGa818u2S3mr4xroY0jiAGgZ0dSF4qkagqdUw4U4vncucuG+jXjse5HspNfezHDmG71lcrMe
		1Eb1xsjVWqj9AXyCeXqxNVaOn9gsNlUw2HrLWCaa9WT6BDxyK3DDWb7/0hyMPjPA834lLQM33VpatKlGCZwA49qJI+vFzu/dqFcuEhTM5Hv7Vw
		zcIakezug==', 4373, 'PD', 3.6, 0.0, 4.32, 0.0, 0.72, 0.0, 20.0, 10.0]

	'''


	date_of_purchase_time_stamp = models.IntegerField(blank=True)
	date_of_purchase = models.CharField(max_length=10, blank=False)
	item = models.CharField(max_length=100, blank=False)
	item_pretty = models.CharField(max_length=100, blank=True)
	quantity = models.FloatField(blank=False)
	price_per_one = models.FloatField(blank=False)
	price_per_all = models.FloatField(blank=False)
	
	category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
	sub_category_01 = models.ForeignKey(SubCategory_01, on_delete=models.SET_NULL, null=True)
	
	#item_class = models.CharField(max_length=100, blank=True, default='Bez kategórie')
	#item_sub_class = models.CharField(max_length=100, blank=True, default='Bez podkategórie')
	
	vat_rate = models.FloatField(blank=False)
	item_type = models.CharField(max_length=10, blank=False)
	seller = models.CharField(max_length=100, blank=False)
	uid = models.CharField(max_length=34, blank=False)
	ico = models.CharField(max_length=8, blank=True)
	cash_register_code = models.CharField(max_length=20, blank=True)
	issue_date =  models.CharField(max_length=20, blank=True)
	created_date = models.CharField(max_length=20, blank=True)
	customer_id = models.TextField(blank=True)
	dic = models.CharField(max_length=10, blank=True)
	ic_dph = models.CharField(max_length=12, blank=True)
	invoice_number = models.TextField(blank=True)
	okp = models.CharField(max_length=44, blank=True)
	paragon = models.BooleanField()
	paragon_number = models.TextField(blank=True)
	pkp = models.TextField(blank=True)
	receipt_no = models.IntegerField(blank=True)
	type_receipt = models.CharField(max_length=50, blank=True)
	tax_base_basic = models.FloatField(blank=True)
	tax_base_reduced = models.FloatField(blank=True)
	total_price = models.FloatField(blank=True)
	free_tax_amount = models.FloatField(blank=True)
	vat_amount_basic = models.FloatField(blank=True)
	vat_amount_reduced = models.FloatField(blank=True)
	vat_rate_basic = models.FloatField(blank=True)
	vat_rate_reduced = models.FloatField(blank=True)
	ean = models.CharField(max_length=13, blank=True)
	owner = models.CharField(max_length=100, blank=False)

	def __str__(self):
		return self.item


class ReceiptsIds(models.Model):
	date_of_purchase_time_stamp = models.IntegerField(blank=True, default=1)
	uid = models.CharField('Receipt UID', max_length=34, blank=False)
	seller = models.CharField('Seller', max_length=150, blank=True, null=True)
	day_name = models.CharField('Day name', max_length=20, blank=True, null=True)
	created_time = models.CharField('Created time', max_length=20, blank=True, null=True)
	created_date = models.CharField('Created date', max_length=20, blank=True, null=True)
	total_price = models.FloatField('Total price', blank=True, null=True)
	owner = models.CharField('Owner', max_length=100, blank=False)

	def __str__(self):
		#return self.seller + ' ' + self.uid
		return self.uid


class Venue(models.Model):
	name = models.CharField('Venue Name', max_length=120)
	address = models.CharField(max_length=300)
	zip_code = models.CharField('Zip Code', max_length=15)
	phone = models.CharField('contact Phone', max_length=25, blank=True)
	web = models.URLField('Website Address', blank=True)
	email_address = models.EmailField('Email Address', blank=True)

	def __str__(self):
		return self.name


class MyClubUser(models.Model):
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.EmailField('User Email', blank=True)

	def __str__(self):
		return self.first_name + ' ' + self.last_name


class Event(models.Model):
	name = models.CharField('Event Name', max_length=120)
	event_date = models.DateTimeField('Event Date')
	venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
	#venue = models.CharField(max_length=120)
	manager = models.CharField(max_length=60, blank=True)
	description = models.TextField(blank=True)
	attendees = models.ManyToManyField(MyClubUser, blank=True)

	def __str__(self):
		return self.name