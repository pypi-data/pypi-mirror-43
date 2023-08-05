__version__ = '0.1.0'
from fire import Fire

from mailgun.mailgun import Mailgun

if __name__ == '__main__':
    api = Mailgun()
    Fire(Mailgun)
