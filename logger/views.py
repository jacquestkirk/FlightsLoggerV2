from django.shortcuts import render
from django.http import HttpResponse
from logger.models import Flight_Info
import datetime
import time
from GoogleFlightsPoller import *


# Create your views here.

def index(request):
    return HttpResponse("Hello there") #todo: Add a readme here

def testDb(request):

    flightType = Flight_Info.TypeChoices.test
    price = 101
    flight_duration_departure_min = 67
    flight_duration_return_min = 93
    airline = 'Scandinavian'
    number_of_miles = 9000
    query_dateTime = datetime.datetime.now()
    origin = 'ORG'
    destination = 'DES'
    departing_date = datetime.date(year= 2017, month = 1, day = 20)
    return_date = datetime.date(year= 2017, month = 1, day = 25)
    departing_departing_time = datetime.datetime(year= 2017, month = 1, day = 20, hour= 23, minute = 6, second = 7)
    departing_arrival_time = datetime.datetime(year= 2017, month = 1, day = 20, hour= 5, minute = 6, second = 7)
    return_departing_time = datetime.datetime(year=2017, month=1, day=25, hour=23, minute=6, second=7)
    return_arrival_time = datetime.datetime(year=2017, month=1, day=25, hour=5, minute=6, second=7)
    query_duration_sec = 100

    flight = Flight_Info()

    flight.type = flightType
    flight.price = price
    flight.flight_duration_departure_min = flight_duration_departure_min
    flight.flight_duration_return_min = flight_duration_return_min
    flight.airline = airline
    flight.number_of_miles = number_of_miles
    flight.legs_departure = 7
    flight.legs_return = 5
    flight.query_dateTime = query_dateTime
    flight.origin = origin
    flight.destination = destination
    flight.departing_date = departing_date
    flight.return_date = return_date
    flight.departing_departing_time= departing_departing_time
    flight.departing_arrival_time = departing_arrival_time
    flight.return_departing_time = return_departing_time
    flight.return_arrival_time = return_arrival_time
    flight.query_duration_sec = query_duration_sec

    flight.save()


    return HttpResponse(str(flight))

def showDb(request):
    flightInfo = Flight_Info.objects.all()

    db_str = Flight_Info.header
    for flight in flightInfo:
        db_str = db_str + str(flight) + '<br/>' +'\r\n'

    return HttpResponse(db_str)

def QueryCheapestFlights(request):
    gfp = GoogleFlightsPoller()


    origin = 'AUS'
    destination = 'DAY'
    departing_date = datetime.date(year= 2017, month = 1, day = 20)
    return_date = datetime.date(year= 2017, month = 1, day = 25)

    gfp.BuildSlicesRoundTrip(origin=origin, destination=destination, depart_date_yyyy_mm_dd=str(departing_date),
                             return_date_yyyy_mm_dd=str(return_date))
    gfp.BuildRequest(num_passengers=1, num_responses=5)

    query_dateTime = datetime.datetime.now()
    time_query_start = time.time()
    gfp.SendQuery()

    query_duration_sec = time.time() - time_query_start

    gfp.GetPrices()
    price = min(gfp.prices)
    lowest_index = gfp.prices.index(price)

    departure_slice = gfp.response['trips']['tripOption'][lowest_index]['slice'][0]['segment']
    return_slice = gfp.response['trips']['tripOption'][lowest_index]['slice'][1]['segment']

    legs_departure = departure_slice.__len__()
    legs_return = return_slice.__len__()

    airline_list=[]
    number_of_miles = 0

    flight_duration_departure_min = 0
    for i in range(0, legs_departure):
        flight_duration_departure_min += departure_slice[0]['duration']
        if i < legs_departure-1: #add the layover time if this isn't the last leg
            flight_duration_departure_min += departure_slice[0]['connectionDuration']

        #check to see if the airline is already int the list, if it isn't add it
        if not(airline_list.__contains__(departure_slice[i]['flight']['carrier'])):
            airline_list.append(departure_slice[i]['flight']['carrier'])

        #add miles
        number_of_miles += departure_slice[i]['leg'][0]['mileage']

    flight_duration_return_min = 0
    for i in range(0, legs_return):
        flight_duration_return_min += return_slice[0]['duration']
        if i < legs_return-1: #add the layover time if this isn't the last leg
            flight_duration_return_min += return_slice[0]['connectionDuration']

        # check to see if the airline is already int the list, if it isn't add it
        if not (airline_list.__contains__(return_slice[i]['flight']['carrier'])):
            airline_list.append(return_slice[i]['flight']['carrier'])

        # add miles
        number_of_miles += return_slice[i]['leg'][0]['mileage']



    airline = ''

    for item in airline_list:
        airline += item + '/'

    departing_departing_time = datetime.datetime.strptime(departure_slice[0]['leg'][0]['departureTime'][0:16], '%Y-%m-%dT%H:%M')
    departing_arrival_time = datetime.datetime.strptime(departure_slice[1]['leg'][0]['arrivalTime'][0:16], '%Y-%m-%dT%H:%M')
    return_departing_time = datetime.datetime.strptime(return_slice[0]['leg'][0]['departureTime'][0:16], '%Y-%m-%dT%H:%M')
    return_arrival_time = datetime.datetime.strptime(return_slice[1]['leg'][0]['arrivalTime'][0:16], '%Y-%m-%dT%H:%M')

    flightType = Flight_Info.TypeChoices.cheapest

    flight = Flight_Info()

    flight.type = flightType
    flight.price = price
    flight.flight_duration_departure_min = flight_duration_departure_min
    flight.flight_duration_return_min = flight_duration_return_min
    flight.airline = airline
    flight.number_of_miles = number_of_miles
    flight.legs_departure = legs_departure
    flight.legs_return = legs_return
    flight.query_dateTime = query_dateTime
    flight.origin = origin
    flight.destination = destination
    flight.departing_date = departing_date
    flight.return_date = return_date
    flight.departing_departing_time = departing_departing_time
    flight.departing_arrival_time = departing_arrival_time
    flight.return_departing_time = return_departing_time
    flight.return_arrival_time = return_arrival_time
    flight.query_duration_sec = query_duration_sec

    flight.save()

    return HttpResponse(str(flight))
