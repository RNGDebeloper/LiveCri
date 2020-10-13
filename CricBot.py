from pycricbuzz import Cricbuzz
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

logger = logging.getLogger(__name__)
def refresh():
    c = Cricbuzz()
    match = c.matches()
    mid = match[0]['id']
    matches = match[0]
    livescore = c.livescore(mid=mid)
    scorecard = c.scorecard(mid=mid)
    matchinfo = c.matchinfo(mid=mid)
    commentary = c.commentary(mid=mid)
    result = {
        "matches": matches,
        "livescore": livescore,
        "scorecard": scorecard,
        "matchinfo": matchinfo,
        "commentary": commentary
    }
    return result
def start(update, context):
    update.message.reply_text("Welcome to Cricket Bot\n\n/info to get match information\n/score to get the live score")

def score(update, context):
    result = refresh()
    update.message.reply_text(f'Batting:  {result["scorecard"]["scorecard"][0]["batteam"]}\nScore:  {result["scorecard"]["scorecard"][0]["runs"]}/{result["scorecard"]["scorecard"][0]["wickets"]}\nOvers:  {result["scorecard"]["scorecard"][0]["overs"]}\nBatting:  {result["scorecard"]["scorecard"][0]["batteam"]}\n\nCommentary : {result["commentary"]["commentary"][0]["comm"]}')

def info(update, context):
    result = refresh()
    update.message.reply_text(f'Match No:  {result["matches"]["mnum"]}\nMatch State:  {result["matches"]["mchstate"]}\nMatch Status:  {result["matches"]["status"]}\nToss:  {result["matches"]["toss"]}\nLocation:  {result["matches"]["venue_location"]}')

def main():
    updater = Updater("1357838884:AAFxrvLzw-g2i4j2mTsXw1z8rbrgAj4dq34", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("score", score))
    dp.add_handler(CommandHandler("info", info))
    # dp.add_handler(CommandHandler("get_msg", get_msg))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
