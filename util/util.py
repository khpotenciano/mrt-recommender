from datetime import datetime, timedelta

class Util:
    @classmethod
    def valid_value(cls, value, value_type):
        return value == None or type(value) == value_type

    @classmethod
    def string_to_date(cls,date_str,format="%Y-%m-%d"):
        date = None
        if date_str == None:
            date = datetime.now()
        else:
            date = datetime.strptime(date_str,format)
        return date

    @classmethod
    def get_next_date(cls, date,delta):
        return date + timedelta(days=delta)

    @classmethod
    def date_to_string(cls, date,format="%Y-%m-%d"):
        return datetime.strftime(date, format)
