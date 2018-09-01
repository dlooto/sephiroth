

# EngineState_Init -> EngineState_Start -> EngineState_Running -> EngineState_Waiting
# -> EngineState_Running
EngineState_Unknown = 0
EngineState_Init = 1
EngineState_Start = 2
EngineState_Running = 3
EngineState_Waiting = 4


ConfigState_Init       = 0
ConfigState_Parsed     = 1
ConfigState_Loaded     = 2


Kw_Requires             = "requires"
Kw_Main                 = "main"
Kw_Action               = "action"
Kw_Resource             = "resource"
Kw_Start_At             = "start_at"

#全部关键字列表
Keywords = [Kw_Action, Kw_Main, Kw_Requires, Kw_Resource]

Logger_Format = '[%(asctime)s %(levelname)s] <%(pathname)s(%(lineno)d)> %(message)s'