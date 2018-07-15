---
layout: post
title: "Update Cloudflare DNS settings with Python"
date: 2018-07-15 15:30:00
categories: python cloudflare dns
description: Automatically update cloudflare DNS settings with python when you have a dynamic IP
published: false
---

# Introduction

I have been slacking on blogging for quite a long time and here is a simple thing I did today
that I can blog about without putting much thought into it :).

Hopefully someone will find this useful.

# Problem

You have a dynamic IP address at home that you want to point a DNS entry at.

This is fine normally; however, regular home internet lines do not have static IPs.


# Solution

Use Cloudflare's API with a Python script running with a cronjob to make sure your
DNS entry is always updated with the correct IP address.


# Requirements


- Computer running on your home network(in my case, a Raspberry Pi Zero)
- Python
- DNS managed by Cloudflare
- DNS record id to update


# Install `requests` library

The script we'll run just needs the `requests` libary installed.

```
sudo pip3 install requests
```


# The Script

Save a file with the following contents into the file `/opt/update-dns.py`.


```python
import requests
import json
import sys


# XXX Settings you need to update!!!
IP_API = 'https://api.ipify.org?format=json'
# Get CF API Key: https://support.cloudflare.com/hc/en-us/articles/200167836-Where-do-I-find-my-Cloudflare-API-key-
CF_API_KEY = 'REPLACE ME'
# Your cloudflare email address
CF_EMAIL = 'REPLACE@ME.COM'
# Your zone id is located on the main cloudflare domain dashboard
ZONE_ID = 'REPLACE ME'
# Run script once without this set and it'll retrive a list of records for you to find the ID to update here
RECORD_ID = ''


if not RECORD_ID:
    resp = requests.get(
        'https://api.cloudflare.com/client/v4/zones/{}/dns_records'.format(ZONE_ID),
        headers={
            'X-Auth-Key': CF_API_KEY,
            'X-Auth-Email': CF_EMAIL
        })
    print(json.dumps(resp.json(), indent=4, sort_keys=True))
    print('Please find the DNS record ID you would like to update and entry the value into the script')
    sys.exit(0)

resp = requests.get(IP_API)
ip = resp.json()['ip']


resp = requests.put(
    'https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}'.format(
        ZONE_ID, RECORD_ID),
    json={
        'type': 'A',
        'name': 'foo.bar.com',
        'content': ip,
        'proxied': False
    },
    headers={
        'X-Auth-Key': CF_API_KEY,
        'X-Auth-Email': CF_EMAIL
    })
assert resp.status_code == 200

print('updated dns record for {}'.format(ip))
```

In the file, you will need to update the variables `CF_API_KEY`, `CF_EMAIL`, `ZONE_ID` and `RECORD_ID`.

Test running the script with:

```bash
python3 /opt/update-dns.py
```

If it worked, you would receive output, `updated dns record for`.


# Cron

Now, to have this running continuously, we can simply use cron.


Edit your cron file.

```bash
sudo crontab -e
```

Add the following line:


```
@hourly /usr/bin/python3.5 /opt/update-dns.py
```

And that should be it!