import argparse


def arg_parse() -> str:
    """
    Парсит аргумент командной строки '--run' и возвращает его значение.

    :return: Значение аргумента `--run`, переданное при запуске скрипта.
    :raises ValueError: Если аргумент не был передан.
    """
    parser = argparse.ArgumentParser(description="Парсинг аргументов запуска сервиса")
    parser.add_argument(
        "--run",
        type=str,
        required=True,
        choices=["api", "worker", "notification"],
    )

    args = parser.parse_args()

    if not args.run:
        raise ValueError(
            "Необходимо передать аргумент '--run' со значением: api, worker или notification"
        )

    return args.run
