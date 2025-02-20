from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    # Add a custom header
    flow.request.headers["X-Forwarded-For"] = "localhost"
