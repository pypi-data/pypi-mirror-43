import ast
import logging
import sqlite3
import sys
import urllib.parse
from time import sleep

import requests
from flask import Flask
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask.ext.session import Session
from flask_qrcode import QRcode
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import IntegerField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired

from examples.event_chain import app
from examples.event_chain import config

application = Flask(__name__)
application.config['SECRET_KEY'] = 'hihihihihi'
SESSION_TYPE = 'filesystem'
application.config.from_object(__name__)

Session(application)
QRcode(application)
CSRFProtect(application)
logging.basicConfig(level=logging.DEBUG)
DB_PATH = config.db_path
logging.info('DB: {}'.format(DB_PATH))
logging.info('forge port {}'.format(config.forge_config.sock_grpc))
APP_SK = "Usi5RHoF/YGoGvbt7TQMaz55p3" \
         "+dl4HUi6M9mHkLuzpJLJxpXrvfQ3ZS189YWlieMik3TKqQuk9hhFLcg/WM8A=="
APP_PK = "SSycaV6730N2UtfPWFpYnjIpN0yqkLpPYYRS3IP1jPA="
APP_ADDR = "z1gJMDjiA9HfbXw9YD2DWKkKWaBJAAMttGu"
TEST_TX = "CiN6MVNNTDM5UjNrNTRNcTY1ZFF1dlU0NkxXOWdMVzVWb2JIRhABGkC8aslX+7N" \
          "/H8DafgxFwRlsYLGa1iRWduWpJ7rkjrRXh/gNttlOzSWEOiLm+MBR3f5S5NZcJW2" \
          "/FH8BDBGxTlYJIgtmb3JnZS1sb2NhbDq7AgoNZmc6dDpleGNoYW5nZRKpAhImEi" \
          "R6amRvYjRXNEFkc2NIU1Y5OWlYRnA5bnBHWkI3WU5SMlVKNEEawgEKvwEKvAEAAAA" \
          "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
          "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
          "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
          "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHo6C" \
          "hJlYzp4OmV2ZW50X2FkZHJlc3MSJHpqZHFSNlB6TjRKdFNLTjdaZnJOdlZ4RThM" \
          "Ymp5aEVwZWJZQQ=="
HOST = 'http://did-workshop.arcblock.co:5000/'


class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    confirm = SubmitField('Confirm')
    total = StringField('Total')
    start_time = StringField("StartTime")
    description = StringField("Description")
    end_time = StringField("EndTime")
    ticket_price = IntegerField("TicketPrice")
    address = StringField('Address')


def wait():
    sleep(5)


def connect_db():
    return sqlite3.connect(DB_PATH)


@application.before_request
def before_request():
    g.db = connect_db()
    g.logger = logging.getLogger('app')
    g.logger.setLevel(level=logging.DEBUG)


@application.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


def gen_mobile_url(event_address):
    arc = 'https://arcwallet.io/i/?'
    params = {'appPk': APP_PK, 'appDid': 'did:abt:' + APP_ADDR,
              'action:': 'requestAuth',
              'url': HOST + 'api/mobile-buy-ticket/{0}'.format(event_address)}
    return arc + urllib.parse.urlencode(params)


@application.route("/details/<address>", methods=['GET', 'POST'])
def event_detail(address):
    if address and address != '':
        event = app.get_event_state(address)
        form = EventForm()
        if not session.get('user', None):
            flash('Please register first!')
            return redirect('/login')
        url = gen_mobile_url(address)
        return render_template('event_details.html', event=event, form=form,
                               url=url)
    else:
        g.logger.error("No event address provided.")
        redirect('/')


@application.route("/clear_db", methods=['GET'])
def clear_db():
    g.logger.info("Clearing all data from db...")
    app.clear_db(g.db)
    redirect('/')


@application.route("/buy", methods=['POST'])
def buy():
    refresh_token()
    form = EventForm()
    address = form.address.data
    g.logger.debug('address: {}'.format(form.address))
    g.logger.debug('submit: {}'.format(form.confirm))
    if not address or address == '':
        g.logger.error("No event address.")
    else:
        app.buy_ticket(address, session['user'], g.db)
    return redirect('/')


@application.route("/activate", methods=['GET', 'POST'])
def use():
    refresh_token()
    ticket_address = request.args.get('address')
    ticket = app.get_ticket_state(ticket_address)
    activate_tx = ticket.gen_activate_asset_tx(session['user'])
    app.activate(activate_tx, session['user'])
    return redirect('/')


@application.route("/", methods=['GET', 'POST'])
def event_list():
    events = app.list_events(g.db)
    event_lists = chunks(events, 3)
    return render_template(
            'event_list.html', event_lists=event_lists,
            session=session, number=len(events),
    )


def get_event_for_ticket(tickets):
    res = {}
    for ticket in tickets:
        event = app.get_event_state(ticket.ticket_info.event_address)
        res[ticket.address] = event
    return res


@application.route("/tickets")
def ticket_list():
    unused_list = app.list_unused_tickets(session['user'].address)
    used_list = app.list_used_tickets(session['user'].address)
    tickets = app.list_tickets(g.db, session['user'])
    events = get_event_for_ticket(tickets)
    combine = unused_list + used_list

    ticket_lists = chunks(tickets, 3)
    return render_template(
            'tickets.html', ticket_lists=ticket_lists,
            number=len(tickets), events=events,
    )


@application.route("/create", methods=['GET', 'POST'])
def create_event():
    refresh_token()
    form = EventForm()
    if form.validate_on_submit():
        if not session.get('user', None):
            flash('Please register first!')
            return redirect('/login')
        elif request.method == "POST":
            app.create_event(
                    user=session['user'],
                    title=form.title.data,
                    total=form.total.data,
                    description=form.description.data,
                    start_time=form.start_time.data,
                    end_time=form.end_time.data,
                    ticket_price=form.ticket_price.data,
                    conn=g.db,
            )
            wait()
            return redirect('/')
    else:
        g.logger.error(form.errors)
    return render_template('event_create.html', form=form)


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    passphrase = StringField('Passphrase', validators=[DataRequired()])
    data = StringField('Data')
    confirm = SubmitField('Confirm')
    address = StringField('Address')


@application.route("/ticket_details", methods=['GET', 'POST'])
def ticket_detail():
    address = request.args.get('address')
    g.logger.debug('about to get ticket exchange tx for {}'.format(address))
    if address and address != '':
        event = app.get_event_state(address)
        exchange_tx = app.get_ticket_exchange_tx(address, g.db)
        return render_template(
                'ticket_details.html', tx=exchange_tx, event=event,
        )


def refresh_token():
    user = session['user']
    user = app.load_user(
            moniker=user.moniker,
            passphrase=user.passphrase,
            conn=g.db,
            address=user.address,
    )
    session.clear()
    session['user'] = user


@application.route("/login", methods=['GET', 'POST'])
def login():
    form = RegisterForm()
    if form.validate_on_submit():
        user = app.load_user(
                moniker=form.name.data,
                passphrase=form.passphrase.data,
                address=form.address.data,
        )
        session['user'] = user
        return redirect('/')
    return render_template('login.html', form=form)


@application.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = app.register_user(
                form.name.data,
                form.passphrase.data,
                g.db,
        )
        session['user'] = user
        g.logger.debug(
                'New User registered! wallet: {}, token: {}'.format(
                        user.wallet,
                        user.token,
                ),
        )
        g.logger.debug("form is validated!!")
        return redirect('/')


@application.route("/recover", methods=['GET', 'POST'])
def recover():
    form = RegisterForm()

    if form.validate_on_submit():
        user = app.recover_user(
                form.data.data.encode('utf8'),
                form.name.data,
                form.passphrase.data,
                g.db,
        )
        session['user'] = user
        g.logger.debug(
                'New User recovered! wallet: {}, token: {}'.format(
                        user.wallet,
                        user.token,
                ),
        )
        g.logger.debug("form is validated!!")
        return redirect('/')

@application.route(
        "/api/mobile-buy-ticket/<event_address>",
        methods=['GET', 'POST'],
)
def mobile_buy_ticket(event_address):
    if request.method == 'GET':
        event = app.get_event_state(event_address)
        g.logger.debug("mobile-buy-ticket receives a request")
        params = {
            'sk': APP_SK,
            'pk': APP_PK,
            'address': APP_ADDR,
            'tx': event.get_encoded_exchange_tx(),
            'url': HOST + 'api/mobile-buy-ticket/{}'.format(event_address),
        }
        headers = {'content-type': 'application/json'}
        response = requests.post(
                'http://did-workshop.arcblock.co:4000/api/authinfo',
                json=params,
                headers=headers,
        )
        g.logger.debug("mobile-buy got response from did auth service.")
        return response.content
    elif request.method == 'POST':
        req = ast.literal_eval(request.get_data(as_text=True))
        g.logger.debug("Receives signature info from wallet {}".format(req))
        app.buy_ticket_mobile(event_address, req)
        return event_address


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]


if __name__ == '__main__':
    run_type = sys.argv[1]
    application.jinja_env.auto_reload = True
    application.config['TEMPLATES_AUTO_RELOAD'] = True
    if run_type == 'debug':
        application.run(debug=True)
    else:
        application.run(debug=False, host='0.0.0.0')
