import flask
import collections
import datetime

app = flask.Flask(__name__)

# We'll store the most recent 10 messages
messages = collections.deque(maxlen=100)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if flask.request.method == 'POST':
        request_ip_address = flask.request.environ['REMOTE_ADDR']
        messages.append({
            'text': flask.request.form['message'],
            'username': get_username(request_ip_address),
            'timestamp': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'color': get_color(request_ip_address)
        })
    return flask.render_template('index.html', messages=reversed(messages))


def get_username(request_ip_address):
    ip_hash = hash(request_ip_address)
    adjectives = [
        'chonky',
        'smol'
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
    selected_animal = animals[ip_hash // 100 % len(animals)]
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
    return colors[hash(request_ip_address) // 10000 % len(colors)]