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
It is a simple bulletin board application.
'''

from flask import Flask, request, Markup, jsonify, make_response
import json, requests, time
from config import *

app = Flask(__name__)

def respond_request(dest_id, message, token, url):
    url = url + '/app'
    print(url)
    app_response = {
    'mode':'app',
    'app_name':app_name,
    'auth_token':str(token),
    'data':{
        1:{'source_id':app_name,
            'destination_id':int(dest_id),
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
    <h1 style="text-align: center;">''' + app_name + '''</h1>
    <table style="width: 600px; border-color: black; margin-left: auto; margin-right: auto;" border="3">
    <tbody>
    <tr>
    <td style="text-align: center;">
    <h3>From</h3>
    </td>
    <td style="text-align: center;">
    <h3>Message</h3>
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
    <div style="text-align: center;">Bulletin Board created by KF7EEL - <a href="https://kf7eel.github.io/hblink3/">https://github.com/kf7eel/hblink3</a></div>
    </html>
    '''
    for i in display_list:
            post_string = post_string + i + '\n'
    return header + post_string + footer
    

@app.route('/post', methods=['POST'])
def api(api_mode=None):
    api_data = request.json
    print(api_data)
    if api_data['mode'] == 'app':
        
        display_list.append('''
            <tr>
            <td>''' + str(api_data['data']['source_id']) + '''</td>
            <td>''' + api_data['data']['message'] + '''</td>
            <td>''' + time.strftime('%H:%M') + '''</td>
            <td>''' + api_data['server_name']+ '''</td>
            </tr>
                            ''')
        
        respond_request(api_data['data']['source_id'], 'Posted: ' + api_data['data']['message'], api_data['auth_token'],api_data['response_url'])
        return jsonify(
                            mode=api_data['mode'],
                            status='Response Sent',
                        )



if __name__ == '__main__':
    global display_list, app_name
    display_list = []
    app.run(debug = True, port=app_port, host=app_host)
