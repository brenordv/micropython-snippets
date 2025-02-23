import urequests
import time
import gc


class HttpClient:
    def __init__(self, base_url="", timeout=30, retries=3):
        """
        Initialize the HTTP client.

        :param base_url: Optional base URL to prefix to all requests.
        :param timeout: Timeout for each request (in seconds).
        :param retries: Number of retry attempts for failed requests.
        """
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.retries = retries

    def _build_url(self, path):
        """
        Build the full URL by concatenating the base URL and the path.
        """
        if self.base_url:
            return "{}/{}".format(self.base_url, path.lstrip("/"))
        return path

    def _request(self, method, path, **kwargs):
        """
        Internal method to perform an HTTP request with retry logic.

        :param method: HTTP method as a string (e.g., 'GET', 'POST').
        :param path: URL path or full URL.
        :param kwargs: Additional arguments passed to urequests.request.
        :return: The response content (decoded text).
        :raises Exception: When the maximum number of retries is exceeded.
        """
        url = self._build_url(path)
        attempt = 0
        while attempt < self.retries:
            try:
                # Note: Some versions of urequests do not support a timeout parameter.
                # If yours does not, you can either implement your own or use a different library.
                response = urequests.request(method, url, **kwargs)
                # Read response content. Depending on your use-case, you might read in chunks.
                content = response.text
                response.close()  # Always close the response to free resources.
                gc.collect()  # Force garbage collection to help in long-running apps.
                return response.status_code >= 200 and response.status_code <= 299, {"content": content , "status_code": response.status_code}
            except Exception as e:
                attempt += 1
                print("Error on {} request to {} (attempt {}): {}".format(method, url, attempt, e))
                time.sleep(1)  # Small delay before retrying.
                gc.collect()
        raise Exception("Max retries reached for {} request to {}".format(method, url))

    def get(self, path, params=None, **kwargs):
        """
        Perform an HTTP GET request.

        :param path: URL path or full URL.
        :param params: Dictionary of query parameters to append to the URL.
        :param kwargs: Additional arguments for the request.
        :return: The response content.
        """
        if params:
            # Build a simple query string; note that MicroPython may not have urllib.parse.
            query = "&".join("{}={}".format(key, params[key]) for key in params)
            if "?" in path:
                path += "&" + query
            else:
                path += "?" + query
        return self._request("GET", path, timeout=self.timeout, **kwargs)

    def post(self, path, data=None, json=None, **kwargs):
        """
        Perform an HTTP POST request.

        :param path: URL path or full URL.
        :param data: Data to send in the body (for form-encoded posts, etc.).
        :param json: A JSON-serializable object to send as JSON.
        :param kwargs: Additional arguments for the request.
        :return: The response content.
        """
        if json is not None:
            import ujson  # MicroPython's lightweight JSON module.
            # Ensure the header is set for JSON content.
            kwargs.setdefault("headers", {})
            kwargs["headers"]["Content-Type"] = "application/json"
            data = ujson.dumps(json)


        return self._request("POST", path, data=data, timeout=self.timeout, **kwargs)

