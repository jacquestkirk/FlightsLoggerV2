import datetime

import csv
class ListGenerators:

    def __init__(self):
        self.airportList = []
        self.outboundDateList = []
        self.returnDateList =[]

    def GenerateAirportList(self):
        #Betty: populate this with code for reading csv file of airports
        #self.airportList.append('AUS')
        #self.airportList.append('IAH')
        f = open("resources/List_AirportCodes.csv", 'rt')
        reader = csv.reader(f)
        for row in reader:
            self.airportList.append(row[0])
        return

    def GenerateFlightDateList(self, startSearch_days, duration_days):
        #Figure out the dates you need
        #Starting from today
        today = datetime.datetime.now()
        #look sartSearch_days out for duration_days
        start = today + datetime.timedelta (days = startSearch_days)
        finish = start + datetime.timedelta (days = duration_days)

        # search between start and finish

        #create a list of dates from start to finish
        allDateList = []
        dayToAdd = start
        while dayToAdd < finish:
            allDateList.append(dayToAdd)
            dayToAdd = dayToAdd + datetime.timedelta(days = 1)


        # look for weekend dates
        for day in allDateList:
            # only append if it is a Saturday, add the corresponding Sunday
            if (datetime.datetime.weekday(day)==5):
                self.outboundDateList.append(day)
                self.returnDateList.append(day + datetime.timedelta(days= 1))

        return

    def GetAirportList(self):
        return self.airportList

    def GetFlightDateList(self):
        return [self.outboundDateList, self.returnDateList]

if __name__ == "__main__":
    from ListGenerators import *
    listGenerator = ListGenerators()

    listGenerator.GenerateAirportList()
    airportList = listGenerator.GetAirportList()

    print "Airport List: "
    print airportList

    startSearch_days = 60
    duration_days = 30
    listGenerator.GenerateFlightDateList(startSearch_days, duration_days)
    flightDateList = listGenerator.GetFlightDateList()

    print "Outbound Date List: "
    print flightDateList[0]

    print "Return Date List"
    print flightDateList[1]


