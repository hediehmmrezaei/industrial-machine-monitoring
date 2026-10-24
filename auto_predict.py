import subprocess
import sys
import time
import logging

logging.basicConfig(
    filename="monitoring.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

while True:
    try:
        logging.info("Checking for new sensor readings")

        result = subprocess.run(
            [sys.executable, "batch_predict.py"],
            capture_output=True,
            text=True,
            check=True
        )

        logging.info("Prediction job completed successfully")

        if result.stdout.strip():
            logging.info(result.stdout.strip())

        print("Prediction cycle completed.")

    except subprocess.CalledProcessError as e:
        logging.error(
            "Prediction job failed: %s",
            e.stderr or str(e)
        )
        logging.warning("ALERT: Machine monitoring pipeline requires attention!")
        print("Prediction failed. Check monitoring.log")

    time.sleep(30)