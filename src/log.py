
import time
import os
import re

LoggerSwitch_None       = 0
LoggerSwitch_Daily      = 1
LoggerSwitch_Monthly    = 2
LoggerSwitch_Restart    = 4

class Logger:
    """
    if filename contains {$date}, means switch log file daily, 
    if filename contains {$month}, means switch log file monthly,
    if filename contains {$pid}, means switch log file when restart, NOT appending
    
    """

    def check_for_daily(self):
        self.switch_file()
        return True

    def check_for_monthly(self):
        self.switch_file()
        return True


    def __init__(self, config):
        self.filename = None # Current file name
        self.file = None
        self.config = config

        self.last_log_time = None
        self.chars_count = 0
        self.lines_count = 0

        print(self.config)
        
        self.switch_policy = LoggerSwitch_None
        self.filename_pattern = os.path.join(self.config['path'], self.config['filename'])
        if '{$date}' in self.filename_pattern:
            self.switch_policy = LoggerSwitch_Daily
        elif '{$month}' in self.filename_pattern:
            self.switch_policy = LoggerSwitch_Monthly
        
        if '{$pid}' in self.filename_pattern:
            self.switch_policy |= LoggerSwitch_Restart

        self.switch_file()

    def make_filename(self):
        time = Logger.get_formatted_time()
        today = time.split(' ')[0]
        month = today[0:7]

        filename = self.filename_pattern
        if self.switch_policy & LoggerSwitch_Daily or\
           self.switch_policy & LoggerSwitch_Monthly:
            filename = re.sub('{\$date}', today, filename)
            filename = re.sub('{\$month}', month, filename)
        if self.switch_policy & LoggerSwitch_Restart:
            filename = re.sub('{\$pid}', str(os.getpid()), filename)

        return filename

    def switch_file(self):
        if self.file:
            self.file.close()

        filename = self.make_filename()

        if self.switch_policy & LoggerSwitch_Restart:
            self.file = open(filename, "w+", encoding='utf8')
        else:
            self.file = open(filename, "a+", encoding='utf8')

        self.open_time = time.localtime(int(time.time()))
        self.chars_count = 0

    def try_switch_file(self):
        pass
        

    def __write_log_line(self, formatted_time, line):
        #TODO: Log level
        self.chars_count += self.file.write("[%s] %s\n" % (formatted_time, line))
        self.lines_count += 1
        if self.lines_count % 1 == 0:
            self.file.flush()

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
            if self.switch_policy & LoggerSwitch_Daily:
                self.check_for_daily()
            elif self.switch_policy & LoggerSwitch_Monthly:
                self.check_for_monthly()
        
        
        self.__write_log_line(formatted_time, line)

        self.last_log_time = current_time





if __name__ == '__main__':
    config = {'filename': 'a1-{$date}-#.log', 'path': "/Users/healer/{$month}"}
    l = Logger(config)
    print(l)
    l.write("ddd")
    l.write("ddd")