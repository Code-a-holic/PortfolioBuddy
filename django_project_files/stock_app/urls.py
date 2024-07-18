from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.home, name="home"),
    path('landing_page', views.landing_page, name="landing_page"),
    path('signup', views.signup, name="signup"),
    path('user_profile', views.user_profile, name="user_profile"),
    path('logout', views.logout, name="logout"),
    path('delete_multiple', views.delete_multiple, name="delete_multiple"),  # -> understand the use of each of the arguments
    path('add_link', views.add_link, name="add_link"),
    path('stock_table', views.stock_table, name="stock_table"),
    path('run_sync', views.run_sync, name="run_sync"),
    path('charts', views.chart, name='charts'),
    path('get_stock_data', views.get_portfolio_data_pie_chart, name='pie_chart'),
    path('current_price_vs_buy_price/<str:stock_name>', views.get_stock_data_line_chart, name="line_chart"),  # <str:stock> used for sending stock name from Js to Django
    path('one_day_multiple_stocks/<str:date>', views.get_stock_data_bar_chart, name="bar_chart")
]
