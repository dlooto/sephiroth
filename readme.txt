





# 

# Variables
A variable starts with @ is context variable, its lifetime is during the context lifetime.
A variable starts with @@ is engine variable, its lifetime is same as the engine's lifetime.
A variable starts with $ is global variable, it can be visit all the time.
Here are build-in global variables, $current_seconds, $now, $today, $pid.


# Main triggers
I support every-month, every-day, every-hour, every-minute, and every-second time-format-triggers
For example, If you set ["every-minute 05", "every-minute 35"], the engine would be invoked when 
second is 05 or 35 in evenry minute.
Notice: If you set same trigger (or ) for one engine, it would trigger more than one time.

# Call functions in Pipeline is supported
And here is the function build-in.
join
stringify
split
first
last
shift
pop
For example:
{@some_variable.data.list | stringify | join | split | first}

# 



