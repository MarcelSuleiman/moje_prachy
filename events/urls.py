from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('<int:year>/<str:month>/', views.home, name='home'),
    path('events', views.all_events, name='list-events'),
    path('add-venue', views.add_venue, name='add-venue'),
    path('camera', views.camera, name='camera'),
    path('camera_dvaadva', views.camera_dva, name='camera-dva'),
    path('video_stream', views.video_stream, name='video_stream'),
    path('dashboar', views.dashboar, name='dashboar'),
    path('nechodsem', views.nechodsem, name='nechodsem'),
    
    path('dash_interactive', views.dash_interactive, name='dash_interactive'),
    path('tabulka', views.ItemsListView.as_view()),
    path('tabulka2', views.ItemsListView.as_view()),
    path('zoznam', views.zoznam, name='zoznam'),
    path('add_receipt_uid', views.add_receipt_uid_manual, name='add-receipt-uid'),

    path('zoznam_bez_cat', views.zoznam_poloziek_bez_kategorie, name='zoznam-bez-cat'),

    path('ukaz_blok/<recipe_id>', views.ukaz_blok, name='ukaz-blok'),
    path('show_venue/<venue_id>', views.show_venue, name='show-venue'),
    path('update_blok/<recipe_id>', views.update_blok, name='update-blok'),
    path('update_item/<item_id>', views.update_item, name='update-item'),
    path('update_category_item/<item_id>', views.category_item, name='category-item'),

    path('search_item', views.search_item, name='search-item'),



    path('items_csv', views.items_csv, name='items-csv'),
    #path('', views.StudentListView.as_view(), name='student_changelist'),
    path('add/', views.ItemsCreateView.as_view(), name='student_add'),
    path('<int:pk>/', views.ItemUpdateView.as_view(), name='student_change'),
    path('ajax/load_sub_category_01/', views.load_sub_category_01, name='load_sub_category_01'),

    #path('table', views.table, name='table'),
]
