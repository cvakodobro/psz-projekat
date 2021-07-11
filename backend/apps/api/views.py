from django.shortcuts import render
from .lib.db_manager import DbManager
from .lib.knn import knn
import pandas as pd
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
import numpy as np


# Create your views here.


@api_view(['POST'])
def get_all(request):
    db = DbManager.Instance()
    con = db.create_engine()
    body = json.loads(request.body.decode('utf-8'))
    page = body['page']
    itemsPerPage = body['itemsPerPage']
    sortBy = body['sortBy']
    sortDesc = body['sortDesc']
    start = (page-1)*itemsPerPage
    end = page*itemsPerPage

    if len(sortBy) > 0:
        df = pd.read_sql(
            "select * from realestate order by {} {} limit {},{}".format(sortBy[0], 'desc' if sortDesc[0] == True else 'asc', start, itemsPerPage), con=con)
    else:
        df = pd.read_sql(
            "select * from realestate limit {},{}".format(start, itemsPerPage), con=con)
    result = df.fillna("").to_dict('records')
    return Response(result)


@api_view(['GET'])
def get_most_common(request):
    db = DbManager.Instance()
    con = db.create_engine()
    df_sell = pd.read_sql(
        """select block, count(*) as number from db.realestate where add_type = 's' and location='Beograd' group by block order by number desc limit 10""", con=con)
    result_sell_labels = df_sell.block
    result_sell_data = df_sell.number
    df_rent = pd.read_sql(
        """select block, count(*) as number from db.realestate where add_type = 'r' and location='Beograd' group by block order by number desc limit 10""", con=con)
    # result_rent = df_rent.to_dict('records')
    result_rent_labels = df_rent.block
    result_rent_data = df_rent.number
    df = pd.read_sql(
        """select block, count(*) as number from db.realestate where location='Beograd' group by block order by number desc limit 10""", con=con)
    # result_all = df.to_dict('records')
    result_all_labels = df.block
    result_all_data = df.number

    result = {
        "sell": {"labels": result_sell_labels, "data": result_sell_data},
        "rent": {"labels": result_rent_labels, "data": result_rent_data},
        "all": {"labels": result_all_labels, "data": result_all_data}
    }

    return Response(result)


@api_view(['GET'])
def get_props_by_size(request):
    db = DbManager.Instance()
    con = db.create_engine()
    df = pd.read_sql("""
    select x, count(*) as y from
	(SELECT size,
	CASE
		WHEN size <= 35 THEN 'Less than 35'
		WHEN size > 35 and size <= 50 THEN '36 - 50'
		WHEN size > 50 and size <= 65 THEN '51 - 65'
		WHEN size > 65 and size <= 80 THEN '66 - 80'
		WHEN size > 80 and size <= 95 THEN '81 - 95'
		WHEN size > 95 and size <= 110 THEN '96 - 110'
		WHEN size > 110 THEN 'More than 110'
    ELSE 'No size data'
	END AS x
	FROM db.realestate) a
    group by x
    """, con=con)
    result = df.to_dict('records')
    return Response(result)


@api_view(['GET'])
def get_props_by_year(request):
    db = DbManager.Instance()
    con = db.create_engine()
    df = pd.read_sql("""
    select x, count(*) as y from
	(SELECT year,
	CASE
		WHEN year < 1950 THEN 'Before 1951'
		WHEN year > 1950 and year <= 1960 THEN '1951 - 1960'
		WHEN year > 1960 and year <= 1970 THEN '1961 - 1970'
		WHEN year > 1970 and year <= 1980 THEN '1971 - 1980'
		WHEN year > 1980 and year <= 1990 THEN '1981 - 1990'
		WHEN year > 1990 and year <= 2000 THEN '1991 - 2000'
		WHEN year > 2000 and year <= 2010 THEN '2001 - 2010'
		WHEN year > 2010 and year <= 2020 THEN '2011 - 2020'
		WHEN year > 2020 THEN 'Aftrer 2021 (under construction)'
	END AS x
	FROM db.realestate) a
    where x is not null
    group by x   
    """, con=con)
    result = df.to_dict('records')
    return Response(result)


@api_view(['GET'])
def get_number_of_properties(request):
    db = DbManager.Instance()
    con = db.create_engine()
    df = pd.read_sql(
        'select count(*) as num from db.realestate where add_type = \'s\'', con=con)
    sell = df.num.iloc[0]
    df = pd.read_sql(
        'select count(*) as num from db.realestate where add_type = \'r\'', con=con)
    rent = df.num.iloc[0]
    df = pd.read_sql('select count(*) as num from db.realestate', con=con)
    all = df.num.iloc[0]
    result = {
        "sell": sell,
        "rent": rent,
        "all": all
    }
    return Response(result)


@api_view(['GET'])
def get_number_of_properties_by_city(request):
    db = DbManager.Instance()
    con = db.create_engine()
    df = pd.read_sql(
        'select location, COUNT(*) as number from db.realestate where add_type = \'s\' group by location order by number desc', con=con)
    df.location = df.apply(lambda x: x.location.title(), axis=1)
    result = df.fillna("").to_dict('records')
    return Response(result)

@api_view(['GET'])
def get_registration(request):
    db = DbManager.Instance()
    con = db.create_engine()
    house = pd.read_sql(
        "select registered, count(*) as number from db.realestate where property_type = 'h' group by registered", con=con)
    apartment = pd.read_sql(
        "select registered, count(*) as number from db.realestate where property_type = 'a' group by registered", con=con)
    h = house.fillna("").to_dict('records')
    a = apartment.fillna("").to_dict('records')
    print(h[2])
    result = {
        'houses': {
            'registered': h[2]['number'],
            'unregistered': h[1]['number'],
            'nodata': h[0]['number']
        },
        'apartments': {
            'registered': a[2]['number'],
            'unregistered': a[1]['number'],
            'nodata': a[0]['number']
        }
    }
    return Response(result)

@api_view(['GET'])    
def get_sell_rent_ratio(request):
    db = DbManager.Instance()
    con = db.create_engine()
    df = pd.read_sql("""
    select location, sell, rent, sell/rent, sell+rent as total from
	(select a.location as location, a.sell as sell, b.rent as rent from 
		(select location, count(*) as sell from db.realestate where add_type='s' group by location) as a
		left join
		(select location, count(*) as rent from db.realestate where add_type='r' group by location) as b 
		on a.location=b.location
	) a
    where location in 
        (select location from 
            (select location, count(*) as number from db.realestate group by location order by number desc limit 5) a
        )  
    """, con=con)
    result = df.to_dict('records')
    return Response(result)

@api_view(['GET'])
def get_props_by_price_category(request):
    db = DbManager.Instance()
    con = db.create_engine()
    df = pd.read_sql("""
    select x, count(*) as y from
        (SELECT price,
        CASE
            WHEN price < 49999 THEN 'Less then 49,999'
            WHEN price >= 50000 and price <= 99999 THEN '50,000 - 99,999'
            WHEN price >=100000 and price <= 149999 THEN '100,000 - 149,999'
            WHEN price >= 150000 and price <= 199999 THEN '150,000 - 199,999'
            WHEN price >=200000 THEN 'Greater then 200,000'
        ELSE 'No price data'
        END AS x
        FROM db.realestate where add_type='s') a
    group by x 
    """, con=con)
    result = df.fillna("").to_dict('records')
    return Response(result)


@api_view(['GET'])
def get_number_of_properties_with_parking(request):
    db = DbManager.Instance()
    con = db.create_engine()
    df = pd.read_sql("""
    select count(*) as parking from db.realestate where parking = 1 and add_type ='s' and location='Beograd'
    union
    select count(*) from db.realestate where add_type ='s' and location='Beograd'
    """, con=con)
    result = df.to_dict('list')
    return Response(result)

@api_view(['GET'])    
def get_top_30(request):
    db = DbManager.Instance()
    con = db.create_engine()
    df_a = pd.read_sql("""
    select location, price, url from db.realestate where property_type='a' and add_type='s' order by price desc limit 30
    """, con=con)
    df_h = pd.read_sql("""
    select location, price, url from db.realestate where property_type='h' and add_type='s' order by price desc limit 30
    """, con=con)
    result_a = df_a.fillna("").to_dict('records')
    result_h = df_h.fillna("").to_dict('records')
    result = {
        "houses": result_h,
        "apartments": result_a
    }
    return Response(result)

@api_view(['GET'])    
def get_top_100(request):
    db = DbManager.Instance()
    con = db.create_engine()
    df_a = pd.read_sql("""
    select property_type, location, size, price, url from db.realestate where property_type='a' order by size desc limit 100
    """, con=con)
    df_h = pd.read_sql("""
    select property_type, location, size, price, url from db.realestate where property_type='h' order by size desc limit 100
    """, con=con)
    result_a = df_a.fillna("").to_dict('records')
    result_h = df_h.fillna("").to_dict('records')
    result = {
        "houses": result_h,
        "apartments": result_a
    }
    return Response(result)

@api_view(['GET'])    
def get_2020(request):
    db = DbManager.Instance()
    con = db.create_engine()
    df_r = pd.read_sql("""
    select property_type, location, size, price, url from db.realestate where add_type='r' and year=2020 order by price desc
    """, con=con)
    df_s = pd.read_sql("""
    select property_type, location, size, price, url from db.realestate where add_type='s' and year=2020 order by price desc
    """, con=con)
    result_s = df_s.fillna("").to_dict('records')
    result_r = df_r.fillna("").to_dict('records')
    result = {
        "sell": result_s,
        "rent": result_r
    }
    return Response(result)

@api_view(['GET'])    
def get_top_30_rooms_area(request):
    db = DbManager.Instance()
    con = db.create_engine()
    df_r = pd.read_sql("""
    select location, property_type, add_type, price, rooms, url from db.realestate order by rooms desc limit 30
    """, con=con)
    df_a = pd.read_sql("""
    select location, add_type, area, price, url from db.realestate where property_type='h' order by area desc limit 30
    """, con=con)
    result_r = df_r.fillna("").to_dict('records')
    result_a = df_a.fillna("").to_dict('records')
    result = {
        "rooms": result_r,
        "area": result_a
    }
    return Response(result)


@api_view(['POST'])
def linear_regression(request):
    # coef = [0.06234250867109111, 0.18303986395649746, -0.07584340781035734, 0.1621612746711966, 0.04906277871235839, 0.02886093913553555, 0.03254728862143361]
    # min =[8.0, 0.0246945, 0.5, 10000]
    # max = [1350.0, 40.1904, 20.0, 1450000]


    # coef = [0.08046321470875929, 0.20532361015352923, -0.07975133541146963, 0.18806038225464353, 0.060185353301486146, 0.03457996434530676, 0.039478804953286116]
    # min = [8.0, 0.0246945, 0.5, 10000]
    # max = [1350.0, 9.9554, 20.0, 1450000]

    coef = [0.19444630693434317, 0.21701636913393632, -0.16081775246562435, 0.352622854640144, 0.14428806978293235, 0.08579726588914242, 0.09149714041624087]
    min = [8.0, 0.0246945, 0.5, 10000]
    max = [1200.0, 9.9554, 14.0, 499900]
    body = json.loads(request.body.decode('utf-8'))
    size = body['size']
    distance = body['distance']
    rooms = body['rooms']
    old = body['old']
    new = body['new']
    nodata = body['nodata']

    s_n = (float(size)-min[0])/(max[0]-min[0])
    d_n = (float(distance)-min[1])/(max[1]-min[1])
    r_n = (float(rooms)-min[2])/(max[2]-min[2])

    c_n = coef[0] + coef[1]*s_n + coef[2]*d_n +coef[3]*r_n + coef[4]*int(new) + coef[5]*int(old) +coef[6]*int(nodata)
    c = c_n*(max[3]-min[3]) + min[3]
    
    return Response(c)

@api_view(['POST'])
def knn_prediction(request):
    body = json.loads(request.body.decode('utf-8'))
    size = body['size']
    distance = body['distance']
    rooms = body['rooms']
    old_new = body['old_new']
    k = body['k'] if body['k'] != '' else None

    db = DbManager.Instance()
    con = db.create_engine()
    df = pd.read_sql("""select * from db.knn """, con=con)
    print(k)

    c = knn(df, np.array([float(size), float(distance), float(rooms), int(old_new)]), k)
    
    return Response(c)