import datetime
import time

from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import Stock, Link, Stock_Data
from .output_get_stock_data import get_specific_day_stock_data
from django.http import JsonResponse


# Create your views here.

def get_stock_list(request):
    stock_list = []
    stock_query_set = Stock.objects.filter(user_name=request.user.username).values()

    for x in stock_query_set:
        stock_list.append(x["stock_name"])

    return stock_list

def home(request):
    if request.user.is_authenticated:
        return redirect("landing_page")
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("landing_page")
            else:
                return render(request, "login.html", {'error': 'Invalid username or password!'})
        else:
            return render(request, "login.html")

def landing_page(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            add_stock = request.POST["add_stock"]
            buy_price = request.POST["buy_price"]
            share_quantity = request.POST["share_quantity"]
            delete_stock = request.POST["delete_stock"]

            username = request.user.username

            if delete_stock and (buy_price or add_stock or share_quantity):
                stock_list = get_stock_list(request)
                all_value_error = {
                    "error": "Please choose either add or delete function and not both!",
                    "stock_list": stock_list
                }
                return render(request, "landing_page.html", all_value_error)

            elif ((buy_price and not (add_stock or share_quantity)) or (add_stock and not (buy_price or share_quantity))
                  or (share_quantity and not (buy_price or add_stock))):
                stock_list = get_stock_list(request)
                missing_error = {
                    "error": "You must add stock name, quantity of shares and buy price to add the stock to your portfolio!",
                    "stock_list": stock_list
                }
                return render(request, "landing_page.html", missing_error)

            elif add_stock and buy_price and share_quantity:
                if Stock.objects.filter(user_name=username, stock_name=add_stock).first():
                    stock_list = get_stock_list(request)
                    duplicate_entry = {
                        "error": "Stock already added to portfolio",
                        "stock_list": stock_list
                    }
                    return render(request, "landing_page.html", duplicate_entry)
                else:
                    stock = Stock(user_name=username, stock_name=add_stock, buy_price=buy_price,
                                  share_quantity=share_quantity)
                    stock.save()
                    return redirect("landing_page")

            elif delete_stock:
                stock_data = Stock.objects.filter(user_name=request.user.username, stock_name=delete_stock).first()

                if stock_data is not None:
                    stock_data.delete()
                    return redirect("landing_page")
                else:
                    stock_list = get_stock_list(request)
                    context_dict = {
                        "error": "Stock not in portfolio",
                        "stock_list": stock_list
                    }
                    return render(request, "landing_page.html", context_dict)
            else:
                stock_list = get_stock_list(request)
                empty_context = {
                    "error": "Please add stock name to add or delete.",
                    "stock_list": stock_list
                }
                return render(request, "landing_page.html", empty_context)
        else:
            stock_list = get_stock_list(request)
            my_sheet_link = Link.objects.filter(user_name=request.user.username).first()  # Need to add db query

            if my_sheet_link is not None:
                lp_contents = {
                    'stock_list': stock_list,
                    'link': my_sheet_link.link
                }
                return render(request, "landing_page.html", lp_contents)
            else:
                lp_contents = {
                    'stock_list': stock_list,
                    'link_error': "Please add link to Google sheets in User Profile page."
                }
                return render(request, "landing_page.html", lp_contents)
    else:
        return redirect("home")

def delete_multiple(request):
    delete_list = request.POST.getlist("stock_list[]")
    if delete_list:
        for i in delete_list:
            stock = Stock.objects.filter(user_name=request.user.username, stock_name=i).first()
            stock.delete()
        return redirect("landing_page")
    else:
        stock_list = get_stock_list(request)
        empty_list = {
            "error": "Select at-least one stock from the list before clicking delete.",
            "stock_list": stock_list
        }
        return render(request, "landing_page.html", empty_list)

def days_between_dates(dt1, dt2):
    date_format = "%d-%m-%Y"
    a = time.mktime(time.strptime(dt1, date_format))
    b = time.mktime(time.strptime(dt2, date_format))
    delta = b - a
    return int(delta / 86400)

def run_sync(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            from_date = request.POST["from_date"]
            to_date = request.POST["to_date"]

            if from_date and to_date:
                stock_list = get_stock_list(request)

                f_date_obj = datetime.datetime.strptime(from_date, '%Y-%m-%d')
                from_date_1 = f_date_obj.strftime('%d-%m-%Y')

                t_date_obj = datetime.datetime.strptime(to_date, '%Y-%m-%d')
                to_date_1 = t_date_obj.strftime('%d-%m-%Y')

                today = datetime.datetime.today()

                # no_of_days = days_between_dates(from_date, to_date)

                if f_date_obj >= t_date_obj:
                    wrong_dates = {
                        "stock_list": stock_list,
                        "error": "Make sure from-date is lesser than to-date."
                    }
                    return render(request, "landing_page.html", wrong_dates)
                elif t_date_obj > today:
                    future_date_error = {
                        "stock_list": stock_list,
                        "error": "Make sure the to-date is not at a farther date than today's date."
                    }
                    return render(request, "landing_page.html", future_date_error)
                else:
                    output = get_specific_day_stock_data(stock_list, from_date_1, to_date_1, request.user.username)
                    run_complete = {
                        "stock_list": stock_list,
                        "output": output,
                        "output_msg": "Code run complete."
                    }
                    return render(request, "landing_page.html", run_complete)
            else:
                stock_list = get_stock_list(request)
                date_error = {
                    "stock_list": stock_list,
                    "error": "Choose from-date and to-date to get stock data."
                }
                return render(request, "landing_page.html", date_error)
def user_profile(request):
    if request.user.is_authenticated:
        return render(request, "user_profile_page.html", {'user': request.user})

def stock_table(request):
    if request.user.is_authenticated:
        stock_list = []
        stock = Stock_Data.objects.filter(username=request.user.username).values()
        for x in stock:
            stock_dict = {
                "stock_name": x["symbol"],
                "date": x["date"],
                "open_price": x["open_price"],
                "close_price": x["close_price"],
                "avg_price": x["avg_price"],
                "turn_over_in_cr": x["turn_over_in_cr"],
                "delivery_percentage": x["delivery_percentage"],
                "delivery_in_cr": x["delivery_in_cr"],
                "buy_price": x["buy_price"],
                "percentage_difference": x["percentage_difference"]
            }
            stock_list.append(stock_dict)

        return render(request, "stock_table.html", {"stock_list": stock_list})
def add_link(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            link = request.POST['link']

            if link:
                saved_link = Link(user_name=request.user.username, link=link)
                saved_link.save()
                return redirect("landing_page")
            else:
                no_link = {
                    'user': request.user,
                    'link_error': "Paste your sheets link before clicking submit."
                }
                return render(request, "user_profile_page.html", no_link)
        else:
            return redirect("home")
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return redirect("home")
        else:
            return render(request, "signup.html", {"error": "Passwords are not matching!"})
    else:
        return render(request, "signup.html")
def logout(request):
    auth.logout(request)
    return redirect("home")
def get_portfolio_data_pie_chart(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            stock_dict = {}

            stock = Stock.objects.filter(user_name=request.user.username).values()

            for x in stock:
                stock_name = x["stock_name"]
                share_quantity = x["share_quantity"]
                stock_dict[stock_name] = share_quantity

            final_dict = {"stock_data": stock_dict}
            return JsonResponse(final_dict)
    else:
        return redirect("home")
def get_stock_data_line_chart(request, stock_name):
    if request.user.is_authenticated:
        if request.method == "GET":
            stock_dict = {}

            symbol = ""

            stock_data = Stock_Data.objects.filter(username=request.user.username, symbol=stock_name).values()

            for x in stock_data:
                symbol = x["symbol"]
                current_price = x["close_price"]
                buy_price = x["buy_price"]
                turn_over = x["turn_over_in_cr"]
                delivery = x["delivery_in_cr"]
                date = x["date"]

                stock_dict[date] = {"current_price": current_price, "buy_price": buy_price, "turn_over_in_cr": turn_over, "delivery_in_cr": delivery}
            stock_dict["stock_name"] = symbol

            return JsonResponse(stock_dict)
    else:
        return redirect("home")
def get_stock_data_bar_chart(request, date):
    print("===========================================")
    print(date)
    if request.user.is_authenticated:
        if request.method == "GET":
            stock_dict = {}

            stock_data = Stock_Data.objects.filter(username=request.user.username, date=date).values()

            for x in stock_data:
                symbol = x["symbol"]
                turn_over_in_cr = x["turn_over_in_cr"]
                delivery_in_cr = x["delivery_in_cr"]
                date = x["date"]

                stock_dict[symbol] = {"delivery_in_cr": delivery_in_cr, "turn_over_in_cr": turn_over_in_cr, "date": date}
            return JsonResponse(stock_dict)
    else:
        return redirect("home")

def chart(request):
    if request.user.is_authenticated:
        portfolio_list = []
        date_list = []
        user_info = Stock.objects.filter(user_name=request.user.username).values()
        stock_data = Stock_Data.objects.filter(username=request.user.username).values()

        for i in user_info:
            portfolio_list.append(i["stock_name"])

        for j in stock_data:
            date_list.append(j["date"])

        data_dict = {"portfolio_list": portfolio_list, "date_list": date_list}
        return render(request, 'charts.html', data_dict)
    else:
        return redirect("home")
