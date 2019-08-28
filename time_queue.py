import datetime
from se_ctrip.settings import START,END,RECENT



def date_query():
    """
    构建日期列表
    :return:
    """
    a = datetime.datetime.today()
    date_lists = []
    for i in range(START, END):
        b = (a + datetime.timedelta(days=i)).strftime('%Y-%m-%d')
        c =(a + datetime.timedelta(days=i+1)).strftime('%Y-%m-%d')
        date_lists.append((b,c))
    return date_lists

def hours_query():
    a = datetime.datetime.today()
    hours_list = []
    for i in range(RECENT):
        b = (a + datetime.timedelta(hours=-i)).strftime('%Y-%m-%d %H')
        hours_list.append(b)
    return hours_list

if __name__=="__main__":
    print(date_query())