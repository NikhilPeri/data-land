import os
from datetime import datetime

def timestamp():
    return datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

def configure_logging(log_dir):
    formatter = logging.Formatter(
        fmt='[%(levelname)s] %(asctime)s.%(msecs)03d | %(message)s',
        datefmt='%Y-%m-%d %I:%M:%-S'
    )

    file_stream = logging.StreamHandler(stream=open(
        os.path.join(log_dir, '{}.log'.format(timestamp())),
        mode='a+'
    ))
    file_stream.setFormatter(formatter)
    file_stream.setLevel(20)

    console_stream = logging.StreamHandler(stream=sys.stdout)
    console_stream.setFormatter(formatter)
    console_stream.setLevel(30)

    logging.getLogger().setLevel(20)
    logging.getLogger().addHandler(file_stream)
    logging.getLogger().addHandler(console_stream)
