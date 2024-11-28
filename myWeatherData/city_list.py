"""
本模块提供了一个城市列表类，用于对所有城市信息进行管理，其内存储了当前
用户所选择的城市，城市数据，可以对外提供所选城市的天气信息
"""

import time
from crawler import Crawler
from .city import City

class CityList:
    '''
    城市列表篇类，存储了一个城市字典，其内数据为{pro:{city:City()}}
    提供了一些API用于获取数据和设置选择城市
    '''
    def __init__(self):
        self.city_list = {}
        self.crawler = Crawler()
        self.useful_city = self.crawler.useful_city_list()
        self.selected_pro = None
        self.selected_city = None

    def get_useful_city(self):
        '''提供可以选择的城市'''
        return self.useful_city

    def set_selected_pro(self, pro):
        '''设置选择的省份'''
        self.selected_pro = pro

    def get_selected_pro(self):
        '''提供当前选择的省份'''
        return self.selected_pro

    def set_selected_city(self, city):
        '''设置当前选择的城市'''
        self.selected_city = city

    def get_selected_city(self):
        '''提供当前选择的城市'''
        return self.selected_city

    def add_city(self, pro, city):
        '''为城市列表添加城市并为其初始化天气数据'''
        city_ = City(city)
        weather_data_now = self.crawler.get_now_weather_data_from_name(pro, city)
        city_.set_weather_data_now(weather_data_now)
        weather_data = self.crawler.get_7d_weather_data_from_name(pro, city)
        city_.set_weather_data(weather_data)
        weather_data_forcast = self.crawler.get_24h_weather_data_from_name(pro,city)
        city_.set_forecast_data(weather_data_forcast)
        city_.set_update_time(time.time())
        self.city_list[pro] = self.city_list.get(pro,{})
        self.city_list[pro][city] = city_

    def update_city_now(self):
        '''更新所选城市当前天气数据'''
        pro, city = self.selected_pro, self.selected_city
        try:
            city_ = self.city_list[pro][city]
        except KeyError:
            self.add_city(pro, city)
            city_ = self.city_list[pro][city]
        weather_data_now = self.crawler.get_now_weather_data_from_name(pro, city)
        city_.set_weather_data_now(weather_data_now)
        city_.set_update_time(time.time())

    def update_city_forecast(self):
        '''更新所选城市预测天气数据'''
        pro, city = self.selected_pro, self.selected_city
        try:
            city_ = self.city_list[pro][city]
        except KeyError:
            self.add_city(pro, city)
            city_ = self.city_list[pro][city]
        weather_data_forcast = self.crawler.get_24h_weather_data_from_name(pro, city)
        city_.set_forecast_data(weather_data_forcast)
        city_.set_update_time(time.time())

    def update_city_7d(self):
        '''更新所选城市长期天气预报'''
        pro, city = self.selected_pro, self.selected_city
        try:
            city_ = self.city_list[pro][city]
        except KeyError:
            self.add_city(pro, city)
            city_ = self.city_list[pro][city]
        weather_data = self.crawler.get_7d_weather_data_from_name(pro, city)
        city_.set_weather_data(weather_data)
        city_.set_update_time(time.time())

    def change_select_city(self, pro, city):
        '''更改选择城市'''
        if self.useful_city.get(pro,{}).get(city,False):
            self.selected_pro = (pro, city)
            if not (pro in self.city_list and city in self.city_list[pro]):
                self.add_city(pro,city)
            return True
        return False

    def get_weather_data_now(self):
        '''从Crawler获取当前城市天气'''
        self.update_city_now()
        city_ = self.city_list[self.selected_pro][self.selected_city]
        data = city_.get_weather_data_now()
        if data:
            return data
        print("error in get_weather_data_now")
        return False


    def get_weather_data_forecast(self):
        '''从Crawler获取当前城市天气预报'''
        self.update_city_forecast()
        city_ = self.city_list[self.selected_pro][self.selected_city]
        data = city_.get_weather_data_forecast()
        if data:
            return data
        print("error in get_weather_data_forecast")
        return False

    def get_weather_data(self):
        '''从Crawler获取当前城市7日天气预报'''
        self.update_city_7d()
        city_ = self.city_list[self.selected_pro][self.selected_city]
        data = city_.get_weather_data()
        if data:
            return data
        print("error in get_weather_data")
        return False
