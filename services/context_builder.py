import datetime
def build_context(intent):
    return {"hour": datetime.datetime.now().hour, "meal_time": intent.get("meal_time")}
