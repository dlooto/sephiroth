
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

# 代码分支说明
* **因各自动站设备及数据配置有差异，为继承原代码仓库，各自动站设立单独的代码分支。说明如下：**
* master: 主干分支（目前未做改动）
* beijing: 北京自动站分支

* shanghai-chongming: 上海崇明站
* shanghai-emagnetic: 上海电磁站
* shanghai-jinshan: 上海金山站
* shanghai-3： 上海临港站

* zhejiang: 浙江站
* jiangsu:  江苏站
* zhuhai-air: 珠海-大气辐射环境监测站
* zhuhai-water: 珠海-竹银水库水质监测站



