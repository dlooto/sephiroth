
import time
import os
import re

LoggerSwitch_None       = 0
LoggerSwitch_Daily      = 1
LoggerSwitch_Monthly    = 2
LoggerSwitch_FileSize   = 3
LoggerSwitch_Restart    = 4



class Logger:
    """
    """

    
    def check_for_daily(self):
        return True

    def check_for_monthly(self):
        return True

    @staticmethod
    def check_for_filesize(self):
        if self.chars_count < self.switch_filesize:
            return False
        # TODO: New File
        return True

    @staticmethod
    def check_for_restart():
        return True


    def __init__(self, config):
        self.filename = None # Current file name
        self.file = None
        self.config = config

        self.last_log_time = None
        self.chars_count = 0
        if 'switch' in config:
            switch = config['switch']
            if switch == 'daily':
                self.switch_policy = LoggerSwitch_Daily
            elif switch == 'monthly':
                self.switch_policy = LoggerSwitch_Monthly
            elif switch.startswith('filesize'):
                self.switch_policy = LoggerSwitch_FileSize
                self.switch_filesize = switch[8:].strip() #TODO: Support MB
            elif switch == 'restart':
                self.switch_policy = LoggerSwitch_Restart
        else:
            self.switch_policy = LoggerSwitch_None  # Default

        self.switch_file()

    def make_filename(self, filename, path):
        time = Logger.get_formatted_time()
        today = time.split(' ')[0]
        month = today[0:7]

        filename = os.path.join(path, filename)

        filename = re.sub('{\$date}', today, filename)    
        filename = re.sub('{\$time}', time, filename)
        filename = re.sub('{\$month}', month, filename)

        return filename

    def switch_file(self):
        if self.file:
            self.file.close()
        self.filename = self.config['filename']
        self.path = self.config['path']

        filename = self.make_filename(self.filename, self.path)

        if self.switch_policy == LoggerSwitch_Restart:
            self.file = open(filename, "w+", encoding='utf8')
        else:
            self.file = open(filename, "a+", encoding='utf8')

        print(self.file)
        self.open_time = time.localtime(int(time.time()))
        self.chars_count = 0

    def try_switch_file(self):
        pass
        

    def __write_log_line(self, formatted_time, line):
        #TODO: Log level
        print(4)
        self.chars_count += self.file.write("[%s] %s\n" % (formatted_time, line))

    @staticmethod
    def get_formatted_time():
        current_second = int(time.time())
        current_time = time.localtime(current_second)
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', current_time)
        return formatted_time

    def write(self, line):
        """
        Interface for log lines
        """
        current_second = int(time.time())
        current_time = time.localtime(current_second)
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', current_time)

        # 只有日期变了才可能涉及到LoggerSwitch_Monthly或者LoggerSwitch_Daily
        if self.last_log_time and self.last_log_time.tm_yday != current_time.tm_yday:
            if self.switch_policy == LoggerSwitch_Daily:
                self.check_for_daily()
            elif self.switch_policy == LoggerSwitch_Monthly:
                self.check_for_monthly()
        elif self.switch_policy == LoggerSwitch_FileSize:
            self.check_for_filesize()

        self.__write_log_line(formatted_time, line)

        self.last_log_time = current_time





if __name__ == '__main__':
    config = {'filename': 'a1-{$date}.log', 'path': "/Users/healer/{$month}"}
    l = Logger(config)

    l.write("ddd")
    l.write("ddd")