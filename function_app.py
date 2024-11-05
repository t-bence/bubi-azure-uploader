import datetime as dt
import os
import urllib.request
import logging
import azure.functions as func

app = func.FunctionApp()

@app.schedule(schedule="0 */10 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False)
@app.blob_output(arg_name="output", connection="AzureWebJobsStorage",
              path="jsons/{DateTime}.json")
def json_downloader(myTimer: func.TimerRequest, output: func.Out[str]) -> None:
    logging.info(f"Running at {dt.datetime.now().isoformat()}")
    if myTimer.past_due:
        logging.info('The timer is past due!')
    
    bubi_json_url = os.environ["TARGET_URL"]

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
        logging.warning("There was no bubi data to write.")
