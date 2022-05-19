from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.http.response import StreamingHttpResponse
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages

import calendar
from calendar import HTMLCalendar
from datetime import datetime

from .models import Event, Venue
from .models import ReceiptsIds
from .models import Items

from .models import Category, SubCategory_01
from django.urls import reverse_lazy

from .forms import VenueForm 
from .forms import ReceiptsIdsForm
from .forms import ItemsForm, ItemsUpdateForm, ItemsUpdateCategoryForm, ReceiptUidManual

from time import sleep
import time

import cv2
import pyzbar.pyzbar as pyzbar
from .financna_sprava import check_recipt
from .grab_data import grab_data

import sqlite3
import psycopg2
import dash
import plotly
import plotly.express as px
import pandas as pd
from django_plotly_dash import DjangoDash
import dash_table
from dash.dependencies import Input, Output
import dash_html_components as html

import csv

import django_tables2 as tables
from django_tables2 import SingleTableView
from .tables import ItemsTable
'''
`import dash_html_components as html` with `from dash import html`
  import dash_html_components as html
'''

import dash_core_components as dcc
'''
`import dash_core_components as dcc` with `from dash import dcc`
  import dash_core_components as dcc
'''

# Create your views here.



from .camera import VideoCamera

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_stream(request):
    return StreamingHttpResponse(gen(VideoCamera()),
                    content_type='multipart/x-mixed-replace; boundary=frame')



def get_frame():
	camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
	font = cv2.FONT_ITALIC

	#uid_receipts = ReceiptsIds.objects.all()
	#print(uid_receipts)
	#print(type(uid_receipts))
	#print(list(uid_receipts))

	#for i in uid_receipts:
	#	print(i)

	while True:

		success, frame = camera.read()

		decoded_objects = pyzbar.decode(frame)
		if decoded_objects != []:
			for obj in decoded_objects:

				cv2.putText(frame, str('precitane'), (50, 580), font, 1, (255, 0, 0), 2)
				uid_bill = str(obj.data)
				uid_bill = uid_bill[2:-1]

				uid_receipts_2 = ReceiptsIds.objects.filter(uid = uid_bill)

				if uid_receipts_2:
					cv2.putText(frame, str('uz naskenovane, dalsi prosim'), (50, 50), font, 1, (255, 0, 0), 2)

				else:
					if len(uid_bill) == 34:
						cv2.putText(frame, str('dekodujem data'), (50, 50), font, 1, (255, 0, 0), 2)
						
						
						
						# pridaj cislo bloku do databazy / tabulky - zatial zbytocne,
						# cislo bloku sa nachadza pri kazdej polozke v inej tabulke
						# ae radsej mat ako nemat, ak sa casom ukaze ze je to naozaj zbytocne,
						# lahsie sa odstrani nez spatne prida
						

						data_from_bill = check_recipt(uid_bill)

						print(data_from_bill['receipt']['issueDate'])
						print(data_from_bill['searchIdentification']['createDate'])
						print(data_from_bill['receipt']['organization']['name'])
						print(data_from_bill['receipt']['totalPrice'])

							
						seller = data_from_bill['receipt']['organization']['name']

						date_time_list = data_from_bill['receipt']['issueDate'].split(' ')
						
						created_date = date_time_list[0]
						created_time = date_time_list[1]

						day_name_en = datetime.strptime(created_date, '%d.%m.%Y').strftime('%a') #'Mon'

						days_translate = {'Mon': 'Pon', 'Tue': 'Ut', 'Wed': 'Str', 'Thu':'Štv', 'Fri':'Pia', 'Sat':'Sob', 'Sun':'Ned'}

						day_name = days_translate[day_name_en]

						date_of_purchase_time_stamp = time.mktime(time.strptime(data_from_bill['receipt']['createDate'], "%d.%m.%Y %H:%M:%S"))

						total_price = float(data_from_bill['receipt']['totalPrice'])
						owner = request.user.get_username()

						print(owner)

						add_receipt_uid(date_of_purchase_time_stamp, uid_bill, seller, day_name, created_time, created_date, total_price, owner)

						list_rows = grab_data(data_from_bill)

						#print(list_rows)
						#print(len(list_rows))

						for list_row in list_rows:
							#print(list_row)
							add_items(list_row, owner)


		ret, buffer = cv2.imencode('.jpg', frame)
		frame = buffer.tobytes()

		#print(camera.isOpened())
		
		yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def camera_dva(request):
	return render(request, 'events/camera_dva.html')


def camera(request):
	try:
		sleep(0.05)
		return StreamingHttpResponse(get_frame(), content_type='multipart/x-mixed-replace; boundary=frame')
	except Exception as E:
		print(E.__class__.__name__, str(E))


def nechodsem(request):
	blocky = []

	owner = request.user.get_username()

	for b in blocky:
		sleep(5)
		data_from_bill = check_recipt(b)
		list_rows = grab_data(data_from_bill)

		#print(list_rows)
		#print(len(list_rows))

		for list_row in list_rows:
			#print(list_row)
			add_items(list_row, owner)

	return render(request, 'events/nechodsem.html', {})

def add_items(list_row, owner):

	date_of_purchase_time_stamp = list_row[0]
	date_of_purchase = list_row[1]
	item = list_row[2]
	quantity = list_row[3]
	price_per_one = list_row[4]
	price_per_all = list_row[5]
	vat_rate = list_row[6]
	item_type = list_row[7]
	seller = list_row[8]
	uid = list_row[9]
	ico = list_row[10]
	cash_register_code = list_row[11]
	issue_date =  list_row[12]
	created_date = list_row[13]

	if list_row[14] == None:
		customer_id = ''
	else:
		customer_id = list_row[14]

	dic = list_row[15]
	ic_dph = list_row[16]

	if list_row[17] == None:
		invoice_number = ''
	else:
		invoice_number = list_row[17]

	okp = list_row[18]
	paragon = list_row[19]

	if list_row[20] == None:
		paragon_number = ''
	else:
		paragon_number = list_row[20]

	pkp = list_row[21]
	receipt_no = list_row[22]
	type_receipt = list_row[23]
	tax_base_basic = list_row[24]
	if list_row[25] == None:
		tax_base_reduced = 0
	else:
		tax_base_reduced = list_row[25]
	
	total_price = list_row[26]
	
	if list_row[27] == None:
		free_tax_amount = 0
	else:
		free_tax_amount = list_row[27]

	vat_amount_basic = list_row[28]
	
	if list_row[29] == None:
		vat_amount_reduced = 0
	else:
		vat_amount_reduced = list_row[29]
	
	vat_rate_basic = list_row[30]
	
	if list_row[31] == None:
		vat_rate_reduced = 0
	else:
		vat_rate_reduced = list_row[31]
	
	owner =	owner

	category_id = 'neznáme'
	sub_category_01_id = 'neznáme'

	r = Items(date_of_purchase_time_stamp=date_of_purchase_time_stamp, date_of_purchase=date_of_purchase, item=item,
		quantity=quantity, price_per_one=price_per_one, price_per_all=price_per_all, vat_rate=vat_rate, item_type=item_type,
		seller=seller, uid=uid, ico=ico, cash_register_code=cash_register_code, issue_date=issue_date, created_date=created_date,
		customer_id=customer_id, dic=dic, ic_dph=ic_dph, invoice_number=invoice_number, okp=okp, paragon=paragon,
		paragon_number=paragon_number, pkp=pkp, receipt_no=receipt_no, type_receipt=type_receipt, tax_base_basic=tax_base_basic,
		tax_base_reduced=tax_base_reduced, total_price=total_price, free_tax_amount=free_tax_amount, vat_amount_basic=vat_amount_basic,
		vat_amount_reduced=vat_amount_reduced, vat_rate_basic=vat_rate_basic, vat_rate_reduced=vat_rate_reduced, owner=owner)
	r.save()

	recategorize_new_added_item(item, date_of_purchase_time_stamp)

def add_receipt_uid(date_of_purchase_time_stamp, uid_bill, seller, day_name, created_time, created_date, total_price, owner):
	
	r = ReceiptsIds(date_of_purchase_time_stamp=date_of_purchase_time_stamp, uid = uid_bill, seller=seller, day_name=day_name, 
					created_date=created_date, created_time=created_time, total_price=total_price, owner=owner)
	r.save()

def dashboar(request):
	'''
	app = dash.Dash(__name__)
	app.layout = html.Div(



		)
	'''
	#connection = sqlite3.connect('C:\\Users\\Marcel\\Desktop\\PYTHON\\citacka blockov\\nakupene polozky\\nakup.db')
	#connection = sqlite3.connect('C:\\Users\\Marcel\\Desktop\\PYTHON\\projekty\\django codemy\\myclub_website\\db.sqlite3')
	connection = sqlite3.connect('.\\db.sqlite3')

	

	#db = settings.DATABASES['default']['NAME']

	#connection = psycopg2.connect(db)
	
	'''

	connection = psycopg2.connect(
		host='ec2-3-212-143-188.compute-1.amazonaws.com',
		port=5432,
		database='d8uiap1g8fcu07',
		user='lonjswwxmkbryh',
		password='339cdf532849edde18b670be9681461c49cf3bb78745926642bcd503847fdbd6'
		)

	'''

	query = "SELECT * FROM events_items WHERE owner = '{}';".format(request.user.get_username())
	query2 = "SELECT * FROM events_category;"

	#df = pd.read_sql_query(query, connection)
	df = pd.read_sql(query, connection)
	df2 = pd.read_sql(query2, connection)

	df = df.join(df2.set_index('id'), on='category_id')

	df = df.sort_values(by='date_of_purchase_time_stamp', ascending=True)

	connection.close()

	fig_pie = px.pie(data_frame=df, names='seller', values='price_per_all')
	graph = fig_pie.to_html(full_html=False, default_height=500, default_width=700)

	# -----------------------

	fig_hist = px.histogram(data_frame=df, x='seller', y='price_per_all')
	fig_hist.update_layout(title="Pohľad: predajca / suma",
								xaxis_title="Predajca",
								yaxis_title="Suma",
								legend_title="Legenda:",
								#font=dict(
								#	family="Courier New, monospace",
								#	size=12,
								#	color="RebeccaPurple"
							)

	graph2 = fig_hist.to_html(full_html=False, default_height=500, default_width=700)

	# -----------------------

	fig_pie = px.pie(data_frame=df, names='name',
									values='price_per_all',
									title='Pohľad: jednotlivé kategórie v %',
									labels={'category_id':'Kategória',
											'price_per_all':'Celková suma'}
					)

	fig_pie.update_traces(textinfo='percent+label')
	
	graph3 = fig_pie.to_html(full_html=False)

	# -----------------------

	fig_hist = px.histogram(data_frame=df, x='date_of_purchase', y='price_per_all')
	graph4 = fig_hist.to_html(full_html=False, default_height=500, default_width=700)


	context = {'graph': graph, 'graph2':graph2, 'graph3':graph3, 'graph4':graph4}

	#return render(request, 'events/dashboar.html', {'fig_pie': fig_pie, fig_hist': fig_hist})
	return render(request, 'events/dashboar.html', context)

def dash_interactive(request):

	
	#db = settings.DATABASES['default']['NAME']

	#connection = psycopg2.connect(db)

	connection = sqlite3.connect('.\\db.sqlite3')

	'''
	connection = psycopg2.connect(
		host='ec2-3-212-143-188.compute-1.amazonaws.com',
		port=5432,
		database='d8uiap1g8fcu07',
		user='lonjswwxmkbryh',
		password='339cdf532849edde18b670be9681461c49cf3bb78745926642bcd503847fdbd6'
		)

	'''


	query = "SELECT * FROM events_items WHERE owner = '{}';".format(request.user.get_username())
	query2 = "SELECT * FROM events_category;"
	query3 = "SELECT id, name FROM events_subcategory_01;"

	df = pd.read_sql_query(query, connection)
	df2 = pd.read_sql(query2, connection)
	df3 = pd.read_sql(query3, connection)


	
	df = df.join(df2.set_index('id'), on='category_id')

	df = df.join(df3.set_index('id'), on='sub_category_01_id', rsuffix="_sc")

	df = df.sort_values(by='date_of_purchase_time_stamp', ascending=True)

	print(df)
	print(df2)
	print(df3)

	#print(df)
	#df = df.sort_values(by='date_of_purchase_time_stamp', ascending=True)

	connection.close()

	app = DjangoDash('DashInteractive')

	app.layout = html.Div([
	html.H1('Graf jednotlivé kategórie - detail'),


	dcc.Dropdown(id='choice',
				options=[{'label':x, 'value':x} for x in sorted(df.name.unique().astype(str))],
				value='Potraviny',),

	dcc.Dropdown(id='choice2',
				options=[{'label':x, 'value':x} for x in sorted(df.name_sc.unique().astype(str))],
				),

	dcc.Graph(id='my-graph', figure={})

	])

	@app.callback(
		Output(component_id='my-graph', component_property='figure'),
		Input(component_id='choice', component_property='value')
		)
	@app.callback(
		Output(component_id='choice2', component_property='figure'),
		Input(component_id='choice', component_property='value')
		)
	#def interactive_graphing(value):
	def display_value(value):
		print(value)
		#dff = df[df.category_id == value]
		dff = df[df.name == value]
		print(dff)
		#fig = px.pie(data_frame=dff, names='sub_category_01_id', values='price_per_all')
		fig = px.pie(data_frame=dff, names='name_sc', values='price_per_all')
		return fig

	return render(request, 'events/dash_interactive.html')
	#return {'data': [fig], 'layout': layout}


class ItemsListView(SingleTableView):
    model = Items
    table_class = ItemsTable
    form_class = ItemsUpdateCategoryForm
    context_object_name = 'category' #???
    #template_name = 'events/tabulka2.html'


class ItemsCreateView(CreateView):
	model = Items
	form_class = ItemsUpdateCategoryForm
	success_url = reverse_lazy('item_changelist')


class ItemUpdateView(UpdateView):
	model = Items
	form_class = ItemsUpdateCategoryForm
	success_url = reverse_lazy('item_changelist')

def load_sub_category_01(request):
	category_id = request.GET.get('category')
	sub_categoryes_01 = SubCategory_01.objects.filter(category_id=category_id).order_by('name')

	return render(request, 'events/sub_category_01_list_options.html', {'sub_categoryes_01':sub_categoryes_01})

def dash(request):
	
	
	db = settings.DATABASES['default']['NAME']

	connection = psycopg2.connect(db)

	'''
	connection = psycopg2.connect(
		host='ec2-3-212-143-188.compute-1.amazonaws.com',
		port=5432,
		database='d8uiap1g8fcu07',
		user='lonjswwxmkbryh',
		password='339cdf532849edde18b670be9681461c49cf3bb78745926642bcd503847fdbd6'
		)

	'''

	query = "SELECT * FROM events_items WHERE owner = '{}';".format(request.user.get_username())

	df = pd.read_sql_query(query, connection)
	df = df.sort_values(by='date_of_purchase_time_stamp', ascending=True)

	connection.close()

	df['id'] = df['date_of_purchase']
	df.set_index('id', inplace=True, drop=False)
	print(df.columns)

	#app = dash.Dash(__name__, prevent_initial_callbacks=True) # this was introduced in Dash version 1.12.0
	app = DjangoDash('Tabulka')


	# Sorting operators (https://dash.plotly.com/datatable/filtering)
	app.layout = html.Div([
		dash_table.DataTable(
			id='datatable-interactivity',
			columns=[
				{"name": i, "id": i, "deletable": True, "selectable": True, "hideable": True}
				if i == "iso_alpha3" or i == "year" or i == "id"
				else {"name": i, "id": i, "deletable": True, "selectable": True}
				for i in df.columns
			],
			hidden_columns = ['item_type', 'item_pre', 'ico', 'ic_dph', 'dic', 'cash_register_code', 'issue_date', 'invoice_number',
							 'customer', 'customer_id', 'okp', 'paragon', 'paragon_number', 'pkp', 'receipt_no', 'vat_amount_reduced',
							 'total_price', 'tax_base_basic', 'tax_base_reduced','total_price','free_tax_amount', 'vat_amount_basic', 
							 'vat_rate_basic', 'vat_rate_reduced', 'owner', 'type_receipt'],
			data=df.to_dict('records'),  # the contents of the table
			editable=True,              # allow editing of data inside all cells
			filter_action="native",     # allow filtering of data by user ('native') or not ('none')
			sort_action="native",       # enables data to be sorted per-column by user or not ('none')
			sort_mode="multi",         # sort across 'multi' or 'single' columns
			column_selectable="multi",  # allow users to select 'multi' or 'single' columns
			row_selectable="multi",     # allow users to select 'multi' or 'single' rows
			row_deletable=True,         # choose if user can delete a row (True) or not (False)
			selected_columns=[],        # ids of columns that user selects
			selected_rows=[],           # indices of rows that user selects
			page_action="native",       # all data is passed to the table up-front or not ('none')
			page_current=0,             # page number that user is on
			page_size=8,                # number of rows visible per page
			style_cell={                # ensure adequate header width when text is shorter than cell's text
				'minWidth': 95, 'maxWidth': 95, 'width': 95
			},
			style_cell_conditional=[    # align text columns to left. By default they are aligned to right
				{
					'if': {'column_id': c},
					'textAlign': 'left'
				} for c in ['item', 'date_of_purchase']
			],
			style_data={                # overflow cells' content into multiple lines
				'whiteSpace': 'normal',
				'height': 'auto'
			}
		),

		html.Br(),
		html.Br(),
		#html.Div(id='bar-container'),
		#html.Div(id='choromap-container')

	])

	table = ItemsTable(Items.objects.all())

	#return render(request, 'events/dash.html', {'app': app})
	return render(request, 'events/dash.html', {'table':table})

def add_receipt_uid_manual(request):

	form = ReceiptUidManual

	if request.method == 'POST':
		form = ReceiptUidManual(request.POST)

		if form.is_valid():

			print(form.cleaned_data['receipt_uid'])
			uid_bill = form.cleaned_data['receipt_uid']

			uid_receipts_2 = ReceiptsIds.objects.filter(uid = uid_bill)

			if uid_receipts_2:
				pass
			else:
				print('tu....')

				print(len(uid_bill))

				if len(uid_bill) == 34:

					print('Tu2:::')
					
					data_from_bill = check_recipt(uid_bill)

					print(data_from_bill['receipt']['issueDate'])
					print(data_from_bill['searchIdentification']['createDate'])
					print(data_from_bill['receipt']['organization']['name'])
					print(data_from_bill['receipt']['totalPrice'])

						
					seller = data_from_bill['receipt']['organization']['name']

					date_time_list = data_from_bill['receipt']['issueDate'].split(' ')
					
					created_date = date_time_list[0]
					created_time = date_time_list[1]

					day_name_en = datetime.strptime(created_date, '%d.%m.%Y').strftime('%a') #'Mon'

					days_translate = {'Mon': 'Pon', 'Tue': 'Ut', 'Wed': 'Str', 'Thu':'Štv', 'Fri':'Pia', 'Sat':'Sob', 'Sun':'Ned'}

					day_name = days_translate[day_name_en]

					date_of_purchase_time_stamp = time.mktime(time.strptime(data_from_bill['receipt']['createDate'], "%d.%m.%Y %H:%M:%S"))

					total_price = float(data_from_bill['receipt']['totalPrice'])
					owner = request.user.get_username()

					print(owner)

					add_receipt_uid(date_of_purchase_time_stamp=date_of_purchase_time_stamp, uid_bill=uid_bill, seller=seller, day_name=day_name,\
									created_time=created_time, created_date=created_date,\
									total_price=total_price, owner=owner)

					list_rows = grab_data(data_from_bill)

					#print(list_rows)
					#print(len(list_rows))

					for list_row in list_rows:
						#print(list_row)
						add_items(list_row, owner)


	variable = 'habakuka'

	return render(request, 'events/add_receipt_uid.html', {'variable':variable, 'form':form})

def recategorize_new_added_item(item, date_of_purchase_time_stamp):
	'''
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.postgresql_psycopg2',
	        'NAME': 'BASE_DATABASE',
	        'USER': 'postgres',
	        'PASSWORD': 'Marcelk0.',
	        'HOST': 'localhost',
	        'PORT': 5433,
	    }
	}
	'''

	'''

	conn = psycopg2.connect(
		host='ec2-3-212-143-188.compute-1.amazonaws.com',
		port=5432,
		database='d8uiap1g8fcu07',
		user='lonjswwxmkbryh',
		password='339cdf532849edde18b670be9681461c49cf3bb78745926642bcd503847fdbd6'
		)
	'''


	from django.conf import settings
	db = settings.DATABASES['default']['NAME']

	conn = psycopg2.connect(db)
	
	c = conn.cursor()

	query_1 = f"SELECT * FROM events_items WHERE item = '{item}';"
	c.execute(query_1)

	data = c.fetchall()

	if len(data) > 1:
		name = data[0][3]

		new_item_pretty = data[0][34]
		new_ean = data[0][35]
		new_class = data[0][36]
		new_sub_class = data[0][37]

		if new_class != None or new_sub_class != None:

			query_2 = f'''UPDATE events_items SET item_pretty = "{new_item_pretty}" WHERE item = "{name}" AND date_of_purchase_time_stamp = "{date_of_purchase_time_stamp}"'''
			query_3 = f'''UPDATE events_items SET ean = "{new_ean}" WHERE item = "{name}" AND date_of_purchase_time_stamp = "{date_of_purchase_time_stamp}"'''
			query_4 = f'''UPDATE events_items SET category_id = "{new_class}" WHERE item = "{name}" AND date_of_purchase_time_stamp = "{date_of_purchase_time_stamp}"'''
			query_5 = f'''UPDATE events_items SET sub_category_01_id = "{new_sub_class}" WHERE item = "{name}" AND date_of_purchase_time_stamp = "{date_of_purchase_time_stamp}"'''

			c.execute(query_2)
			c.execute(query_3)
			c.execute(query_4)
			c.execute(query_5)

			conn.commit()
			conn.close()

		conn.close()

	else:
		conn.close()

def recategorize(item_id):


	

	from django.conf import settings
	db = settings.DATABASES['default']['NAME']

	conn = psycopg2.connect(db)

	'''

	conn = psycopg2.connect(
		host='ec2-3-212-143-188.compute-1.amazonaws.com',
		port=5432,
		database='d8uiap1g8fcu07',
		user='lonjswwxmkbryh',
		password='339cdf532849edde18b670be9681461c49cf3bb78745926642bcd503847fdbd6'
		)

	'''

	c = conn.cursor()

	query_1 = f"SELECT * FROM events_items WHERE id = '{item_id}';"
	c.execute(query_1)

	data = c.fetchall()
	

	name = data[0][3]

	new_item_pretty = data[0][34]
	new_ean = data[0][35]
	new_class = data[0][36]
	new_sub_class = data[0][37]

	query_2 = f"UPDATE events_items SET item_pretty = '{new_item_pretty}' WHERE item = '{name}'"
	query_3 = f"UPDATE events_items SET ean = '{new_ean}' WHERE item = '{name}'"
	query_4 = f"UPDATE events_items SET category_id = '{new_class}' WHERE item = '{name}'"
	query_5 = f"UPDATE events_items SET sub_category_01_id = '{new_sub_class}' WHERE item = '{name}'"

	c.execute(query_2)
	c.execute(query_3)
	c.execute(query_4)
	c.execute(query_5)
	
	conn.commit()
	conn.close()

def update_item(request, item_id):
	item = Items.objects.get(pk=item_id)

	print('ja som update item')

	form = ItemsUpdateForm(request.POST or None, instance=item)

	if form.is_valid():
		
		form.save()
		print(item_id)
		#recategorize(item_id)
		print('prepisane')
		redirect_url = 'ukaz_blok/'+item.uid

		#stay here

		#return render(request, redirect_url)
		#return redirect('ukaz_blok', item.uid)
		#return HttpResponseRedirect('redirect_url')

	return render(request, 'events/update_item.html', {'item':item, 'form':form})

def category_item(request, item_id):
	item = Items.objects.get(pk=item_id)

	# 100 calls per day "category": "Food, Beverages & Tobacco > Food Items > Snack Foods > Cereal & Granola Bars > Cereal Bars",
	#'https://api.upcitemdb.com/prod/trial/lookup?upc=5000159407236'
	#'https://api.upcitemdb.com/prod/trial/lookup?upc=8593894904087'

	form = ItemsUpdateCategoryForm(request.POST or None, instance=item)

	if form.is_valid():
		
		form.save()

		messages.success(request, ('Zmeny boli uložené...'))

		#print(item_id)
		recategorize(item_id)
		#print('prepisane')
		redirect_url = 'ukaz_blok/'+item.uid

		#stay here

		#return render(request, redirect_url)
		#return redirect('ukaz_blok', item.uid)
		#return HttpResponseRedirect('redirect_url')

	return render(request, 'events/update_category_item.html', {'item':item, 'form':form})

def update_blok(request, recipe_id):
	items = Items.objects.filter(uid=recipe_id)

	form = ItemsUpdateForm(request.POST or None)

	return render(request, 'events/update_receipt.html', {'items' : items, 'form':form})

def ukaz_blok(request, recipe_id):
	items = Items.objects.filter(uid=recipe_id)

	for item in items:
		seller = item.seller
		created_date = item.created_date
		break

	return render(request, 'events/ukaz_blok.html', {'items' : items, 'seller':seller, 'created_date':created_date})

def zoznam_poloziek_bez_kategorie(request):

	items = Items.objects.filter(category_id=None)
	
	return render(request, 'events/all_without_category.html', {'items' : items})

def items_csv(request):
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=items.csv'

	#lines = ['Toto je lajka jedna;\n', 'Toto je lajka dva;\n', 'Toto je lajka tri;\n' ]

	# create csv writer
	writer = csv.writer(response)

	writer.writerow(["TimeStamp","Dátum","Položka","Množstvo","Cena za MJ","Cena celkom","DPH",
		"Kategoria","Pod kategoria","Predajca","Predajca IČO","Predajca DIČ","Predajca IČ-DPH"])

	#lines = []

	items = Items.objects.filter(owner = request.user.get_username()).order_by(str("date_of_purchase_time_stamp")).reverse()
	

	#lines.append('"TimeStamp";"Dátum";"Položka";"Množstvo";"Cena za MJ";"Cena celkom";"DPH";"Predajca";"Predajca IČO";"Predajca DIČ";"Predajca IČ-DPH";\n')

	'''
	for item in items:
		q = str(round(item.quantity, 2)).replace('.', ',')
		lines.append(f'"{item.date_of_purchase_time_stamp}";"{item.date_of_purchase}";"{item.item}";"{q}";"{item.price_per_one}";"{item.price_per_all}";"{item.vat_rate}";"{item.seller}";"{item.ico}";"{item.dic}";"{item.ic_dph}";\n')
	'''
	for item in items:
		quantity = str(item.quantity).replace('.', ',')
		price_per_one = str(round(item.price_per_one, 2)).replace('.', ',')
		price_per_all = str(round(item.price_per_all, 2)).replace('.', ',')
		vat_rate = str(item.vat_rate).replace('.', ',')
		

		if item.category_id:
			try:
				c = item.category
				#c = Category.objects.get(pk=c)
				s = item.sub_category_01
				#s = SubCategory_01.objects.get(pk=s)
			except AttributeError:
				c = item.category_id
				s = item.sub_category_01_id
			except TypeError:
				c = item.category_id
				s = item.sub_category_01_id
		else:
			c = item.category_id
			s = item.sub_category_01_id

		writer.writerow([item.date_of_purchase_time_stamp, item.date_of_purchase, item.item, 
						quantity, price_per_one, price_per_all,
						vat_rate, c, s, item.seller, item.ico, item.dic, item.ic_dph])
	

	#response.writelines(lines)

	return response

def zoznam(request):

	receipts = ReceiptsIds.objects.filter(owner = request.user.get_username()).order_by(str("date_of_purchase_time_stamp")).reverse()
	#receipts = ReceiptsIds.objects.order_by("date_of_purchase_time_stamp")
	#receipts = ReceiptsIds.objects.filter(owner = request.user.get_username()).order_by("created_date")
	
	# zmaz
	#print(len(receipts))
	# potialto

	'''
	sellers = []

	for i in range(len(receipts)):
		receipts_heads = Items.objects.filter(uid=receipts[i].uid)
		for head in receipts_heads:
			seller = head.seller
			sellers.append(seller)
			break

	print(receipts_heads)
	'''

	#return render(request, 'events/zoznam.html', {'receipts' : receipts, 'sellers': sellers})
	return render(request, 'events/zoznam.html', {'receipts' : receipts})

def search_item(request):

	search_term = request.POST['search_term']

	# https://stackoverflow.com/questions/739776/how-do-i-do-an-or-filter-in-a-django-query
	#result = Item.objects.filter(item.creator = owner) | Item.objects.filter(item.moderated = False)
	#
	# tento sposob znamena ze hladany vyraz musi byt 100% totozny a nachadzat sa v jednom alebo v druhom stlpci
	
	# nefunguje "unsupported operand type(s) for |: 'str' and 'QuerySet'"
	#results = Items.objects.filter(item__contains=search_term | Items.objects.filter(item_pretty__contains=search_term), owner = request.user.get_username())

	from django.db.models import Q

	# Item.objects.filter(Q(creator=owner) | Q(moderated=False))
	results = Items.objects.filter(Q(item__contains=search_term) | Q(item_pretty__contains=search_term), owner = request.user.get_username())

	if request.method == 'POST':
		return render(request, 'events/search_item.html', {'search_term': search_term, 'results':results})

	else:
		return render(request, 'events/search_item.html', {})

def show_venue(request, venue_id):
	venue = Venue.objects.get(pk=venue_id)
	#venue_owner = User.objects.get(pk=venue.owner)
	return render(request, 'events/show_venue.html', 
		{'venue': venue})#'venue_owner':venue_owner})

def add_venue(request):
	submitted = False
	if request.method == 'POST':
		form = VenueForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect('/add-venue?submitted=True')
	else:
		form = VenueForm
		if 'submitted' in request.GET:
			submitted = True

	return render(request, 'events/add_venue.html', {'form': form, 'submitted': submitted})

def all_events(request):
	event_list = Event.objects.all()
	return render(request, 'events/event_list.html',
		{'event_list': event_list})

def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	name = 'Ján'

	# convert month to number
	month = month.title() # month.capitalize()
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	# create calendar

	cal = HTMLCalendar().formatmonth(year, month_number)
	return render(request,
		'events/home.html', {
		'name': name,
		'year': year,
		'month': month,
		'month_number': month_number,
		'cal': cal
		})
