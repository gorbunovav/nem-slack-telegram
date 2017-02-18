'''
Created on 26.09.2015

@author: root
'''
import Queue
import threading
import time
import ConfigParser
import logging
import json
from slack_coms import SlackManager
from telegram_coms import TelegramManager

Config = ConfigParser.ConfigParser()
Config.read("config.ini")

logging.basicConfig(format='%(levelname)s: %(asctime)s %(message)s in %(module)s on line %(lineno)d',
                    level=Config.get('Logger', 'Level'),
                    handlers=[logging.StreamHandler()
                              #,logging.FileHandler("bridge.log")
                             ]
                   )

SLACK_TOKEN = Config.get('Token', 'Slack')
TELEGRAM_TOKEN = Config.get('Token', 'Telegram')

SLACK_CHANNEL_MATCHING = json.loads(Config.get('Channels', 'Match'))

TELEGRAM_CHANNEL_MATCHING = {tel_channel: slack_channel for slack_channel,
                          tel_channel in SLACK_CHANNEL_MATCHING.items()}

SLACK_EMO_MATCHING = {':stuck_out_tongue:': ':P',
                             ':smile:': ':D',
                            ':simple_smile:': ':)',
                            ':wink:': ';)', }

slack = SlackManager(SLACK_TOKEN, TELEGRAM_CHANNEL_MATCHING,
                     SLACK_EMO_MATCHING)
telegram = TelegramManager(TELEGRAM_TOKEN, SLACK_CHANNEL_MATCHING)

'''Queues are used to pass information between Threads. Duh!'''
slack_output_queue = Queue.Queue()
telegram_output_queue = Queue.Queue()


'''All threads are being created and started.'''
slack_listen_thread = threading.Thread(name='slack_listener',
                                       target=slack.listen_to_slack,
                                       args=(slack_output_queue,))
slack_listen_thread.setDaemon(True)
slack_listen_thread.start()

telegram_listen_thread = threading.Thread(name='telegram_listener',
                                       target=telegram.listen_to_telegram,
                                       args=(telegram_output_queue,))
telegram_listen_thread.setDaemon(True)
telegram_listen_thread.start()

slack_forward_thread = threading.Thread(name='slack_forwarder',
                                       target=slack.forward_to_slack,
                                       args=(telegram_output_queue, ))

slack_forward_thread.setDaemon(True)
slack_forward_thread.start()

telegram_forward_thread = threading.Thread(name='telegram_forwarder',
                                    target=telegram.forward_to_telegram,
                                    args=(slack_output_queue,))

telegram_forward_thread.setDaemon(True)
telegram_forward_thread.start()

if __name__ == '__main__':
    while True:
        try:
            message = 'Running Threads: ' + ', '.join(thread.name for
                                                     thread in
                                                     threading.enumerate())
            logging.info(message)

            time.sleep(60 * 60 * 24)
        except KeyboardInterrupt:
            raise
        except Exception, e:
            logging.error(str(e))
