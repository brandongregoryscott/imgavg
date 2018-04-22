import io
import random
import logging
import sys
import os
import ast

from twitterbot import TwitterBot, ignore

import imgavg

def convert_image_to_bytes(img):
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    return img_bytes

class Bot(TwitterBot):
    def bot_init(self):
        ############################
        # REQUIRED: LOGIN DETAILS! #
        ############################
        self.config['api_key'] = os.environ['API_KEY']
        self.config['api_secret'] = os.environ['API_SECRET']
        self.config['access_key'] = os.environ['ACCESS_KEY']
        self.config['access_secret'] = os.environ['ACCESS_SECRET']

        ######################################
        # SEMI-OPTIONAL: OTHER CONFIG STUFF! #
        ######################################

        # how often to tweet, in seconds
        self.config['tweet_interval'] = os.environ['TWEET_INTERVAL']  # default: 30 minutes

        # use this to define a (min, max) random range of how often to tweet
        # e.g., self.config['tweet_interval_range'] = (5*60, 10*60) # tweets every 5-10 minutes
        # self.config['tweet_interval_range'] = (45 * 60, 75 * 60)

        # only reply to tweets that specifically mention the bot
        self.config['reply_direct_mention_only'] = ast.literal_eval(os.environ['REPLY_DIRECT_MENTION_ONLY'])

        # only include bot followers (and original tweeter) in @-replies
        self.config['reply_followers_only'] = ast.literal_eval(os.environ['REPLY_FOLLOWERS_ONLY'])

        # fav any tweets that mention this bot?
        self.config['autofav_mentions'] = ast.literal_eval(os.environ['AUTOFAV_MENTIONS'])

        # fav any tweets containing these keywords?
        self.config['autofav_keywords'] = ast.literal_eval(os.environ['AUTOFAV_KEYWORDS'])

        # follow back all followers?
        self.config['autofollow'] = ast.literal_eval(os.environ['AUTOFOLLOW'])


        ###########################################
        # CUSTOM: your bot's own config variables! #
        ###########################################

        self.config['bots'] = ast.literal_eval(os.environ['BOTS'])
        self.config['tags'] = ast.literal_eval(os.environ['TAGS'])
        self.config['responses'] = ast.literal_eval(os.environ['RESPONSES'])

    def on_scheduled_tweet(self):
        return
        mention_user = random.choice(self.config['bots'])
        text = random.choice(self.config['tags'])
        img = imgavg.original()
        self.post_tweet(".@{0} {1}".format(mention_user, text), media=convert_image_to_bytes(img))

    def on_mention(self, tweet, prefix):
        reply_user = tweet['user']['screen_name']
        if 'media' not in tweet['entities'].keys():
                pass
        else:
            reply_img = imgavg.main(tweet)
            text = random.choice(self.config['responses'])
            while not self.post_tweet(".@{0} {1}".format(reply_user, text), reply_to=tweet, media=convert_image_to_bytes(reply_img)):
                pass

    @ignore
    def on_timeline(self, tweet, prefix):
        pass

if __name__ == '__main__':
    bot = Bot()
    bot.run()
