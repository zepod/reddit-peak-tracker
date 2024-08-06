import praw
import pandas as pd
from datetime import datetime
import schedule
import time
import logging


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize the Reddit client
reddit = praw.Reddit(
    client_id='XXXXX',
    client_secret='XXXXX',
    user_agent='XXXXX'
)

# List of subreddits to monitor
subreddits = ['IndieGaming', 'indiegames', 'Games', 'gaming', 'rpg_gamers']

# Path to the CSV file
csv_file = 'track_record.csv'

def fetch_active_users():
    logging.info('Starting to fetch active users.')
    data = {}
    timestamp = datetime.now().strftime('%Y-%m-%d %H:00:00')
    data['Timestamp'] = [timestamp]

    for subreddit in subreddits:
        try:
            logging.info(f'Fetching data for subreddit: {subreddit}')
            subreddit_instance = reddit.subreddit(subreddit)
            data[subreddit] = [subreddit_instance.active_user_count]
            logging.info(f'Active users in {subreddit}: {subreddit_instance.active_user_count}')
        except Exception as e:
            data[subreddit] = [None]
            logging.error(f'Error fetching data for {subreddit}: {e}')

    df = pd.DataFrame(data)

    try:
        existing_df = pd.read_csv(csv_file)
        updated_df = pd.concat([existing_df, df], ignore_index=True)
        logging.info('CSV file loaded successfully.')
    except FileNotFoundError:
        updated_df = df
        logging.warning('CSV file not found. A new file will be created.')

    updated_df.to_csv(csv_file, index=False)
    logging.info('CSV file updated successfully.')

# Schedule the task to run every hour
schedule.every().hour.do(fetch_active_users)
logging.info('Task scheduled to run every hour.')


# Run the scheduling loop
if __name__ == "__main__":
    print('Script started.')
    logging.info('Script started.')
    fetch_active_users()  # Run once at start
    while True:
        schedule.run_pending()
        time.sleep(600)
        logging.info('Waiting for the next schedule.')
