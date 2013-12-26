import psutil
from raven import Client
from settings import RAVEN_CALLBACK_URL, RAVEN_TIMEOUT

client = Client(RAVEN_CALLBACK_URL, timeout=RAVEN_TIMEOUT)


def mb(bytes):
    return bytes / 1024.0 / 1024.0


def percent_left(percent):
    return 100 - percent


def notify(message):
    print message
    #client.captureMessage(message)


def check_ram(limit=90):
    use = psutil.virtual_memory()
    free = use.free + use.cached + use.buffers

    if use.percent > limit:
        notify('Less than {limit}% RAM ({mb} mb) available.'.format(limit=percent_left(limit), mb=mb(free)))


def check_swap(limit=75):
    use = psutil.swap_memory()

    if use.percent > limit:
        notify('Less than {limit}% swap ({mb} mb) left.'.format(limit=percent_left(limit), mb=mb(use.free)))


def check_disk(limit=95, path='/'):
    use = psutil.disk_usage(path)

    if use.percent > limit:
        notify('Less than {limit}% disk ({mb} mb) available.'.format(limit=percent_left(limit), mb=mb(use.free)))


def check_cpu(limit=98, interval=0.1):
    use = psutil.cpu_percent(interval=interval)

    if use > limit:
        notify('CPU usage at {use}%.'.format(use=use))


if __name__ == "__main__":
    check_ram()
    check_swap()
    check_disk()
    check_cpu()
