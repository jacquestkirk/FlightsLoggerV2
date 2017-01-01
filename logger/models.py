from django.db import models

# Create your models here.

class Flight_Info(models.Model):

    header = 'Type,Price (USD),Flight Duration Departure(min),Flight Duration Return(min), Airline,Miles,Legs Departure,Legs Arrival,Query Time,Origin Airport,Destination Airport,Departing Date,Return Date,Departing Departure Time,Departing Arrival Time,Return Departure Time,Return Arrival Time,Query Time (sec)' + '<br/>' +'\r\n'

    class TypeChoices:
        cheapest = 'CHEAP'
        noLayover = 'NOLAY'
        test = 'TEST'

    typeChoicesTuple = (
        (TypeChoices.cheapest, 'Cheapest Flight'),
        (TypeChoices.noLayover, 'No Layover'),
        (TypeChoices.test, 'For Testing')
    )

    type = models.CharField(max_length= 5, choices= typeChoicesTuple)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    flight_duration_departure_min = models.IntegerField()
    flight_duration_return_min = models.IntegerField()
    airline = models.CharField(max_length=50)
    number_of_miles = models.IntegerField()
    legs_departure = models.IntegerField()
    legs_return = models.IntegerField()
    query_dateTime = models.DateTimeField(auto_now=False, auto_now_add=False)
    origin = models.CharField(max_length=5)
    destination = models.CharField(max_length=5)
    departing_date = models.DateField(auto_now=False, auto_now_add=False)
    return_date = models.DateField(auto_now=False, auto_now_add=False)
    departing_departing_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    departing_arrival_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    return_departing_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    return_arrival_time  = models.DateTimeField(auto_now=False, auto_now_add=False)
    query_duration_sec = models.IntegerField()

    def __str__(self):
        return self.type + ',' + str(self.price) + ',' + str(self.flight_duration_departure_min) + ',' + str(self.flight_duration_return_min) + ',' + self.airline + ',' +\
               str(self.number_of_miles) +',' + str(self.legs_departure) +',' + str(self.legs_return) + ',' +\
               str(self.query_dateTime) + ',' + self.origin + ',' + self.destination + ',' +\
               str(self.departing_date) + ',' + str(self.return_date) + ',' + str(self.departing_departing_time) + ',' + str(self.departing_arrival_time) + ',' + \
               str(self.return_departing_time) + ',' + str(self.return_arrival_time) + ',' + str(self.query_duration_sec)




