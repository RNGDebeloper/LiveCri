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
    result = {}
    result['matches'] = matches
    result['livescore']= livescore
    result['scorecard']= scorecard
    result['matchinfo']= matchinfo
    result['commentary']= commentary
    return result

def start(update, context):
    update.message.reply_text("Welcome to Cricket Bot\n\n/info to get match information\n/score to get the live score")

def score(update, context):
    result = refresh()
    batsman1_name = result['livescore']["batting"]["batsman"][0]["name"]
    batsman1_runs = result['livescore']["batting"]["batsman"][0]["runs"]
    batsman1_balls = result['livescore']["batting"]["batsman"][0]["balls"]
    batsman2_name = result['livescore']["batting"]["batsman"][1]["name"]
    batsman2_runs = result['livescore']["batting"]["batsman"][1]["runs"]
    batsman2_balls = result['livescore']["batting"]["batsman"][1]["balls"]
    bowler_name = result['livescore']["bowling"]["bowler"][0]["name"]
    bowler_overs = result['livescore']["bowling"]["bowler"][0]["overs"]
    bowler_runs = result['livescore']["bowling"]["bowler"][0]["runs"]
    bowler_wickets = result['livescore']["bowling"]["bowler"][0]["wickets"]
    update.message.reply_text(f'Batting:  {result["scorecard"]["scorecard"][0]["batteam"]}\nScore:  {result["scorecard"]["scorecard"][0]["runs"]}/{result["scorecard"]["scorecard"][0]["wickets"]}\nOvers:  {result["scorecard"]["scorecard"][0]["overs"]}\n{batsman1_name}: {batsman1_runs} ({batsman1_balls})\n{batsman2_name}: {batsman1_runs} ({batsman2_balls})\n\nBalling: {result["scorecard"]["scorecard"][0]["bowlteam"]}\n{bowler_name}: {bowler_wickets}-{bowler_runs} ({bowler_overs})\n\nCommentary : {result["commentary"]["commentary"][0]["comm"]}')

def info(update, context):
    result = refresh()
    t1_name = result["matches"]["team1"]["name"]
    t2_name = result["matches"]["team2"]["name"]
    team1 = ", ".join(result["matches"]["team1"]["squad"])
    team2 = ", ".join(result["matches"]["team2"]["squad"])
    update.message.reply_text(f'Match No:  {result["matches"]["mnum"]}\nMatch State:  {result["matches"]["mchstate"]}\nMatch Status:  {result["matches"]["status"]}\nToss:  {result["matches"]["toss"]}\nLocation:  {result["matches"]["venue_location"]}\n\n{t1_name} Squad: {team1}\n\n{t2_name} Squad: {team2}')

def main():
    updater = Updater("6881938858:AAHxjQCupjXOrP3FjRUJljAEAty-U7iFGUg", use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("score", score))
    dp.add_handler(CommandHandler("info", info))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
