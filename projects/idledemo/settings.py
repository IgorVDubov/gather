CLIENT_VERSION=0.1
STATE_ARG='args.currentState'
STATE_TIME_ARG='args.currentStateTime'
CAUSEID_ARG='args.cause_id'
IDLE_HANDLERID_ARG='args.idle_handler_id'
IDLE_STATES=(1,2) # состояния при которых фиксируется простой
NOT_CHEKED_CAUSE=0  # причина простоя по умолсанию (если не указана)
CAUSE_CHECK_TIMEOUT=120 # таймаут указания причины простоя
IDLE_CAUSES={1:"Авария", 2:"Нет сырья", 3:"Нет задания", 4:"Плановый простой"}

