"""
A simple Azure function to scrape bubi bike data and save it to blob storage

https://github.com/yokawasa/azure-functions-python-samples/blob/master/v2functions/queue-trigger-blob-in-out-binding/readme.md

https://stackoverflow.com/questions/72904046/how-to-write-to-a-text-file-in-a-blob-container-using-azure-function-with-python

"""

import logging
import azure.functions as func
import datetime as dt

app = func.FunctionApp()

@app.schedule(schedule="0 */10 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False)
@app.blob_output(arg_name="output", connection="connectionstring",
              path="{DateTime}.json")
def timer_trigger(myTimer: func.TimerRequest, output: func.Out[str]) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    time_string = dt.datetime.utcnow().isoformat()

    content = f"Hello world, the time is: {time_string}"

    output.set(content)
    
    logging.info('Python timer trigger function executed.')