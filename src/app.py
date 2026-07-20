import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    """
    event is the incoming HTTP request.
    Whatever dict we return becomes the HTTP response.
    """
    path = event.get("rawPath", "/")
    method = event.get("requestContext", {}).get("http", {}).get("method", "?")

    logger.info(json.dumps({"msg": "request received", "path": path, "method": method}))

    try:
        if path == "/health":
            body = {"status": "ok"}
            status_code = 200
        elif path == "/hello":
            body = {"message": "Hello from Jay!", "path": path}
            status_code = 200
        else:
            body = {"error": "not found", "path": path}
            status_code = 404

        logger.info(json.dumps({"msg": "request ok", "path": path}))
        return {
            "statusCode": status_code,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(body),
        }
    except Exception:
        logger.exception("request failed")
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "internal server error"}),
        }
