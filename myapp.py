from flask import Flask, request
import json 
from pymessenger import Bot


app = Flask(__name__)

FB_ACCESS_TOKEN = "EAAb7fKPY6LMBAIsbSVJ3YsDaQZAQ2kiTQ9XcPyuDzAfljx48mVW5OFjtmpxErExfrqBv1cg3gfKpj5PHf4ZCUXVbycJecV5U0v8hdah3JQR28tSWReGiqqYZA1iYrLAE7mZBpDMeQ5MSgymM3DOELbrGOKO1c2sU04oSQgXWQAZDZD"
bot = Bot(FB_ACCESS_TOKEN)


@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello shuja", 200



@app.route('/', methods=['POST'])
def webhook():
	print(request.data)

	data = request.get_json()

	if data['object'] == "page":
		entries = data['entry']

		for entry in entries:
			messaging = entry['messaging']

			for messaging_event in messaging:

				sender_id = messaging_event['sender']['id']
				recipient_id = messaging_event['recipient']['id']

				if messaging_event.get('message'):

					if messaging_event['message'].get('text'):

						query = messaging_event['message']['text']
						print(query)
						bot.send_text_message(sender_id, query)

	return "ok", 200


if __name__ == "__main__":
	app.run(port=8000, use_reloader = True) 
