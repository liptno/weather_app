"""
这个模块提供了一个爬虫类，用于远程获取天气信息
"""

import json
import requests


class Crawler:
    '''本类提供了一个爬虫类，用于进行天气数据的获取'''
    def __init__(self):
        self._data_source = "https://restapi.amap.com/v3/weather/weatherInfo?"
        self._contry = 'china'
        self._key = "52321b51f4af44dbbdf9f0db438736f8"
        self.timeout = 5.0
        with open('config/adcode.json', 'r', encoding="utf-8") as file:
            self._adcode_data = json.load(file)

    def get_now_weather_data_from_name(self,provshi,city):
        '''
        :param provshi: 省份
        :param city: 城市
        '''
        adcode = self._adcode_data[provshi][city]

        return self.get_now_weather_data_from_adcode(adcode)

    def get_now_weather_data_from_adcode(self, adcode):
        '''
        :param adcode: 城市编码
        :param extensions: base(实时)/all(预测)
        :param output: 文件类型(默认为JSON，暂不支持其他数据类型)
        :return: dict 其内储存了文件相关信息
        '''
        idcode = self.get_location_id(adcode)
        weather_data_url = ("https://devapi.qweather.com/v7/weather/now?"
                          +"location="+idcode
                          +"&key="+self._key
                            )
        weather_data_net = requests.get(weather_data_url, timeout=self.timeout)
        weather_data_net.encoding = 'utf-8'
        weather_data=json.loads(weather_data_net.text)

        return weather_data['now']

    def get_24h_weather_data_from_name(self, provshi,city):
        '''
        :param provshi: 省份
        :param city: 城市
        '''
        adcode = self._adcode_data[provshi][city]

        return self.get_24h_weather_data_from_adcode(adcode)

    def get_24h_weather_data_from_adcode(self, adcode):
        '''
        :param adcode: 城市编码
        :param extensions: base(实时)/all(预测)
        :param output: 文件类型(默认为JSON，暂不支持其他数据类型)
        :return: dict 其内储存了文件相关信息
        '''
        idcode = self.get_location_id(adcode)
        weather_data_url = ("https://devapi.qweather.com/v7/weather/24h?"
                          +"location="+idcode
                          +"&key="+self._key
                            )
        weather_data_net = requests.get(weather_data_url, timeout=self.timeout)
        weather_data_net.encoding = 'utf-8'
        weather_data=json.loads(weather_data_net.text)

        return weather_data['hourly']

    def get_7d_weather_data_from_name(self, provshi,city):
        '''
        :param provshi: 省份
        :param city: 城市
        '''
        adcode = self._adcode_data[provshi][city]

        return self.get_7d_weather_data_from_adcode(adcode)

    def get_7d_weather_data_from_adcode(self, adcode):
        '''
        :param adcode: 城市编码
        :param extensions: base(实时)/all(预测)
        :param output: 文件类型(默认为JSON，暂不支持其他数据类型)
        :return: dict 其内储存了文件相关信息
        '''
        idcode = self.get_location_id(adcode)
        weather_data_url = ("https://devapi.qweather.com/v7/weather/7d?"
                          +"location="+idcode
                          +"&key="+self._key
                            )
        weather_data_net = requests.get(weather_data_url, timeout=self.timeout)
        weather_data_net.encoding = 'utf-8'
        weather_data=json.loads(weather_data_net.text)

        return weather_data['daily']

    def get_location_id(self, adcode):
        data_url = ('https://geoapi.qweather.com/v2/city/lookup?'+
                   'location='+str(adcode)+'&'+
                    'key='+self._key
                    )
        data_net = requests.get(data_url, timeout=self.timeout)
        data_net.encoding = 'utf-8'
        data = json.loads(data_net.text)
        return data['location'][0]['id']

    def useful_city_list(self):
        '''

        :return:字典格式的city_list:{pro:{city1,city2,...}}
        '''
        city_list = {}
        for pro, pro_city_list in self._adcode_data.items():
            city_list[pro] = list(pro_city_list.keys())
        return city_list
