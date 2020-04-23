import requests

class covid_data:
    url = ''
    response = ''
    data = ''

    def __init__(self, country):
        self.url = 'https://pomber.github.io/covid19/timeseries.json'
        self.response = requests.get(self.url)
        self.data = self.response.json()
        self.country_data = self.data[country]

    def most_recent(self):
        return self.country_data[-1]

    def most_recent_confirmed(self):
        return self.country_data[-1]['confirmed']

    def most_recent_recovered(self):
        return self.country_data[-1]['recovered']    
    
    def most_recent_change_confirmed(self):
        today = self.country_data[-1]['confirmed']
        yesterday = self.country_data[-2]['confirmed']
        return today - yesterday

    def most_recent_change_recovered(self):
        today = self.country_data[-1]['recovered']
        yesterday = self.country_data[-2]['recovered']
        return today - yesterday

    def number_day_decreasing_confirmed(self):
        today = self.country_data[-1]['confirmed']
        counter = 0
        while (today < self.country_data[-1-counter]['confirmed']):
            today = self.country_data[-1-counter]['confirmed']
            counter += 1
        if counter == 0:
            outputString = "The number of cases of COVID-19 today increased from yesterday, with " + str(self.most_recent_change_confirmed()) + " new cases."
        else:
            outputString = "The number of new cases today declined to " + str(self.most_recent_change_confirmed()) + " which is the day " + str(counter) + "of declining new cases"
        return outputString
            
def main():
    us_data = covid_data("US")
    print(us_data.most_recent())
    print(us_data.most_recent_confirmed())
    print(us_data.most_recent_recovered())
    print(us_data.most_recent_change_confirmed())
    print(us_data.most_recent_change_recovered())
    print(us_data.number_day_decreasing_confirmed())


if __name__ =='__main__':
    main()