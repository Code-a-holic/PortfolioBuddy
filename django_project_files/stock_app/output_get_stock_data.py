# This file gets the list of stocks from the database, retrieves the real-time stock values and saves them to G-Sheets.

from nselib import capital_market
from datetime import datetime
from .models import Stock_Data, Stock

def get_buy_price(username, stock_name):
    stock_query_set = Stock.objects.filter(user_name=username, stock_name=stock_name).first()
    print(type(stock_query_set))
    buy_price = stock_query_set.buy_price

    return buy_price

def getDate():
    today = datetime.now()
    date = today.strftime('%d')
    month = today.strftime('%b')
    year = today.strftime('%Y')

    return date + "-" + month + "-" + year

def getDay():
    today = datetime.now()
    return today.strftime("%A")

def get_specific_day_stock_data(stocks_list, from_date, to_date, username):

    break_button = False
    for i in stocks_list:
        data_dict = (capital_market.price_volume_and_deliverable_position_data(symbol=i, from_date=from_date, to_date=to_date)).to_dict()
        print(data_dict)

        total_date_count = data_dict["Date"].values()

        for i in range(len(total_date_count)):

            openPrice = data_dict["OpenPrice"][i]
            closePrice = data_dict["ClosePrice"][i]
            avgPrice = data_dict["AveragePrice"][i]
            turnoverInRs = data_dict["TurnoverInRs"][i]

            if type(openPrice) == str:
                openPrice = openPrice.replace(",", "")
            if type(closePrice) == str:
                closePrice = closePrice.replace(",", "")
            if type(avgPrice) == str:
                avgPrice = avgPrice.replace(",", "")
            if type(turnoverInRs) == str:
                turnoverInRs = turnoverInRs.replace(",", "")

            turn_over_in_cr = float(turnoverInRs) / 10000000

            open_price = float(openPrice)
            close_price = float(closePrice)

            percentage_difference = ((close_price - open_price) / open_price) * 100

            if data_dict["%DlyQttoTradedQty"][i] == "-" or data_dict["%DlyQttoTradedQty"][i] == " ":
                delivery_in_cr = 0
            elif type(data_dict["%DlyQttoTradedQty"][i]) is str:
                delivery_in_rs = (float(data_dict["%DlyQttoTradedQty"][i]) / 100) * float(turnoverInRs)
                delivery_in_cr = delivery_in_rs / 10000000
            else:
                delivery_in_rs = (data_dict["%DlyQttoTradedQty"][i] / 100) * float(turnoverInRs)
                delivery_in_cr = delivery_in_rs / 10000000

            if data_dict["%DlyQttoTradedQty"][i] == "-" or data_dict["%DlyQttoTradedQty"][i] == " ":
                delivery_percentage = 0
            elif type(data_dict["%DlyQttoTradedQty"][i]) is str:
                delivery_percentage = float(data_dict["%DlyQttoTradedQty"][i])
            else:
                delivery_percentage = data_dict["%DlyQttoTradedQty"][i]

            symbol = data_dict['ï»¿"Symbol"'][i]

            buy_price = get_buy_price(username, symbol)

            stock_data = {
                    "symbol": symbol,
                    "date": data_dict["Date"][i],
                    "openprice": float(openPrice),
                    "closeprice": float(closePrice),
                    "avgprice": float(avgPrice),
                    "turnover_in_cr": turn_over_in_cr,
                    "deliverypercentage": delivery_percentage,
                    "delivery_in_cr": delivery_in_cr,
                    "buy_price": buy_price,
                    "percentage_difference": percentage_difference
            }

            if not stock_data["date"]:  # In Python empty dict evaluates to "false" in an if statement.
                break_button = True

            else:
                result = send_to_db(stock_data, username)
                print("result")
                print(result)

            if break_button:

                file = open("../z_log_file.txt", "a")
                file.write(f"\nNo markets today")
                file.close()

                break

        if break_button:
            print("No data found!")
            print(data_dict)

            break
    print("Code run complete")

    file = open("../z_log_file.txt", "a")
    file.write(f"\nCode run complete\n\n")
    file.close()

def send_to_db(stock_data_input_1, username):
    stock_data = Stock_Data(username=username, symbol=stock_data_input_1["symbol"], date=stock_data_input_1["date"],
                            open_price=stock_data_input_1["openprice"], close_price=stock_data_input_1["closeprice"],
                            avg_price=stock_data_input_1["avgprice"], turn_over_in_cr=stock_data_input_1["turnover_in_cr"],
                            delivery_percentage=stock_data_input_1["deliverypercentage"], delivery_in_cr=stock_data_input_1["delivery_in_cr"],
                            buy_price=stock_data_input_1["buy_price"], percentage_difference=stock_data_input_1["percentage_difference"])
    stock_data.save()
    return "Added to dB."




