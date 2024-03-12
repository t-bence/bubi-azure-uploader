"""
A simple Azure function to scrape bubi bike data and save it to blob storage

https://github.com/yokawasa/azure-functions-python-samples/blob/master/v2functions/queue-trigger-blob-in-out-binding/readme.md

https://stackoverflow.com/questions/72904046/how-to-write-to-a-text-file-in-a-blob-container-using-azure-function-with-python

"""

import logging
import azure.functions as func
import datetime as dt
import urllib.request
import json

app = func.FunctionApp()

@app.schedule(schedule="0 */10 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
#@app.blob_output(arg_name="output", connection="connectionstring",
#              path="{DateTime}.json")
def json_downloader(myTimer: func.TimerRequest) -> None: #, output: func.Out[str]) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    time_string = dt.datetime.utcnow().isoformat()
    if "." in time_string:
        time_string = time_string[:time_string.index(".")]

    bubi_json_url = "https://maps.nextbike.net/maps/nextbike-live.json?domains=bh"

    available_bikes = 0
    
    try:
        with urllib.request.urlopen(bubi_json_url) as url:
            bubi_data = json.load(url)
            available_bikes = bubi_data["countries"][0]["available_bikes"]

    except Exception as e:
        logging.error(f"Failed to read JSON file: {e}")


    logging.info(f"There were {available_bikes} available bikes at {time_string}")

    #output.set(available_bikes)
    