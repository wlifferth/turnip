import flask
import collections
import datetime
import json

app = flask.Flask(__name__, static_url_path='')

# We'll store the most recent 10 messages
messages = collections.deque(maxlen=100)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if flask.request.method == 'POST':
        request_ip_address = get_client_ip_address()
        insert_new_message(
            text=flask.request.form['message'],
            username=get_username(request_ip_address),
            color=get_color(request_ip_address)
        )
    return flask.send_file('index.html')

@app.route('/messages', methods = ['GET'])
def message_data():
    return json.dumps(get_recent_messages())

# Functions for changing state
def insert_new_message(username, color, text):
    messages.append({
        'text': flask.request.form['message'],
        'username': get_username(request_ip_address),
        'color': get_color(request_ip_address),
        'creation_time': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
    })

def get_recent_messages(num_messages=100):
    messages_list = list(reversed(messages))
    if len(messages_list) > num_messages:
        messages_list = messages_list[:num_messages]
    return messages_list

# Utilities for making fun usernames

def get_client_ip_address():
    if flask.request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        return flask.request.environ['REMOTE_ADDR']
    else:
        return flask.request.environ['HTTP_X_FORWARDED_FOR']

def get_username(request_ip_address):
    ip_hash = hash(request_ip_address)
    adjectives = [
        'chonky',
        'smol',
        'lit',
        'whack',
        'heppy',
        'bb',
        'anarchist'
    ]
    animals = [
        'doggo',
        'catto',
        'spoder',
        'floof',
        'bunn',
        'corgi',
        'mayonaise'
    ]
    selected_adjective = adjectives[ip_hash % len(adjectives)]
    selected_animal = animals[(ip_hash // 100) % len(animals)]
    return f'{selected_adjective} {selected_animal}'

def get_color(request_ip_address):
    colors = [
        'F8B195',
        'F67280',
        'C06C84',
        '6C5B7B',
        '355C7D'
    ]
    ip_hash = hash(request_ip_address)
    return colors[(hash(request_ip_address) // 10000) % len(colors)]

if __name__ == '__main__':
    app.run(host='0.0.0.0')