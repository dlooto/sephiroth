

class Converters:

    func = dict()

    @staticmethod
    def register(converter_name):
        def __converter(func):
            Converters.func[converter_name] = func
        return __converter

    @staticmethod
    def get(converter_name):
        return Converters.func[converter_name]


@Converters.register('unixtime')
def formatted_time_to_unixtime(formatted_time):
    import time
    st = time.strptime(formatted_time, '%Y-%m-%d %H:%M:%S')
    return int(time.mktime(st))


@Converters.register('format_unixtime')
def unixtime_to_formatted_time(unixtime):
    import time
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(unixtime))

# Test code
# print(Converters.get('unixtime')('2017-07-29 00:11:22'))