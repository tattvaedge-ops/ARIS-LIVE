import os


def run_self_diagnostics():
    report = {
        "status": "healthy",
        "checks": {}
    }

    # OPENAI KEY
    if os.getenv("OPENAI_API_KEY"):
        report["checks"]["openai_api_key"] = "OK"
    else:
        report["checks"]["openai_api_key"] = "MISSING"
        report["status"] = "warning"

    # SECRET KEY
    if os.getenv("SECRET_KEY"):
        report["checks"]["secret_key"] = "OK"
    else:
        report["checks"]["secret_key"] = "MISSING"
        report["status"] = "warning"

    # KLING KEY
    if os.getenv("KLING_ACCESS_KEY"):
        report["checks"]["kling_access_key"] = "OK"
    else:
        report["checks"]["kling_access_key"] = "MISSING"

    # DATABASE
    if os.path.exists("aris_memory.db"):
        report["checks"]["database"] = "OK"
    else:
        report["checks"]["database"] = "MISSING"
        report["status"] = "warning"

    # UPLOAD FOLDER
    if os.path.exists("uploads"):
        report["checks"]["uploads_folder"] = "OK"
    else:
        report["checks"]["uploads_folder"] = "MISSING"
        report["status"] = "warning"

    return report