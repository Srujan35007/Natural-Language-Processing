import praw 
import time 
from curtsies.fmtfuncs import red, blue, cyan, yellow, bold # pip3 install curtsies
from argparse import ArgumentParser as AP 

reddit = praw.Reddit(
    client_id = 'CLIENT_ID',
    client_secret = 'CLIENT_SECRET',
    username = 'REDDIT_USERNAME',
    password = 'REDDIT_PASSWORD',
    user_agent = 'USER_AGENT'
)
print('User Authorized.\n')

def get_comments_and_replies(subreddit_name):
    start_time = time.time()
    with open(f'./Comments_and_Replies_{subreddit_name}.txt', 'w') as write_file:
        submission_ids = []
        sub = reddit.subreddit(subreddit_name)
        count = 0
        submission_count = 0
        write_file.write('submission_id<::>parent_id<::>comment_id<::>comment_body<::>comment_score\n'.upper())
        for submission in sub.top('all', limit=999):
            submission_count += 1
            for comment in submission.comments.list():
                try:
                    submission_id = str(submission.id)
                    parent_id = str(comment.parent())
                    comment_id = str(comment.id)
                    content = str(comment.body).replace('\n', '<NEWLINE>')
                    write_file.write(f"{submission_id}<::>{parent_id}<::>{comment_id}<::>{content}<::>{comment.score}\n")
                    count += 1
                    if count == 1:
                        print(cyan(f"Started scraping {subreddit_name}"))
                    elif count % 10000 == 0:
                        time_taken = time.time()/60-start_time/60
                        ETA = (1-submission_count/999)/(submission_count/999)*time_taken
                        print("%d Comments downloaded.\t%.2f Mins. passed.\t%.2f Comments/Min."%(count, time_taken, count/time_taken), end='\t')
                        print(bold(cyan(f'({submission_count}/999)')), yellow(f'ETA: {round(ETA,2)} Mins.'))
                    else:
                        pass
                except Exception as E:
                    pass
                
    print(bold(red(f"Total comments from {subreddit_name} = {count}\n\n")))
                    
if __name__ == '__main__':
    parser = AP()
    parser.add_argument('subreddits_comma_seperated')
    args = parser.parse_args()
    subreddits = sorted(list(set(args.subreddits_comma_seperated.split(','))))
    for subreddit_ in subreddits:
        try:
            print(bold(cyan(f"Subreddit ({subreddits.index(subreddit_)+1}/{len(subreddits)})")))
            get_comments_and_replies(subreddit_)
        except:
            print(red(f"Skipping {subreddit_}"))
