import logging
import sys

LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | "
    "%(filename)s:%(lineno)d | %(message)s | user_id=%(user_id)s"
)


class SafeFormatter(logging.Formatter):
    def format(self, record):
        if not hasattr(record, "user_id"):
            record.user_id = "-"
        return super().format(record)


def setup_logging():
    formatter = SafeFormatter(
        LOG_FORMAT,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler("app.log", encoding="utf-8")
    file_handler.setFormatter(formatter)

    logging.basicConfig(
        level=logging.INFO,
        handlers=[console_handler, file_handler],
    )

    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
