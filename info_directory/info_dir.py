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
It is an information directory application.
'''

from flask import Flask, request, Markup, jsonify, make_response
import json, requests, time
from config import *
import os, ast

app = Flask(__name__)

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
    q_data = ast.literal_eval(os.popen('cat ./queries.txt').read())
    print(q_data)
    q_list = ''
    for i in q_data:
        q_list = q_list + ''' <tr>
    <td style="text-align: center;">''' + i + '''</td>
    </tr>''' + '\n'
        print(i)
    header = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <title>''' + app_name + '''</title>
    </head>
    <p><img style="display: block; margin-left: auto; margin-right: auto;" src="''' + app_logo + '''" alt="Logo" width="300" height="144" /></p>
    <h1 style="text-align: center;">''' + app_name + '''</h1>
    <table style="width: 200px; margin-left: auto; margin-right: auto;" border="1">
    <tbody>
    <tr>
    <td style="text-align: center;">
    <h2>Available Queries</h2>
    </td>
    </tr>
    

    '''
    footer = '''
    </tbody>
    </table>
    <p>&nbsp;</p>
    <div style="text-align: center;">Information Directory created by KF7EEL - <a href="https://kf7eel.github.io/hblink3/">https://github.com/kf7eel/hblink3</a></div>
    </html>
    '''

    return header + q_list + footer
    

@app.route('/query', methods=['POST'])
def api(api_mode=None):
    q_data = ast.literal_eval(os.popen('cat ./queries.txt').read())
    api_data = request.json
    #radio_id_get = response = requests.get("https://radioid.net/api/dmr/user/?id=" + str(api_data['data']['source_id']))
    print(api_data['data']['message'])
    #print(radio_id_get.json())
    #radio_id_result = radio_id_get.json()
    #print(radio_id_result['results'][0]['callsign'])
    #from_callsign = radio_id_result['results'][0]['callsign']
    #name = radio_id_result['results'][0]['fname']
    if api_data['mode'] == 'app':
        try:
            respond_request(api_data['data']['source_id'], q_data[api_data['data']['message']], api_data['auth_token'],api_data['response_url'])
            return jsonify(
                                mode=api_data['mode'],
                                status='Response Sent',
                            )
        except:
            respond_request(api_data['data']['source_id'], 'Error with query', api_data['auth_token'],api_data['response_url'])
            return jsonify(
                                mode=api_data['mode'],
                                status='Response Sent',
                            )



if __name__ == '__main__':
    global display_list, app_name
    display_list = []
    app.run(debug = True, port=app_port, host=app_host)
