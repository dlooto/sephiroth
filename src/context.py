
import json
import time
from functools import reduce

def get_val_str(line, begin=0):
    """
    Strings parsing to fetch one variable
    """
    pos = line.find("{", begin)
    if pos < 0:
        return None, -1
    n = line[pos + 1]
    if n != '$' and n != '@':
        return None, pos + 1
    
    end = line.find("}", pos + 2)

    return line[pos + 1: end], pos
        

def get_val_str_list(line):
    """
    Strings parsing
    """    
    begin = 0
    results = []
    while True:
        v, pos = get_val_str(line, begin)
        offset = 0
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
    def get_funcs(func_names):
        funcs = []
        for func_name in func_names:
            func_name = func_name.strip()
            if func_name == 'join':
                funcs.append( lambda x: ",".join(x) )
            elif func_name == 'stringify':
                funcs.append( lambda x: [str(i) for i in x] )
            elif func_name == 'split':
                funcs.append( lambda x: x.split(',') )
            elif func_name == 'first':
                funcs.append( lambda x: x[0] )
            elif func_name == 'last':
                funcs.append( lambda x: x[-1] )
            elif func_name == 'shift':
                funcs.append( lambda x: x[1:] )
            elif func_name == 'pop':
                funcs.append( lambda x: x[:-1] )
            elif func_name == 'reverse':
                funcs.append( lambda x: x[::-1] )                
            else:
                raise Exception('No this function %s!' % func_name)         
        return funcs

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
            import resource
            return resource.Resource.get_global_var(var)

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
        """
        """
        ps = var.split('.')
        v = self.vars
        for p in ps:
            if not p.isdigit():
                v = v[p]
            else:
                v = v[int(p)]
        return v

    def get_last_return_value(self):
        return self.last_return_value

    def set_return_value(self, return_value):
        self.return_value = return_value

    def eval_expr(self, expr):
        if '|' not in expr:
            return self.eval_var(expr)
        else:
            ps = expr.split('|')
            v = self.eval_var(ps[0].strip())
            funcs = Context.get_funcs(ps[1:])
            v = reduce(lambda x, y: y(x), funcs, v)
            
            return v

    def eval_var(self, var):
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
            v = self.eval_expr(val)
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
