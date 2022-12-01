from django.shortcuts import render
from .models import Data
from django.views.generic import ListView


#controller for the index template
def index_view(request):
    context = {}
    resources = Data.objects.all().order_by('service_name').values()
    apps = Data.objects.all()

    context = {"data_list": apps, "resources": resources}
    return render(request, "homeapp/index.html", context)


#controller for the raw data table template
def raw_view(request):
    context = {}
    context["data_list"] = Data.objects.all()
    return render(request, "homeapp/table.html", context)


#controller that displays tables for specific applications
class DepthView(ListView):
    model = Data
    template_name = 'homeapp/table.html'
    
    def get_context_data(self):
        context = {}
        context['data_list'] = Data.objects.all().filter(tags_app_name=self.kwargs['slug'])
        return context


#returns total cost sum of query set
def totalCost(query_set):
    result = 0
    for i in query_set:
        result += float(i.cost)
    return result

#returns a list of numbers from 1 to 30 😅
def dateArray():
    date_array = []
    for i in range(30):
        date_array.append(i+1)
    return date_array

#returns average daily cost of query set
def average_daily_cost(query_set):
    sum = 0
    for i in costByDate(query_set):
        sum += i
    return sum/30


#Calculate sum of all costs associated with query_set per day
def costByDate(query_set):
    cost_by_date = []
    for l in range(30):
        sum = 0.0
        if l>8:
            data_by_date = query_set.filter(date=str(l+1)+"/11/2020")
            for m in data_by_date:
                sum += float(m.cost)
            cost_by_date.append(sum)
        else:
            data_by_date = query_set.filter(date="0"+str(l+1)+"/11/2020")
            for m in data_by_date:
                sum += float(m.cost)
            cost_by_date.append(sum)
    
    return cost_by_date

list_of_services = ["Logic Apps", "Azure App Service", "Storage", "Virtual Machines", "Virtual Machines Licenses", "Virtual Network", "Log Analytics", "Advanced Threat Protection", "Bandwidth", "Key Vault", "Azure Cosmos DB", "Redis Cache", "Container Registry", "Azure Database for PostgreSQL", "Azure Data Factory v2", "Security Center", "Insight and Analytics", "Advanced Data Security", "Azure DNS", "Azure Front Door Service", "Network Watcher", "Azure Cognitive Search", "API Management", "Power BI Embedded"]

#controller for the charts template for specific apps
class ChartsView(ListView):
    model = Data
    template_name = 'homeapp/charts.html'
    
    def get_context_data(self):
        app_data = Data.objects.all().filter(tags_app_name=self.kwargs['slug'])

        #Calculate sum of all costs associated with specific services for the app
        cost_array = []
        for i in list_of_services:
            service_data = app_data.filter(service_name=i)
            cost_array.append(totalCost(service_data))

        #Calculate ratio --> average daily cost across all apps: average daily cost for specific app
        avg1 = average_daily_cost(Data.objects.all())
        avg2 = average_daily_cost(app_data)
        ratio = avg1/avg2

        context = {'item':list_of_services, 'costs':cost_array, 'cost_by_date':costByDate(app_data), 'date_array':dateArray(), 'app':self.kwargs['slug'], 'word':"service", 'c_b_d_all':costByDate(Data.objects.all()), 'ratio': ratio}
        return context


#controller for charts template for all data
class ChartsAllView(ListView):
    model = Data
    template_name = 'homeapp/charts.html'

    def get_context_data(self):
        #Calculate sum of costs associated with each app in the database
        list_of_apps = ["Macao", "Delaware-deposit-Plastic", "index-Consultant-blue", "Integrated-SDD", "Accountability-Clothing", "Philippines-THX", "info-mediaries", "AI-Administrator-capability", "firewall-Towels-compressing", "Officer", "Triple-buffered-Brand", "program-compelling", "Corporate-Electronics", "Multi-tiered", "global-Rustic", "Cambridgeshire-next-Springs", "Bike-Hawaii-Naira", "Health", "seamless-Arkansas-payment", "Markets-payment-Shoes", "Solutions", "Industrial", "Locks-integrated", "EXE", "redundant-copy-action-items", "Regional-Table", "Licensed-Account-paradigms", "auxiliary-Granite", "calculating", "zero", "markets-reboot-Avon", "Account-Pizza-cross-media", "Computers", "Granite", "Computers-Fresh", "User-centric", "Palau-redundant-solution-oriented", "Dakota-Future-proofed-SCSI", "Maine-Avon", "Loti", "Wooden-Health", "Table-Flats-Electronics", "Territory-e-markets", "forecast-Games", "Gloves", "red-Facilitator", "1080p-Lock", "mobile-transmit", "interface-deliver"]
        cost_array = []
        for i in list_of_apps:    
            app_data = Data.objects.filter(tags_app_name=i)
            cost_array.append(totalCost(app_data))

        #Calculate sum of costs associated with every service
        service_costs = []
        for i in list_of_services:
            service_data = Data.objects.all().filter(service_name=i)
            service_costs.append(totalCost(service_data))        

        context = {'item':list_of_apps, 'costs':cost_array, 'cost_by_date':costByDate(Data.objects.all()), 'date_array':dateArray(), 'app': "all apps", 'service_costs':service_costs, 'list_of_services':list_of_services, 'word':"app"}
        return context
