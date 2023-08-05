from fire import Fire

from mailgun.mailgun import Mailgun

def run():
    api = Mailgun()
    Fire(Mailgun)

if __name__ == '__main__':
    run()
