"""
A simple Azure function to scrape bubi bike data and save it to blob storage

https://github.com/yokawasa/azure-functions-python-samples/blob/master/v2functions/queue-trigger-blob-in-out-binding/readme.md

https://stackoverflow.com/questions/72904046/how-to-write-to-a-text-file-in-a-blob-container-using-azure-function-with-python

"""

import logging
import azure.functions as func
import datetime as dt
import urllib.request

app = func.FunctionApp()

@app.schedule(schedule="0 */10 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False)
@app.blob_output(arg_name="output", connection="connectionstring",
              path="{DateTime}.json")
def json_downloader(myTimer: func.TimerRequest, output: func.Out[str]) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    time_string = dt.datetime.utcnow().isoformat()
    if "." in time_string:
        time_string = time_string[:time_string.index(".")]

    bubi_json_url = "https://maps.nextbike.net/maps/nextbike-live.json?domains=bh"

    bubi_data = None
    
    try:
        with urllib.request.urlopen(bubi_json_url) as url:
            bubi_data = url.read()
    except Exception as e:
        logging.error(f"Failed to read JSON file: {e}")

    # write data to output blob
    if bubi_data is not None:
        output.set(bubi_data)
        logging.info("Output written to blob storage.")
    else:
        logging.warn("There was no bubi data to write.")
