from flask import Flask, request, jsonify

from services.ticketService import buy_ticket, get_ticket

app = Flask(__name__)


@app.route("/purchase/",methods=['POST'])
def purchase_ticket():
    data = request.get_json()
    if not data or 'user_email' not in data or 'event_name' not in data:
        return {'message': 'missing required fields'}, 400

    event_name = data['event_name']
    user_email = data['user_email']
    ticket_id = buy_ticket(eventName=event_name,email=user_email)
    response = {
        "message": "Ticket purchased successfully",
        'ticket_id': ticket_id}
    return jsonify(response), 200

@app.route("/tickets",methods=['GET'])
def get_all_tickets():
   return get_ticket()


if __name__ == '__main__':
    app.run()
