from flask import current_app, request
from mastodon import Mastodon
import json, time

def main():
    m = Mastodon(
        api_base_url=f'https://mastodon.au'
    )

    # Get the ID of the lastid status main the public timeline
    lastid= m.timeline(timeline='public', since_id=None, limit=1, remote=True)[0]['id']

    # Sleep for 5 seconds to allow for some status to be posted before we fetch them
    time.sleep(5)

    # Fetch the statuses from the public timeline since the lastid
    return json.dumps(m.timeline(timeline='public', since_id=lastid, remote=True), default=str)
