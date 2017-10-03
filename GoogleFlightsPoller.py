#from Credentials import * #Warning: This is not pushed to source control
import requests
import json
import os
import datetime
from dateutil.parser import parse

class Segment:

    def __init__(self):
        self.OriginCode = ""
        self.DestinationCode = ""
        self.DepartureTime = -1
        self.ArrivalTime = -1
        self.CarrierCode = ""
        self.FlightNumber = -1
        self.CabinClass = -1
        self.SegmentDuration_min = -1
        self.OnTimePerformance = -1
        self.Mileage = -1


    def __repr__(self):
        repr_str = []
        repr_str.append("Origin Code: " + self.OriginCode)
        repr_str.append("Destination Code: " + self.DestinationCode)
        repr_str.append("Departure Time: " + str(self.DepartureTime))
        repr_str.append("Arrival Time: " + str(self.ArrivalTime))
        repr_str.append("Carrier Code: " + self.CarrierCode)
        repr_str.append("Flight Number: " + str(self.FlightNumber))
        repr_str.append("Cabin Class: " + str(self.CabinClass))
        repr_str.append("Segment Duration (min): " + str(self.SegmentDuration_min))
        repr_str.append("On Time Performance: " + str(self.OnTimePerformance))
        repr_str.append("Mileage: " + str(self.Mileage))

        return '\n'.join(repr_str)


class OneWayTrip:
    def __init__(self):
        self.price = -1
        self.OriginCode = ""
        self.DestinationCode = ""
        self.DepartureTime = -1
        self.ArrivalTime = -1
        self.SearchDate = -1
        self.duration_min = -1
        self.num_segments = -1
        self.Segments = []
        self.Layover1Durations_min = []
        self.notes = ""

    def __repr__(self):
        repr_str=  []
        repr_str.append("Price (USD): " + str(self.price))
        repr_str.append("Origin Code: " + self.OriginCode)
        repr_str.append("Destination Code: " + self.DestinationCode)
        repr_str.append("Departure Time: " + str(self.DepartureTime))
        repr_str.append("Arrival Time: " + str(self.ArrivalTime))
        repr_str.append("SearchDate: " + str(self.SearchDate))
        repr_str.append("Duration (min): " + str(self.duration_min))
        repr_str.append("numSegments: " + str(self.num_segments))
        repr_str.append("Segments (count): " + str(self.Segments.__len__()))
        repr_str.append("Layover Durations: " + str(self.Layover1Durations_min))
        repr_str.append("notes: " + self.notes)

        return '\n'.join(repr_str)

class GoogleFlightsPoller:

    TripList =[]

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

    def ParseResults(self):
        assert self.response != {}, 'Valid response has not been received'

        self.TripList = []

        num_responses = self.response['trips']['tripOption'].__len__()

        for i in range(0, num_responses):

            trip = OneWayTrip()

            #make sure it is a one way flight
            num_slices = self.response['trips']['tripOption'][i]['slice'].__len__()
            if num_slices > 1:
                trip.notes = "Error: ParseResults() only works on one way flights"
                self.TripList.append(trip)
                continue




            #build up each segment
            trip.num_segments = self.response['trips']['tripOption'][i]['slice'][0]['segment'].__len__()

            for n in range(0, trip.num_segments):

                #treat the legs as a separate segment
                num_legs = self.response['trips']['tripOption'][i]['slice'][0]['segment'][n]['leg'].__len__()
                trip.num_segments += num_legs -1

                for m in range(0,num_legs):
                    newSegment = Segment()

                    newSegment.OriginCode = self.response['trips']['tripOption'][i]['slice'][0]['segment'][n]['leg'][m]['origin']
                    newSegment.DestinationCode = self.response['trips']['tripOption'][i]['slice'][0]['segment'][n]['leg'][m]['destination']
                    newSegment.DepartureTime = parse(self.response['trips']['tripOption'][i]['slice'][0]['segment'][n]['leg'][m]['departureTime'])
                    newSegment.ArrivalTime = parse(self.response['trips']['tripOption'][i]['slice'][0]['segment'][n]['leg'][m]['arrivalTime'])
                    newSegment.CarrierCode = self.response['trips']['tripOption'][i]['slice'][0]['segment'][n]['flight']['carrier']
                    newSegment.FlightNumber = self.response['trips']['tripOption'][i]['slice'][0]['segment'][n]['flight']['number']
                    newSegment.CabinClass = self.response['trips']['tripOption'][i]['slice'][0]['segment'][n]['cabin']
                    newSegment.SegmentDuration_min = float(self.response['trips']['tripOption'][i]['slice'][0]['segment'][n]['leg'][m]['duration'])

                    if self.response['trips']['tripOption'][i]['slice'][0]['segment'][n].keys().__contains__('onTimePerformance'):
                        trip.Layover1Durations_min.append(float(self.response['trips']['tripOption'][i]['slice'][0]['segment'][n]['leg'][m]["onTimePerformance"]))

                    #OnTimePerformance = 0 #I don't know if this stuff has on time performance
                    newSegment.Mileage = float(self.response['trips']['tripOption'][i]['slice'][0]['segment'][n]['leg'][m]['mileage'])

                    if self.response['trips']['tripOption'][i]['slice'][0]['segment'][n].keys().__contains__('connectionDuration'):
                        trip.Layover1Durations_min.append(float(self.response['trips']['tripOption'][i]['slice'][0]['segment'][n]["connectionDuration"]))


                    trip.Segments.append(newSegment)



            # build up the trip
            string_price_w_units = self.response['trips']['tripOption'][i]['saleTotal']
            string_price = string_price_w_units.replace('USD', '')  # remove the USD substring
            trip.price = float(string_price)

            trip.SearchDate = datetime.datetime.now()
            trip.duration_min = self.response['trips']['tripOption'][i]['slice'][0]['duration']

            trip.OriginCode = trip.Segments[0].OriginCode
            trip.DestinationCode = trip.Segments[-1].DestinationCode
            trip.DepartureTime = trip.Segments[0].DepartureTime
            trip.ArrivalTime = trip.Segments[-1].ArrivalTime

            self.TripList.append(trip)






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


    #gfp.BuildSlicesRoundTrip(origin='AUS', destination='DAY', depart_date_yyyy_mm_dd='2018-01-20', return_date_yyyy_mm_dd='2018-01-25')
    gfp.ClearSliceList()
    gfp.BuildSlicesOneWay(origin='AUS', destination='DAY', date_yyyy_mm_dd='2017-12-23')
    #gfp.BuildSlicesRoundTripList(origin_list, destination_list,depart_date_list, arrival_date_list)
    print( 'number of slices: ' + str(gfp.sliceList.__len__()))
    gfp.BuildRequest( num_passengers= 1 , num_responses = 5)
    print('sending query')
    gfp.SendQuery()
    print('response received')

    #gfp.GetPrices()
    #print(gfp.prices)