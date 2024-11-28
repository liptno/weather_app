"""这个模块提供一个shell窗口用于对天气进行预报，稍微改动后
可以称为优质的数据提供模块用于给UL模块提供数据
"""
import datetime
from myWeatherData import city_list


class WorkShell:
    '''
    本类实现了一个shell窗口用于对天气进行预报
    其中准备了help，pro，city，weather4个指令
    具体请使用cmd ?来查看具体功能
    '''
    def __init__(self):
        '''
        初始化：
        state:当前状态
        city_list:城市列表CityList对象
        useful_city:储存可用城市与省份的信息
        useful_pro:储存可用省份信息
        pro:当前省份，初始设置为北京
        city:当前城市,初始设置为北京市
        '''
        self.state = "prepare"
        self.city_list = city_list.CityList()
        self.useful_city = self.city_list.get_useful_city()
        self.useful_pro = list(self.useful_city.keys())
        self.pro = self.useful_pro[0]
        self.city = list(self.useful_city[self.pro])[0]
        self.city_list.set_selected_city(self.city)
        self.city_list.set_selected_pro(self.pro)


    def setup(self,json):
        '''初始化'''
        return json

    def end(self):
        """
        TODO
        将信息保存至config/下
        """
        return 0

    def run(self):
        '''运行函数'''
        self.state = "run"
        while self.state != "end":
            cmd = input("weather app >")
            if cmd == '':
                continue
            argv = cmd.split()
            argc = len(argv)
            if not self.cmd_exec(argc, argv):
                print("Invalid cmd")
        self.end()

    def help(self):
        '''
        TODO 输出你所拥有的指令何其对应的格式
        '''
        print("there are some cmd we have")
        print("weather ...")

    def weather_help(self):
        '''
        TODO
        输出weather对应的help
        '''
        print("There is the weather help")

    def pro_help(self):
        '''
        TODO
        输出pro对应的help
        '''
        print("There is the pro help")

    def weather_now(self):
        '''获取当前天气信息并输出'''
        data = self.city_list.get_weather_data_now()
        for key, value in data.items():
            if value!="null":
                print(key,value,sep="=  ")

    def weather_forecast(self):
        '''获取最近几小时的预测天气信息并输出'''
        data_list = self.city_list.get_weather_data_forecast()
        hours = 0
        print("--------------------------------------")
        for data_ in data_list:
            data = data_.get_data()
            print("hour: ", hours)
            for key, value in data.items():
                if value!="null":
                    print(key,value,sep="=  ")
            hours += 1
            print("--------------------------------------")

    def weather_days(self):
        '''从city_list获取多天的天气信息列表并循环输出'''
        data_list = self.city_list.get_weather_data()
        days = 0
        print("--------------------------------------")
        for data_ in data_list:
            data = data_.get_data()
            print("day: ", days)
            for key,value in data.items():
                if value!="null":
                    print(key,value,sep="=  ")
            days += 1
            print("--------------------------------------")

    def set_pro(self, pro):
        '''检查省份是否存在,设定省份信息'''
        if pro in self.useful_pro:
            self.pro = pro
            self.city_list.set_selected_pro(pro)
            self.city = self.useful_city[self.pro][0]
            self.city_list.set_selected_city(self.city)
            return True
        return False

    def set_city(self, city, pro=False):
        '''设定目标城市信息'''
        if not pro:
            pro = self.pro
        #检查城市是否存在
        if city in self.useful_city[pro]:
            self.city = city
            self.city_list.set_selected_city(city)
            return True
        return False

    def show_useful_pro(self):
        '''展示所有可用省份'''
        for pro in self.useful_pro:
            print(pro, end=" ")
        print()

    def show_useful_city(self):
        '''展示对应省份下的可用城市'''
        for city in self.useful_city[self.pro]:
            print(city, end=" ")
        print()

    def weather_all(self):
        '''获取所有天气信息'''
        self.weather_now()
        self.weather_forecast()
        self.weather_days()

    def weather_cmd_exec(self, argc, argv):
        '''天气指令处理'''
        #处理help或无指令
        if argc == 1:
            print(f"省份:{self.pro}，城市{self.city},当前时间:{datetime.datetime.now()}")
            self.weather_now()
            return True
        #处理天气信息展示指令
        if argc == 2:
            if argv[1] == "?":
                self.weather_help()
                return True
            print(f"省份:{self.pro}，城市:{self.city},当前时间:{datetime.datetime.now()}")
            weather_type = argv[1].split(",")
            weather_type_use = {"now": False, "forecast": False, "7d": False, "all": False}
            #针对all进行处理
            if "all" in weather_type:
                self.weather_all()
                return True
            #针对now，forecast，days处理
            for i in weather_type:
                if i == "now":
                    if weather_type_use[i]:
                        continue
                    weather_type_use[i] = True
                    self.weather_now()
                if i in ("fc", "forecast"):
                    if weather_type_use["forecast"]:
                        continue
                    weather_type_use["forecast"] = True
                    self.weather_forecast()
                if i == "days":
                    if weather_type_use["7d"]:
                        continue
                    self.weather_days()
            return True
        #处理失败
        print("Invalid cmd")
        return False

    def pro_cmd_exec(self, argc, argv):
        '''省份指令处理'''
        if argc == 1:
            print(self.city_list.selected_pro)
        else:
            if argv[1] == "?":
                self.show_useful_pro()
                return True
            if argv[1] == "now" and argc == 2:
                print(self.city_list.selected_pro)
            elif argv[1] == "set" and argc == 3:
                if not self.set_pro(argv[2]):
                    print("Invalid province. Useful provinces:")
                    self.show_useful_pro()
            else:
                return False
        return True

    def city_cmd_exec(self, argc, argv):
        '''城市指令处理'''
        if argc == 1:
            print(self.city_list.selected_city)
        else:
            if argv[1] == "?":
                self.show_useful_city()
                return True
            if argv[1] == "now" and argc == 2:
                print(self.city_list.selected_city)
            elif argv[1] == "set" and argc == 3:
                if not self.set_city(argv[2]):
                    print("Invalid city. Useful city:")
                    self.show_useful_city()
            else:
                return False
        return True

    def cmd_exec(self, argc, argv):
        '''

        :param argc:指令个数
        :param argv:指令列表
        :return: 是否执行成功
        指令 q:退出
            help:帮助
            pro:省份相关
            city:城市相关
            we/wether:获取天气
        '''
        cmd = argv[0]
        if cmd == "q":
            self.state = "end"
            return True
        if cmd == "help":
            self.help()
            return True
        if cmd == "pro":
            return self.pro_cmd_exec(argc, argv)
        if cmd == "city":
            return self.city_cmd_exec(argc, argv)
        if cmd in ("we", "weather"):
            return self.weather_cmd_exec(argc, argv)
        return False

A = WorkShell()
A.run()
