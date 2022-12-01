from django.core.management.base import BaseCommand
from homeapp.models import *
import requests
import json

#exctract data from API
response = requests.get('https://engineering-task.elancoapps.com/api/raw')
parse_json = json.loads(response.text)

#setting up seeding of extracted data into local database
class Command(BaseCommand):

    def handle(self, *args, **options):
        Data.objects.all().delete()
        loading = 0

        for item in range(len(parse_json)):
            sample = Data(
                consumed_quantity=parse_json[item]["ConsumedQuantity"],
                cost = parse_json[item]["Cost"],
                date = parse_json[item]["Date"],
                instance_id = parse_json[item]["InstanceId"],
                meter_category = parse_json[item]["MeterCategory"],
                resource_group = parse_json[item]["ResourceGroup"],
                resource_location = parse_json[item]["ResourceLocation"],
                tags_app_name = parse_json[item]["Tags"]["app-name"],
                tags_environment = parse_json[item]["Tags"]["environment"],
                tags_business_unit = parse_json[item]["Tags"]["business-unit"],
                unit_of_measure = parse_json[item]["UnitOfMeasure"],
                location = parse_json[item]["Location"],
                service_name = parse_json[item]["ServiceName"],
            )
            sample.save()

            #this is just to see progress while seeding
            if int(100*item/len(parse_json)) > loading:
                loading = int(100*item/len(parse_json))
                print(loading, "%")
        self.stdout.write("done")
