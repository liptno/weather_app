"""
本模块提供了一个City类，用于储存一个城市的天气数据
"""

from .weather_data import WeatherData
from .weather_forecast import WeatherForecast


class City:
    '''
    本类为城市类，用于储存城市的当前天气数据，天气预测数据，往后7天的天气数据
    '''
    def __init__(self,city):
        self.name = city
        self.weather_forecast_data = WeatherForecast()
        self.weather_data = []
        self.weather_data_now = WeatherData()
        self.update_time = 0

    def set_update_time(self,time):
        '''更新时间戳'''
        self.update_time = time

    def get_update_time(self):
        '''获取时间戳'''
        return self.update_time

    def set_forecast_data(self,data):
        '''设置天气预测数据'''
        self.weather_forecast_data.setup(data)

    def set_weather_data(self,data):
        '''设置长时间天气数据'''
        self.weather_data = []
        for day in data:
            weather_data = WeatherData()
            weather_data.setup_day(day)
            self.weather_data.append(weather_data)

    def set_weather_data_now(self,data):
        '''设置当前天气数据'''
        self.weather_data_now.setup_now(data)

    def get_weather_data_now(self):
        '''对外部提供当前天气数据'''
        return self.weather_data_now.get_data()

    def get_weather_data_forecast(self):
        '''提供天气预测数据'''
        return self.weather_forecast_data.get_data()

    def get_weather_data(self):
        '''提供长期天气预报'''
        return self.weather_data
