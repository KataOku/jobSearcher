from sources.google import Google
from sources.workday import Workday
import os

os.makedirs("adverts", exist_ok=True)


google=Google("Google", "https://careers.google.com")
google.check_for_new()

adobe=Workday("Adobe","https://adobe.wd5.myworkdayjobs.com/external_experienced", "junior tester")
adobe.check_for_new()
