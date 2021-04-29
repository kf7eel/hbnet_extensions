###############################################################################
#   Copyright (C) 2021 Eric Craw, KF7EEL <kf7eel@qsl.net>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
###############################################################################

'''
This is an example application that utilizes the JSON API.
It is a simple weathwe application.
'''

from flask import Flask, request, Markup, jsonify, make_response
import json, requests, time
from config import *

app = Flask(__name__)

class weather:
    '''Use open weather map for weather data'''
    def __init__(self):
        global owm_API_key
        self.api_url = 'http://api.openweathermap.org/data/2.5/'
        self.api_current = 'weather?'
        self.lat = 'lat='
        self.lon = '&lon='
        self.city = 'q='
        self.app_id = '&appid=' + owm_API_key + '&units=imperial'
        # return temp, pressure, wind, and wind dir

    def current_loc(self, lat, lon):
        url = self.api_url + self.api_current + self.lat + lat + self.lon + lon + self.app_id
        wx_data = requests.get(url).json()
        return wx_data['name'] , wx_data['sys']['country'], wx_data['weather'][0]['main'], wx_data['main']['temp'], wx_data['main']['pressure'], wx_data['wind']['speed'], wx_data['wind']['deg']
    def city_loc(self, city_name):
        url = self.api_url + self.api_current + self.city + city_name + self.app_id
        wx_data = requests.get(url).json()
        print(url)
        return wx_data['name'] , wx_data['sys']['country'], wx_data['weather'][0]['main'], wx_data['main']['temp'], wx_data['main']['pressure'], wx_data['wind']['speed'], wx_data['wind']['deg']
        



def respond_request(dest_id, message, token, url):
    url = url + '/app'
    print(url)
    app_response = {
    'mode':'app',
    'app_name':app_name,
    'app_shortcut':app_shortcut,
    'auth_token':str(token),
    'data':{
        1:{ 'destination_id':int(dest_id),
            'slot':0,
            'msg_type':'unit',
            'msg_format':'motorola',
            'message':message
              }
        }
}
    json_object = json.dumps(app_response, indent = 4)
    print(json_object)
    requests.post(url, data=json_object, headers={'Content-Type': 'application/json'})

@app.route('/', methods=['GET'])
def view():
    post_string = ''
    header = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>''' + app_name + '''</title>
    </head>
    <p><img style="display: block; margin-left: auto; margin-right: auto;" src="''' + app_logo + '''" alt="Logo" width="300" height="144" /></p>
    <h1 style="text-align: center;">''' + app_name + '''</h1>
    <table style="width: 800px; border-color: black; margin-left: auto; margin-right: auto;" border="3">
    <tbody>
    <tr>
    <td style="text-align: center;">
    <h3>From</h3>
    </td>
    <td style="text-align: center;">
    <h3>Query</h3>
    </td>
    <td style="text-align: center;">
    <h3>Result</h3>
    </td>
    <td style="text-align: center;">
    <h3>Time</h3>
    </td>
    <td style="text-align: center;">
    <h3>Network/Server</h3>
    </td>
    </tr>
    '''
    footer = '''
    </tbody>
    </table>
    <p>&nbsp;</p>
    <div style="text-align: center;">HBLink Weather created by KF7EEL - <a href="https://kf7eel.github.io/hblink3/">https://github.com/kf7eel/hblink3</a></div>
    </html>
    '''
    for i in display_list:
            post_string = post_string + i + '\n'
    return header + post_string + footer
    

@app.route('/weather', methods=['POST'])
def api(api_mode=None):
    api_data = request.json
    parsed = api_data['data']['message'].split(' ')
    radio_id_get = response = requests.get("https://radioid.net/api/dmr/user/?id=" + str(api_data['data']['source_id']))
    #print(radio_id_get.json())
    radio_id_result = radio_id_get.json()
    #print(radio_id_result['results'][0]['callsign'])
    from_callsign = radio_id_result['results'][0]['callsign']
    name = radio_id_result['results'][0]['fname']
    try:
        wx = weather().city_loc(api_data['data']['message'])
        sms_result = wx[0] + ', ' + wx[1] + '. ' + wx[2] + ', Temp: ' + str(wx[3]) + ' Pres: ' + str(wx[4]) + ' Wind Speed: ' + str(wx[5]) + ' Wind Dir: ' + str(wx[6])
        if api_data['mode'] == 'app':
            #         <td style="text-align: center;"><strong>''' + str(from_callsign) + '</strong><br />' + '<em>' + str(name) + '</em><br />' + str(api_data['data']['source_id']) + '''</td>

            display_list.append('''
            <tr>
            <td style="text-align: center;"><strong>''' + str(from_callsign) + '</strong><br />' + '<em>' + str(name) + '</em><br />' + str(api_data['data']['source_id']) + '''</td>
            <td style="text-align: center;">''' + api_data['data']['message'] + '''</td>
            <td style="text-align: center;">''' + sms_result + '''</td>
            <td style="text-align: center;">''' + time.strftime('%H:%M \n %m/%d/%y') + '''</td>
            <td style="text-align: center;">''' + api_data['server_name']+ '''</td>
            </tr>

                                ''')
    except:
        sms_result = 'Error with query'
        
    respond_request(api_data['data']['source_id'], sms_result, api_data['auth_token'],api_data['response_url'])
    return jsonify(
                        mode=api_data['mode'],
                        status='Response Sent',
                    )



if __name__ == '__main__':
    global display_list, app_name
    display_list = []
    app.run(debug = True, port=app_port, host=app_host)
