import asyncio
import aiohttp
import json
from datetime import datetime, timedelta
from .helpers import extract_info, create_timelines_url

async def fetch_timeline(session, url, headers):
    async with session.get(url, headers=headers) as response:
        return await response.json()

async def get_recent_timelines(access_token, instance_url, output_file, local=False):
    headers = {'Authorization': f'Bearer {access_token}'}
    date_limit = datetime.now() - timedelta(minutes=605) # only get data 10 hours before.
    max_id = None
    count = 0

    async with aiohttp.ClientSession() as session:
        while True:
            search_url = create_timelines_url(instance_url, max_id, local)
            try:
                data = await fetch_timeline(session, search_url, headers)
            except Exception as e:
                print(f"Error requesting timelines: {str(e)}")
                await asyncio.sleep(1)
                continue

            if data:
                if "error" in data:
                    print(f"Error requesting timelines: {data['error']}")
                    if data["error"] == "Too many requests":
                        await asyncio.sleep(10)
                    continue
                try:
                    with open(output_file, 'a') as f:
                        for status in data:
                            created_at = datetime.strptime(status['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
                            if created_at >= date_limit:
                                info = extract_info(status)
                                if info:
                                    count += 1
                                    json.dump(info, f)
                                    f.write("\n")
                            else:
                                print(f"ID: {status['id']} reached date limit")
                                return count
                    max_id = data[-1]['id']
                except Exception as e:
                    print(f"Error setting status data: {str(e)}")
                    print("Data:", json.dumps(data))
                    continue
            else:
                print("No data returned")
                break
            await asyncio.sleep(1)
    return count