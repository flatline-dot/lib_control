import datetime

a = datetime.date.today()
b = datetime.date(year=2022, month=1, day=15)
c = a + datetime.timedelta(days=10)
print(c)
