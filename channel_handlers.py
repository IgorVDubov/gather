from time import time

def progSheduller(vars):
    
    return vars

# шаблон программ
def func(vars,stored):
    '''
    VARS
        
    STORED
        
    '''
    return stored

# шаблон программs обработки канала
def func(resultIn,stored):
    '''
    STORED
    '''
    resultOut=None
    return resultOut, stored


import collections
def middle(inResult, stored):
    '''
    бегущее среднее из MAX_VALUES значений
    STORED
        deque
    '''
    if not stored.deque:
        stored.deque=collections.deque([inResult for r in range(stored.MAX_VALUES)],stored.MAX_VALUES)
        
    stored.deque.append(inResult)
    outResult=sum(stored.deque)/stored.MAX_VALUES
    return outResult, stored


def progVEK(vars,stored):
    '''
    VARS:
    VAR_INPUT value_in :  IN вход канала
                * status_db : USINT; END_VAR // статус отрезка для записи БД
                * length_db : UDINT; END_VAR // длительность отрезка для записи БД
                * time_db : DATE_AND_TIME; END_VAR // начало отрезка для записи БД
                * db_write : BOOL; END_VAR // флаг записи в БД -> DB_in
	VAR_OUTPUT status : текущее состояние (для отображения)
	VAR_INPUT dost :  достоверность аргумент от канала к источнику
	VAR_INOUT write_init : BOOL := 1; END_VAR // принудительная инициализация записи
	VAR_OUTPUT status_bit1 : BOOL; END_VAR // бит1 статуса для HEX канала состояния
	VAR_OUTPUT status_bit2 : BOOL; END_VAR // бит2 статуса для HEX состояния
	
    STORED
    gr_stand  граница простоя
     gr_work : REAL; END_VAR // граница рботы
	dost_Timeout : USINT := 5; END_VAR // таймаут НЕдостоверности канала
	min_length : USINT := 20; END_VAR // минимальный отрезок времени сменеы статуса (если меньше, статус не меняется)
	VAR time_now : DATE_AND_TIME; END_VAR
    '''


    return stored



#---------------------------------------------------------------------------#
# Exported Identifiers
#---------------------------------------------------------------------------#
__all__ = [
        "middle",
        "progVEK",
        "progSheduller",
]

