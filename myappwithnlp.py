from flask import Flask, request
import json 
from pymessenger import Bot
from utils import apiai_response


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
						entity = messaging_event.get('message')['nlp']['entities']
						print(query)
						intent , params , default = apiai_response(query, sender_id)
						if intent == 'news':
							bot.send_text_message(sender_id, str(params))

						elif intent.startswith('smalltalk'):
							bot.send_text_message(sender_id, default)


	return "ok", 200


if __name__ == "__main__":
	app.run(port=8080, use_reloader = True)
