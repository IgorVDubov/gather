CLIENT_VERSION=0.1
STATE_ARG='args.currentState'
TECH_IDLE_ARG='args.minLength'
STATE_TIME_ARG='args.currentStateTime'
CAUSEID_ARG='args.cause_id'
IDLE_HANDLERID_ARG='args.idle_handler_id'
IDLE_STATES=(1,2) # состояния при которых фиксируется простой
NOT_CHEKED_CAUSE=0  # причина простоя по умолсанию (если не указана)
CAUSE_CHECK_TIMEOUT=120 # таймаут указания причины простоя
IDLE_CAUSES={-1:'Не подтверждена',0:'Технологический простой',1:"Авария", 2:"Нет сырья", 3:"Нет задания", 4:"Плановый простой"}
# IDLE_CAUSES={1:'Не подтверждена',2:'Технологический простой',1:"Авария", 2:"Нет сырья", 3:"Нет задания", 4:"Плановый простой"}
TECH_IDLE_ID=-1
STATES =['N/A', 'Откл', 'Простой', 'Работа']
TIME_FORMAT='%Y-%m-%dT%H:%M:%S'

DEFAULT_CAUSES=(1,2)

