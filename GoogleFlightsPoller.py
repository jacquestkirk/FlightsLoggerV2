#from Credentials import * #Warning: This is not pushed to source control
import requests
import json
import os

class GoogleFlightsPoller:

    class TripType:
        OneWay = 0
        RoundTrip = 1

    def __init__(self):
        self.request = ''
        self.expected_num_responses = 0
        self.response = {}
        self.prices =[]
        self.sliceList = []

    def ClearSliceList(self):
        self.sliceList=[]

    def BuildSlicesOneWay(self, origin, destination, date_yyyy_mm_dd):
        slice1 = {
            "origin": origin,
            "destination": destination,
            "date": date_yyyy_mm_dd
        }

        self.sliceList = [slice1]

    def BuildSlicesRoundTrip(self, origin, destination, depart_date_yyyy_mm_dd , return_date_yyyy_mm_dd):
        slice1 = {
            "origin": origin,
            "destination": destination,
            "date": depart_date_yyyy_mm_dd
        }
        slice2 = {
            "origin": destination,
            "destination": origin,
            "date": return_date_yyyy_mm_dd
        }

        self.sliceList = [slice1, slice2]

    def BuildSlicesOneWayList(self, origin_list, destination_list, date_list_yyyy_mm_dd):
        for origin in origin_list:
            for destination in destination_list:
                for date in date_list_yyyy_mm_dd:
                    slice = {
                                "origin": origin,
                                "destination": destination,
                                "date": date
                            }
                    self.sliceList.append(slice)

    def BuildSlicesRoundTripList(self, origin_list, destination_list, depart_date_list_yyyy_mm_dd, return_date_list_yyyy_mm_dd):
        self.BuildSlicesOneWayList(origin_list, destination_list, depart_date_list_yyyy_mm_dd)
        self.BuildSlicesOneWayList(destination_list, origin_list, return_date_list_yyyy_mm_dd)

    def BuildRequest(self, num_passengers, num_responses  = 10):

        assert self.sliceList !=[] , 'trip origin and destination must be defined'

        params = {
            "request": {
                "slice": self.sliceList,
                "passengers": {
                    "adultCount": num_passengers
                },
                "solutions": num_responses,
                "refundable": False
            }
        }

        self.request = params
        self.expected_num_responses = num_responses
        print (self.request)

    def SendQuery(self):
        assert self.request != '' , "Request is not yet defined"

        key = os.environ.get('GOOGLE_FLIGHTS_API_KEY', 'AIzaSyD-4ygYT2eBqK1zqSXT5PxsnK6Hqq6u7ME')
        url = "https://www.googleapis.com/qpxExpress/v1/trips/search?key=" + key
        headers = {'content-type': 'application/json'}

        response = requests.post(url, data=json.dumps(self.request), headers=headers)
        self.response = response.json()
        print (self.response)

    def GetPrices(self):
        assert self.response != {} , 'Valid response has not been received'
        self.prices = []

        num_responses = self.response['trips']['tripOption'].__len__()

        for i in range(0,num_responses):
            string_price_w_units = self.response['trips']['tripOption'][i]['saleTotal']
            string_price = string_price_w_units.replace('USD', '') #remove the USD substring
            self.prices.append(float(string_price))

    def JsonifyResult(self):
        jsonified = self.response.__str__().replace("'",'"')
        jsonified = jsonified.replace('Chicago O"Hare', "Chicago O'Hare")
        jsonified = jsonified.replace('True', '"TRUE"')
        return jsonified



if __name__ == "__main__":
    from GoogleFlightsPoller import *
    gfp = GoogleFlightsPoller()


    origin_list = ['AUS']
    destination_list = ['ORD']
    depart_date_list = ['2018-01-01','2018-01-02','2018-01-03','2018-01-04','2018-01-05']
    arrival_date_list = ['2018-01-06', '2018-01-07','2018-01-08','2018-01-09','2018-01-10']

    #gfp.BuildSlicesOneWay(origin = 'AUS', destination = 'DAY', date_yyyy_mm_dd = '2017-01-20')
    #gfp.BuildSlicesRoundTrip(origin='AUS', destination='DAY', depart_date_yyyy_mm_dd='2018-01-20', return_date_yyyy_mm_dd='2018-01-25')
    gfp.ClearSliceList()
    gfp.BuildSlicesRoundTripList(origin_list, destination_list,depart_date_list, arrival_date_list)
    print( 'number of slices: ' + str(gfp.sliceList.__len__()))
    gfp.BuildRequest( num_passengers= 1 , num_responses = 1)
    print('sending query')
    gfp.SendQuery()
    print('response received')

    #gfp.GetPrices()
    #print(gfp.prices)