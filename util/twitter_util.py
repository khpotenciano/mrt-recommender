import re
from util import Util
class TwitterUtil:

    @classmethod
    def is_date(cls,text):
        pattern = r"^\d{1,2}:\d{2}\s{1}(AM|PM|am|pm){1}.{1,3}(jan|Jan|JAN|feb|Feb|FEB|mar|Mar|MAR|apr|Apr|APR|may|May|MAY|jun|Jun|JUN|jul|Jul|JUL|aug|Aug|AUG|sep|Sep|SEP|oct|Oct|OCT|nov|Nov|NOV|dec|Dec|DEC){1}\s{1}\d{1,2},{1}\s{1}\d{4}$"
        regex_object = re.compile(pattern, re.IGNORECASE)
        return len(regex_object.findall(text)) == 1

    @classmethod
    def get_date_index(cls, captions):
        index = None
        for row_number in range(len(captions)):
            if TwitterUtil.is_date(captions[row_number]):
                index = row_number
        return index

    @classmethod
    def twitter_date_string_to_datetime(cls, date_str):
        dates = date_str.split('·')
        datetime = f"{dates[1]} {dates[0]}".strip()
        return Util.string_to_date(datetime, "%b %d, %Y %I:%M %p")
