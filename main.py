import aiohttp
from aiohttp import ClientTimeout
import asyncio
import csv
from collections import Counter

# 1 second
get_timeout = ClientTimeout(total=1)


async def check(urls: str) -> Counter:
    local = Counter()
    async with aiohttp.ClientSession() as session:
        # split resources separated by |
        for url in [x.strip() for x in urls.split('|')]:
            try:
                async with session.get(url, timeout=get_timeout) as response:
                    print("Get", url)
                    status = response.status
                    # print("Status:", status)
                    if status == 200:
                        print("Open!")
                        local[0] += 1
                    elif status == 301:
                        location = response.headers['location']
                        # print("Location:", location)
                        # repeat with redirect location
                        local.update(await check(location))
                    elif status == 302:
                        location = response.headers['location']
                        # print("Location: ", location)
                        if location.find('warning.rt.ru'):
                            print("Blocked!")
                            local[1] += 1
                        else:
                            # print("Unexpected location:", location, "for", url)
                            local[2] += 1
                    else:
                        # print("Unexpected status: ", status)
                        local[3] += 1
            except Exception:
                if url.startswith('https://'):
                    # repeat with http
                    local.update(await check(url.replace('https://', 'http://')))
                else:
                    local[4] += 1
    return local


if __name__ == '__main__':
    counter = Counter()
    loop = asyncio.get_event_loop()
    p = 0

    with open('dump.csv', 'r', encoding='iso-8859-1') as f:
        total = sum(1 for line in f)
    print("Found", total, "lines")

    with open('dump.csv', 'r', encoding='iso-8859-1') as f:
        for line in csv.reader(f, delimiter=';'):
            p += 1
            print("Progress %d%%" % (p * 100 / total), end='\r')
            domain = line[1]
            resource = line[2]
            # print("Check", domain, resource)
            counter.update(loop.run_until_complete(check(resource)))
            print(p, "Check", domain, resource, counter)

        # in main, close line of progress
        print("")
