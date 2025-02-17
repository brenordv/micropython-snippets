import os
import time
import ujson


class ErrorLogManager:
    def __init__(self, log_folder="logs", ntp_helper = None):
        """
        Initializes the ErrorLogManager with a log folder and an optional NTP helper.
        :param log_folder: The folder where the log files will be stored.
        :param ntp_helper: An NTP helper to get the local time. This is a reference to the class NtpHelper in the
        network_helpers package of this repo.
        """
        self.log_folder = log_folder
        self.ntp_helper = ntp_helper
        self._create_log_folder_if_not_exists()

    def _create_log_folder_if_not_exists(self):
        """Creates the log folder if it does not exist."""
        try:
            if not self._folder_exists(self.log_folder):
                os.mkdir(self.log_folder)
        except OSError as e:
            print("Failed to create log folder:", e)

    def _folder_exists(self, folder_path):
        """Checks if a folder exists."""
        try:
            return os.stat(folder_path)[0] & 0o40000 == 0o40000  # Checking if it's a directory
        except OSError:
            return False

    def _get_local_time(self):
        """Returns the current local time."""
        if self.ntp_helper:
            return self.ntp_helper.get_local_time()

        return "{}".format(time.time())

    def log_error(self, error_message, error_object=None):
        """Logs an error message and an error object to a log file with a timestamp."""
        timestamp = self._get_local_time().replace(":", "-").replace("/", "-")
        log_file = "{}/error_{}.log".format(self.log_folder, timestamp)

        log_data = {
            "timestamp": timestamp,
            "error_message": error_message,
            "error_object": str(error_object) if error_object else {}
        }

        try:
            with open(log_file, "w") as f:
                ujson.dump(log_data, f)
        except OSError as e:
            print("Failed to write to log file:", e)

    def list_logs(self):
        """Lists all log files in the log folder."""
        try:
            return os.listdir(self.log_folder)
        except OSError as e:
            print("Failed to list logs:", e)
            return []

    def read_log(self, log_filename):
        """Reads a specific log file and returns the JSON content."""
        try:
            with open("{}/{}".format(self.log_folder, log_filename), "r") as f:
                return ujson.load(f)
        except OSError as e:
            print("Failed to read log file:", e)
            return None
        except ujson.JSONDecodeError as e:
            print("Failed to parse log file:", e)
            return None

    def delete_log(self, log_filename):
        """Deletes a specific log file by name."""
        try:
            os.remove("{}/{}".format(self.log_folder, log_filename))
            print("Log file deleted successfully.")
        except OSError as e:
            print("Failed to delete log file:", e)
