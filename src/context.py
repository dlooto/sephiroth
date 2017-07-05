
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
        self.vars = dict()
        self.last_return_value = None

    # All context share one current_time in seconds
    @staticmethod
    def set_time(current_time):
        Context.current_time = current_time
    
    @staticmethod
    def get_time():
        return Context.current_time

    @staticmethod
    def get_global_var_value(var):
        if var == '$current_seconds':
            return Context.get_time()
        elif var == '$pid':
            return os.getpid()
        elif var == '$today':
            return time.strftime('%Y-%m-%d', time.localtime(Context.get_time()))
        elif var == '$now':
            return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(Context.get_time()))
        else:
            return None

    def set_engine(self, engine):
        self.engine = engine

    def get_engine_var(self, var):
        if self.engine:
            return self.engine.get_value(var)
        return None

    def set_context_var(self, var, value):
        self.vars[var] = value
        self.last_return_value = value

    def get_context_var(self, var):
        return self.vars[var]

    def get_last_return_value(self):
        return self.last_return_value

    def set_return_value(self, return_value):
        self.return_value = return_value

    def eval_val(self, var):
        if var[0] == '@':
            if var[1] == '@':   # @@val for engine var
                return self.get_engine_var(var[2:])
            else:   # @val
                return self.get_context_var(var[1:])
        elif var[0] == '$': # $current_seconds
            return Context.get_global_var_value(var)

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
