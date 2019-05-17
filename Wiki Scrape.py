from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from typing import Tuple
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import time

"""
Code written by Ajitesh Misra
"""

# for this to work you need an actual username and password
# for the wiki
login_data = {
	"u" : "Username",
	"p" : "Password"
}

data_points = []

# the amount of data points you want to get
TIME_LIMIT = 168

# Log into the website
# this loads the first 1,000,000,000 edits of the wiki, after we have logged in
LOGIN_URL = "https://mathwiki.utm.utoronto.ca/wiki/index.php?title=Special:UserLogin&returnto=Special%3ALog&returntoquery=offset%3D%26limit%3D1000000000%26type%3D%26user%3D"

def get_total_edits() -> int:
    """ Use selenium to log into the wiki logs 
    and then find the total amount of edits
    Then close the browser
    """

    # use selenium to enter log into the website
    browser = webdriver.Chrome()
    browser.get(LOGIN_URL)

    # find where to enter the username and password
    username_box = browser.find_element_by_id("wpName1")
    password_box = browser.find_element_by_id("wpPassword1")

    # find where to click once info is entered
    login_button = browser.find_element_by_id("wpLoginAttempt")

    # input the needed data to log in
    username_box.send_keys(login_data["u"])
    password_box.send_keys(login_data["p"])

    # log into the wiki
    login_button.click()

    # We are now logged into the wiki
    # get the html data from the page
    soup = BeautifulSoup(browser.page_source, "html.parser")

    # find the amount of listed entries
    number_of_entries = len((soup.ul.findAll("li")))

    # close the browser
    browser.quit()

    return number_of_entries

def find_data_point() -> None:
    """ Create a data point of (date, number of edits)
    At a given time and add it to the data points list
    data points are of the type: Tuple(DateTime, int)
    Tuple: (datetime, number of edits)
    """
    # get the total number of edits from the wiki log
    edits = get_total_edits()
    
    # print edits for debugging purposes
    print(edits)

    # find the current time in the given format
    time = datetime.now().strptime("25/01/2019, 23:55:08" , "%d/%m/%Y, %H:%M:%S")

    # update the data points as a tuple of (time, edit)
    data_points.append((time, edits))

def plot_data() -> None:
    """ Create the plot of number of edits over time
    """
    x = []
    y = []
    for point in data_points:
        # time is the independant variable
        x.append(point[0])
        # number of edits is the dependant variable
        y.append(point[1])

    # use matplotlib to plot the data
    figure, axes = plt.subplots()
    axes.plot_date(x,y)

    # configure the x axis to show all the data points
    # starting with the first one, and then the last point
    axes.set_xlim(data_points[0][0] - timedelta(hours= 3), data_points[-1][0] + timedelta(hours= 3))

    # set up x axis to be date and times
    axes.xaxis.set_major_formatter(dates.DateFormatter("%Y/%m/%d  %H:%M:%S"))
    axes.xaxis.set_minor_formatter(dates.DateFormatter("%Y/%m/%d  %H:%M:%S"))

    # tilt the x axis labels to be more readable
    figure.autofmt_xdate()

    # render the graph
    plt.show()

if __name__ == "__main__":
    while True:
        # update the data points
        find_data_point()
        # only run once every hour
        time.sleep(3600)

        # break and plot the data points after enough 
        # data points exist
        if len(data_points) > TIME_LIMIT:
            break
    
    plot_data()