import requests
import json
import pandas as pd
import datetime as dt
import os
path = os.path.dirname(os.path.realpath(__file__))

## for testing purposes
amazon_stocks = json.load(open(path + "/amazon_stocks_2y.json", 'r'))

class day:
    
    def __init__(self, date, close, avg, count) -> None:
        self.date = date
        self.close = close
        self.avg = avg
        self.count = count


    def calculate_avg(self):
        avg = ((self.avg * (self.count -1 )) + self.close) / self.count
        return avg


    def main(self):

        self.avg = self.calculate_avg()

        # return {
        #     "Date" : self.date,
        #     "Close Price" : self.close,
        #     "Moving Average" : self.avg
        # }
        return [self.date, self.close, self.avg]

    
def fetch(identifier):
    # url = "https://stock-prices2.p.rapidapi.com/api/v1/resources/stock-prices/2y"

    # querystring = {"ticker":f"{identifier}"}

    # headers = {
    #     "X-RapidAPI-Key": "INSERT PERSONAL API KEY HERE",
    #     "X-RapidAPI-Host": "stock-prices2.p.rapidapi.com"
    # }

    # try:
    #     response = requests.request("GET", url, headers=headers, params=querystring)
    #     return response.json()
    # except Exception as e:
    #     print(e)
    #     return {}

    return amazon_stocks


def main(identifier, no_days = 10):

    json_obj = fetch(identifier=identifier)
    if len(amazon_stocks.keys()) == 0:
    # if len(json_obj.keys()) == 0:
        print("Json response is empty")
        return

    initial_date = dt.date(2021,1,1)
    for item in list(json_obj.keys()):
        temp_datetime_obj = dt.datetime.strptime(item, '%Y-%m-%d').date()

        ## find the first available date after 2021
        if (initial_date - temp_datetime_obj).days <= 0 :
            initial_date = temp_datetime_obj
            print("First available date in 2021 is ", initial_date)
            break
    
    def first_available(date):

        last_date = dt.datetime.strptime(list(amazon_stocks.keys())[-1],'%Y-%m-%d').date()
        # last_date = dt.datetime.strptime(list(json_obj.keys())[-1],'%Y-%m-%d').date()
        if (date - last_date).days > 0 :
            return ''

        string_date = date.strftime("%Y-%m-%d")
        
        try:
            ## check if data is available for that day
            temp_day = json_obj[string_date]
            return date

        except KeyError:
            date = date + dt.timedelta(days = 1)
            date = first_available(date)

            return date
            

    avg = 0
    values = []
    for i in range(no_days):
        
        initial_date = first_available(initial_date)
        if initial_date == '':
            print("Only these days are available")
            break

        string_date = initial_date.strftime("%Y-%m-%d")
        
        temp_day = json_obj[string_date]
        
        temp_list = day(date = string_date, close=temp_day['Close'], avg = avg, count = i + 1).main()
        values.append(temp_list)

        initial_date = initial_date + dt.timedelta(days = 1)
        avg = temp_list[2]
    
    df = pd.DataFrame(values, columns=['Date','closing Price', 'Moving Average'])
    print(df)

    now = dt.datetime.now().isoformat()
    df.to_csv(path+f"/exported_data/At_{now}_for_{no_days}_days.csv",index=False)


if __name__ == '__main__':

    main(identifier="AMZN", no_days=100)