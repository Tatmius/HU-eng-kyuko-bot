from bs4 import BeautifulSoup
import urllib.request
import datetime


def scraping(url):
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, features="lxml")
    tbody = soup.find('tbody')
    class_info_array = tbody.find_all('tr')
    return class_info_array


class ClassInfo:
    def __init__(self, date, period, category, class_name, prof, place, description, update):
        self.date = date
        self.period = period
        self.category = category
        self.class_name = class_name
        self.prof = prof
        self.place = place
        self.description = description
        self.update = update

    def message_form(self):
        sending_message = "<講義科目名>\n" + self.class_name \
                + "\n<日時>\n" + self.date \
                + "\n<講時>\n" + self.period \
                + "\n<区分>\n" + self.category \
                + "\n<担当>\n" + self.prof \
                + "\n<講義室>\n" + self.place \
                + "\n<備考>\n" + self.description \
                + "\n<更新>\n" + self.update + "\n________\n"
        return sending_message

    def get_change_date(self):   # This method returns datetime object
        date_text = self.date.split('/')
        date_year = int(date_text[0])
        date_month = int(date_text[1])
        date_day = int(((date_text[2]).split('('))[0])
        change_date = datetime.datetime(year=date_year, month=date_month, day=date_day)

        return change_date


def make_inst_class_info(trarray):
    all_td = trarray.find_all('td')
    date = all_td[0].text
    period = all_td[1].text
    category = all_td[2].text
    class_name = all_td[3].text
    prof = all_td[4].text
    place = all_td[5].text
    description = all_td[6].text
    update = all_td[7].text
    class_info = ClassInfo(date, period, category, class_name, prof, place, description, update)
    return class_info


def delta_date_from_now(x):
    y = x - datetime.datetime.now()  # This function returns deltatime object.
    return y


def nearest_change(array):
    nearest_change_instance = make_inst_class_info(array[-1])
    date_nearest = nearest_change_instance.get_change_date()
    delta_now_nearest = delta_date_from_now(date_nearest)
    if delta_now_nearest.days >= 2:
        message = "今日と明日の休講情報は現時点ではありません。"
    else:
        nearest_change_text = nearest_change_instance.message_form()
        message = nearest_change_text

    return message


def change_weekly(array):
    message_weekly = ""
    count = len(array)
    for i in range(count):
        tmp_instance = make_inst_class_info(array[count - 1 - i])
        tmp_date = tmp_instance.get_change_date()
        delta_date = delta_date_from_now(tmp_date)
        if delta_date.days > 7:
            break
        message_weekly = message_weekly + tmp_instance.message_form()

    return message_weekly











