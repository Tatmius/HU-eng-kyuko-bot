from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent, QuickReply, QuickReplyButton, MessageAction
)
import scrape, os

from local_keys import channel_access_token, channel_secret

app = Flask(__name__)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


# line_bot_api.push_message(' ', messages="hello")


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(FollowEvent)
def handle_follow(event):
    profile = line_bot_api.get_profile(event.source.user_id)
    user_id = profile.user_id


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    nearest = "今日明日の講義情報"
    week = "7日以内の講義情報"
    receive_message = event.message.text
    info_array = scrape.scraping('https://www.eng.hokudai.ac.jp/lecinfo/')
    items = [
        QuickReplyButton(action=MessageAction(label=nearest, text=nearest)),
        QuickReplyButton(action=MessageAction(label=week, text=week))
    ]

    if receive_message == nearest:
        reply_message = scrape.nearest_change(info_array)
    elif receive_message == week:
        reply_message = scrape.change_weekly(info_array)
    elif receive_message == "うんち":
        reply_message = "うんち！"
    else:
        reply_message = "現在個別の返信には対応しておりません。"

    message = TextSendMessage(text=reply_message, quick_reply=QuickReply(items=items))
    line_bot_api.reply_message(event.reply_token, messages=message)


if __name__ == '__main__':
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
