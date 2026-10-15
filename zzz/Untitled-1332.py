import time
from datetime import datetime

import requests

URL = "https://spo-13.mskobr.ru/"
INTERVAL = 300        # пауза между проверками, секунд (5 минут)
TIMEOUT = 15          # сколько ждать ответа, секунд
LOG_FILE = "site_check.log"

HEADERS = {
    # Представляемся обычным браузером: многие сайты блокируют python-requests
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0 Safari/537.36"
    )
}


def log(message: str) -> None:
    """Печатает сообщение с временем и дублирует его в файл."""
    line = f"[{datetime.now
():%Y-%m-%d %H:%M:%S} {message}"
    print(line, flush=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def check_site() -> None:
    try:
        start = time.monotonic()
        r = requests.get(URL, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        elapsed = time.monotonic() - start

        if r.ok:  # любой код 200–399 считаем успехом
            log(f"OK: код {r.status_code}, ответ за {elapsed:.2f} с")
        else:
            log(f"ВНИМАНИЕ: сайт вернул код {r.status_code} ({r.reason})")

    except requests.exceptions.Timeout:
        log(f"ВНИМАНИЕ: сайт не ответил за {TIMEOUT} с")
    except requests.exceptions.SSLError as e:
        log(f"ВНИМАНИЕ: проблема с SSL-сертификатом — {e}")
    except requests.exceptions.ConnectionError as e:
        log(f"ВНИМАНИЕ: не удалось подключиться — {e}")
    except requests.exceptions.RequestException as e:
        log(f"ВНИМАНИЕ: ошибка запроса — {e}")


def main() -> None:
    log(f"Старт мониторинга {URL}, интервал {INTERVAL} с")
    try:
        while True:
            check_site()
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        log("Мониторинг остановлен пользователем")


if __name__ == "__main__":
    main()