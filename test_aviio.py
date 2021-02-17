import json
import requests
from time import sleep
import unittest
import csv
from datetime import date
import time

apiToken = 'LpNe5bB4CZnvkWaTV9Hv7Cd37JqpcMNF'
apiURLBase = 'https://atlas.pretio.in/atlas/coding_quiz'
headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer {0}'.format(apiToken)}


def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1


def status():
    while True:
        response = requests.get(apiURLBase, headers=headers)
        if response.status_code == 200:
            break
        elif response.status_code == 429:
            print('Getting Status Code <response 429> waiting 60 Sec to Try Again')
            countdown(60)
            print('\nTrying Again......!\n')
            pass
        elif response.status_code == 500:
            return response
            break
    return response


def main():
    response = status()
    f = open('offers_{}.csv'.format(str(date.today())), 'w', newline='', errors='ignore')
    writer = csv.writer(f, delimiter=",")
    writer.writerow(['Active', 'Cap', 'Name', 'Payout', 'Platform'])
    responseJson = json.loads(response.content)
    outs = []
    try:
        for element in responseJson['rows']:
            outs.append(
                [element['active'], element['cap'], element['name'], float(element['payout']), element['platform']])
    except:
        print("\n GETTING INVALID JSON RESPONSE TRY AGAIN\n")

    def getKey(item):
        return item[3]

    export = sorted(tuple(outs), key=getKey)
    for row in export:
        writer.writerow(row)

    f.close()


class TestResponse(unittest.TestCase):
    actual = status().status_code
    if actual == 200:
        main()

    def test_500(self):
        actual = self.actual
        expected = 500
        self.assertNotEqual(actual, expected)

    def test_200(self):
        actual = self.actual
        expected = 200
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    main()
