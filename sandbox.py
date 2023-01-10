import json
idle_causes=["Авария", "Нет сырья", "Нет задания", "Плановый простой"]
j=json.dumps(idle_causes, default=str)
print(j)
print(json.loads(j))
