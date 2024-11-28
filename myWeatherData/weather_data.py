"""
该模块提供了一个天气数据类，用于在运行过程中缓存数据
"""

class WeatherData:
    '''
    该类每天气数据基础类
    使用了两种方式进行self。data的设置和管理
    '''
    def __init__(self):
        self.useful = False
        self.data={}

    def setup_now(self,data):
        '''
        本函数用于从now或forecast类信息建立天气数据
        :param data:数据源
        :return: 不返回任何值
        '''
        self.useful = True
        self.data = {
            'timesamps': data.get('obstime',data.get('fxTime','null')),
            'status': data['text'],
            'temperature':data.get('temp',0),
            'windDir': data['windDir'],
            'windScale': data['windScale'],
            'windSpeed': data['windSpeed'],
            'humidity' : data['humidity'],
            'vis': data.get('vis','null'),
            'pop': data.get('pop','null')
        }

    def setup_day(self,data):
        '''
        本函数用于从days类信息建立天气数据
        :param data:数据源
        :return: 不返回任何值
        '''
        self.useful = True
        self.data = {
            'timesamps': data.get('fxData','null'),
            'statusDay': data['textDay'],
            'statusNight': data['textNight'],
            'tempMax': data.get('tempMax', 0),
            'tempMin': data.get('tempMin', 0),
            'windDirDay': data['windDirDay'],
            'windDirNight': data['windDirNight'],
            'windScaleDay': data['windScaleDay'],
            'windScaleNight': data['windScaleNight'],
            'windSpeedDay': data['windSpeedDay'],
            'windSpeedNight': data['windSpeedNight'],
            'humidity': data['humidity'],
            'vis': data.get('vis', 'null'),
            'pop': data.get('pop', 'null')
        }
    def get_data(self):
        '''
        :return:自身所储存的天气数据
        '''
        if self.useful :
            return self.data
        return False
