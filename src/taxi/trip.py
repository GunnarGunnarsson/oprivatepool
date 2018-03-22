# coding=utf-8



class TaxiTrip(object):
    def __init__(self,
                 pickup_longitude,
                 pickup_latitude,
                 dropoff_longitude,
                 dropoff_latitude):
        self.pickup_longitude = pickup_longitude
        self.pickup_latitude = pickup_latitude
        self.dropoff_longitude = dropoff_longitude
        self.dropoff_latitude = dropoff_latitude


class GreenTaxiTrip(TaxiTrip):
    """ Documentation taken from http://www.nyc.gov/html/tlc/downloads/pdf/data_dictionary_trip_records_green.pdf.
    Seems incorrect/incomplete.

    VendorID A code indicating the LPEP provider that provided the record.
        1= Creative Mobile Technologies, LLC;
        2= VeriFone Inc.
    lpep_pickup_datetime The date and time when the meter was engaged.
    lpep_dropoff_datetime The date and time when the meter was disengaged.
    Passenger_count The number of passengers in the vehicle.
        This is a driver-entered value.
    Trip_distance The elapsed trip distance in miles reported by the taximeter.
    Pickup_longitude Longitude where the meter was engaged.
    Pickup_latitude Latitude where the meter was engaged.
    RateCodeID The final rate code in effect at the end of the trip.
        1= Standard rate
        2=JFK
        3=Newark
        4=Nassau or Westchester
        5=Negotiated fare
        6=Group ride
    Store_and_fwd_flag  This flag indicates whether the trip record was held in vehicle
                        memory before sending to the vendor, aka “store and forward,”
                        because the vehicle did not have a connection to the server.
                        Y= store and forward trip
                        N= not a store and forward trip
    Dropoff_longitude Longitude where the meter was timed off.
    Dropoff_latitude Latitude where the meter was timed off.
    Payment_type A numeric code signifying how the passenger paid for the trip.
                    1= Credit card
                    2= Cash
                    3= No charge
                    4= Dispute
                    5= Unknown
                    6= Voided trip
    Fare_amount The time-and-distance fare calculated by the meter.
    Extra                   Miscellaneous extras and surcharges. Currently, this only includes
                            the $0.50 and $1 rush hour and overnight charges.
                            MTA_tax $0.50 MTA tax that is automatically triggered based on the metered
                            rate in use.
    Improvement_surcharge   $0.30 improvement surcharge assessed on hailed trips at the flag
                            drop. The improvement surcharge began being levied in 2015.
    Tip_amount  Tip amount – This field is automatically populated for credit card
                tips. Cash tips are not included.
    Tolls_amount Total amount of all tolls paid in trip.
    Total_amount The total amount charged to passengers. Does not include cash tips.
    Trip_type A code indicating whether the trip was a street-hail or a dispatch
        that is automatically assigned based on the metered rate in use but
        can be altered by the driver.
        1= Street-hail
        2= Dispatch
    """

    def __init__(self,
                 vendor_id,
                 lpep_pickup_datetime,
                 lpep_dropoff_datetime,
                 store_and_fwd_flag,
                 ratecode_id,
                 pickup_longitude,
                 pickup_latitude,
                 dropoff_longitude,
                 dropoff_latitude,
                 passenger_count,
                 trip_distance,
                 fare_amount,
                 extra,
                 mta_tax,
                 tip_amount,
                 tolls_amount,
                 ehail_fee,
                 total_amount,
                 payment_type,
                 trip_type,
                 *empty_attributes):
        super(GreenTaxiTrip, self).__init__(pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude)

        self.vendor_id = vendor_id
        self.lpep_pickup_datetime = lpep_pickup_datetime
        self.lpep_dropoff_datetime = lpep_dropoff_datetime
        self.store_and_fwd_flag = store_and_fwd_flag
        self.ratecode_id = ratecode_id
        self.passenger_count = passenger_count
        self.trip_distance = trip_distance
        self.fare_amount = fare_amount
        self.extra = extra
        self.mta_tax = mta_tax
        self.tip_amount = tip_amount
        self.tolls_amount = tolls_amount
        self.ehail_fee = ehail_fee
        self.total_amount = total_amount
        self.payment_type = payment_type
        self.trip_type = trip_type
        self.empty_attributes = empty_attributes

    def __str__(self):
        return ",".join([self.vendor_id,
                         self.lpep_pickup_datetime,
                         self.lpep_dropoff_datetime,
                         self.store_and_fwd_flag,
                         self.ratecode_id,
                         self.pickup_longitude,
                         self.pickup_latitude,
                         self.dropoff_longitude,
                         self.dropoff_latitude,
                         self.passenger_count,
                         self.trip_distance,
                         self.fare_amount,
                         self.extra,
                         self.mta_tax,
                         self.tip_amount,
                         self.tolls_amount,
                         self.ehail_fee,
                         self.total_amount,
                         self.payment_type,
                         self.trip_type
                         ])


class GreenNewTaxiTrip(GreenTaxiTrip):
    def __init__(self, vendor_id, lpep_pickup_datetime, lpep_dropoff_datetime, store_and_fwd_flag, ratecode_id,
                 pickup_longitude, pickup_latitude, dropoff_longitude, dropoff_latitude, passenger_count, trip_distance,
                 fare_amount, extra, mta_tax, tip_amount, tolls_amount, ehail_fee, improvement_surcharge, total_amount,
                 payment_type, trip_type, *empty_attributes):
        super(GreenNewTaxiTrip, self).__init__(vendor_id, lpep_pickup_datetime, lpep_dropoff_datetime,
                                               store_and_fwd_flag, ratecode_id, pickup_longitude, pickup_latitude,
                                               dropoff_longitude, dropoff_latitude, passenger_count, trip_distance,
                                               fare_amount, extra, mta_tax, tip_amount, tolls_amount, ehail_fee,
                                               total_amount, payment_type, trip_type, empty_attributes)
        self.improvement_surcharge = improvement_surcharge

    @staticmethod
    def is_new_link(link):
        return '2016' in link or '2015' in link
