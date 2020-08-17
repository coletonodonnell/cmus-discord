#!/usr/bin/env python3
from pypresence import Presence
from subprocess import check_output
from dotenv import load_dotenv
import os
import nest_asyncio
import asyncio
import datetime
import pickle
import sys
import psutil

def extract_data(cmus_data):
    if cmus_data == "status stopped":
        sys.exit(0)
    else:
        cmus_data = cmus_data.split()
        collector = []

        # Dictionary that will contain our parsed-out data.
        cmus_keys = ['status', 'file', 'artist', 'album',  'discnumber', 'tracknumber', 'title', 'date', 'duration']
        cmus_info = {}

        last_found = None
        it = iter(cmus_keys)
        expected_key = next(it) # the first key
        for value in cmus_data:
            if value == expected_key:
                if last_found is not None: # not the first key
                    cmus_info[last_found] = " ".join(collector)
                    collector = []
                last_found = expected_key
                expected_key = next(it, None) # we know the next expected key
            else:
                collector.append(value)
        cmus_info[last_found] = " ".join(collector)
        artist_length_cutoff = cmus_info["artist"].find("albumartist")
        fix_artist = cmus_info["artist"][:artist_length_cutoff]
        cmus_info["artist"] = fix_artist
        return cmus_info

async def rpc_update(cmus_data):
    client_id = "744268701150478359"
    RPC = Presence(client_id)
    RPC.connect()
    epoch_time = int(datetime.datetime.now().timestamp())
    end_time = epoch_time + int(cmus_data["duration"])
    if cmus_data["status"] == "playing":
        RPC.update(state=f"by {cmus_data['artist']}", details=cmus_data["title"], end=end_time, large_image="cmus_black", large_text="cmus - console music player for Unix")
        await asyncio.sleep(int(cmus_data["duration"]) + 1)
    if cmus_data["status"] == "paused":
        while True:
            RPC. update(details="Paused", large_image="cmus_black", large_text="cmus - console music player")
            await asyncio.sleep(240)
    sys.exit(0)

# Most annoyingly, cmus doesn't support pausing duration directly, so I will need to manage this manually using yet another pkl file (I love pkl files)
async def pause_logic(cmus_data, cmus_loop, DIRECTORY):
    x = open(f"{DIRECTORY}pause.pkl", "rb")
    de_pickled_pause_data = pickle.load(x)
    total_duration = int(cmus_data["duration"])
    name = cmus_data["title"]
    if name in de_pickled_pause_data:
        if cmus_data["status"] == "paused":
            cmus_data["duration"] = de_pickled_pause_data[1]
            cmus_loop.create_task(rpc_update(cmus_data))
        if cmus_data["status"] == "playing":
            cmus_data["duration"] = de_pickled_pause_data[1]
            cmus_loop.create_task(rpc_update(cmus_data))
            total_duration = de_pickled_pause_data[1]
            while True:
                await asyncio.sleep(1)
                x = open(f"{DIRECTORY}pause.pkl", "wb")
                total_duration -= 1
                to_pickle = [name, total_duration]
                pickle.dump(to_pickle, x)
                x.close()
    else:
        cmus_loop.create_task(rpc_update(cmus_data))
        while True:
            await asyncio.sleep(1)
            x = open(f"{DIRECTORY}pause.pkl", "wb")
            total_duration -= 1
            to_pickle = [name, total_duration]
            pickle.dump(to_pickle, x)
            x.close()

async def script_check(DIRECTORY):
    await asyncio.sleep(0.5)
    check =  str(int(datetime.datetime.now().timestamp()))
    x = open(f"{DIRECTORY}check.pkl", "wb")
    pickle.dump(check, x)
    new_check = check
    while new_check == check:
        x = open(f"{DIRECTORY}check.pkl", "rb")
        new_check = pickle.load(x)
        x.close()
        await asyncio.sleep(0.1)
    sys.exit(0)

async def check_cmus():
    while True:
        cmusStatus = "cmus" in (p.name() for p in psutil.process_iter())
        if cmusStatus:
            await asyncio.sleep(5)
        else:
            sys.exit(0)

async def main():
    load_dotenv()
    DIRECTORY = os.getenv("FULL_DIRECTORY")
    nest_asyncio.apply()
    cmusStatus = "cmus" in (p.name() for p in psutil.process_iter())
    if cmusStatus:
        cmus_data = extract_data(sys.argv[1])
        cmus_loop = asyncio.get_event_loop()
        cmus_loop.create_task(script_check(DIRECTORY))
        cmus_loop.create_task(check_cmus())
        cmus_loop.create_task(pause_logic(cmus_data, cmus_loop, DIRECTORY))
        cmus_loop.run_forever()
    else:
        print("cmus isn't running, are you executing this separate of cmus...? Please look at the README to see how to use this script.")

if __name__ == "__main__":
    main_loop = asyncio.get_event_loop()
    main_loop.run_until_complete(main())