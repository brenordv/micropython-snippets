from lib.error_log_manager import ErrorLogManager

log_manager = ErrorLogManager("logs")

try:
    # Simulating an error
    1 / 0
except Exception as e:
    log_manager.log_error("Division by zero error", e)

# List logs
logs = log_manager.list_logs()
print("Logs available:", logs)

# Read first log if exists
if logs:
    log_content = log_manager.read_log(logs[0])
    print("First log content:", log_content)

#Delete the first log file
# if logs:
#     log_manager.delete_log(logs[0])
#     print("Deleted log:", logs[0])
