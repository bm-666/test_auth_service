import asyncio

from app import main
from enums.enums import ServiceEnum
from services.email_notification import notification_run
from utils.utils import arg_parse
from workers.send_email import worker_run

if __name__ == "__main__":
    args = arg_parse()
    if args == ServiceEnum.API:
        main()

    elif args == ServiceEnum.WORKER:
        asyncio.run(worker_run())

    elif args == ServiceEnum.NOTIFICATION:
        asyncio.run(notification_run())
