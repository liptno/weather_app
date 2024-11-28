"""
本模块提供了一个天气预测类，其存储了5个天气数据，用于为天气预测提供数据
"""

from .weather_data import WeatherData
class WeatherForecast:
    '''
    本类包含一个含有5个weather_data类的列表用于存储天气预测信息
    '''
    def __init__(self):
        self.weather_datas = []
    def setup(self,data):
        '''
        用于使用数据进行初始化
        :param data:数据源
        :return: NULL
        '''
        self.weather_datas = []
        for i in range(5):
            hour_data = data[i]
            weather_data = WeatherData()
            weather_data.setup_now(hour_data)
            self.weather_datas.append(weather_data)
    def get_data(self):
        '''
        用于提供数据
        :return: 天气数据列表
        '''
        return self.weather_datas
