
import json
import time

def get_val_str(line, begin=0):
    pos = line.find("{", begin)
    if pos < 0:
        return None, -1
    n = line[pos + 1]
    if n != '$' and n != '@':
        return None, pos + 1
    
    end = line.find("}", pos + 2)

    return line[pos + 1: end], pos
        

def get_val_str_list(line):
    begin = 0
    results = []
    while True:
        v, pos = get_val_str(line, begin)
        offset = 0
        # print(v, pos)
        if v:
            results.append((v, pos, pos + len(v) + 1))
            offset = len(v)
        if pos < 0:
            break

        begin = pos + offset
    return results

class Context:

    def __init__(self):
        self.return_value = None

    # All context share one current_time in seconds
    @staticmethod
    def set_time(current_time):
        Context.current_time = current_time

    def get_time(self):
        return Context.current_time

    def __getitem__(self, key):
        """
        TODO: 
        """
        if key == '$current_seconds':
            return self.get_time()
        elif key == '$pid':
            return os.getpid()
        elif key == '$today':
            return time.strftime('%Y-%m-%d', time.localtime(self.get_time()))
        elif key == '$now':
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.get_time()))

        if key in self.__dict__:
            return self.__dict__[key]
        raise Exception("No attr %s" % key)

    def __setitem__(self, key, value):
        self.__dict__[key] = value        

    def set_engine(self, engine):
        self.engine = engine

    def get_engine_var(self, var):
        if self.engine:
            return self.engine.get_value(var)
        return None

    def set_return_value(self, return_value):
        self.return_value = return_value

    def eval_val(self, val):
        if val[0] == '@':
            if val[1] == '@':   # @@val
                return self.get_engine_var(val[2:])
            else:   # @val
                pass
        elif val[0] == '$': # $current_seconds
            return self[val]

    def evaluate(self, expr):
        """
        eval the expr, 1. Append to an array; 2. join
        """
        vals = get_val_str_list(expr)
        last_begin = 0
        a = []
        for val, begin, end in vals:
            v = self.eval_val(val)
            a.append(expr[last_begin: begin])
            a.append(str(v))
            last_begin = end + 1
        a.append(expr[last_begin:])

        return "".join(a)

    def __str__(self):
        
        return "Context: %s %s" % (id(self), str(self.return_value))


if __name__ == '__main__':
    line = '{@main.a.b}{$a}-{$ab}{{@act.val}'
    v = get_val_str_list(line)
    print(v)
    for a, b, c in v:
        print(line[b+1: c])
