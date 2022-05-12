import os
import time
import glob
from pyrogram import Client
from pyrogram.raw.functions.account import ReportPeer
from pyrogram.raw.types import InputReportReasonOther
from dotenv import load_dotenv


def choice_session(sessions: list, res: str) -> str:
    """Request sessions and return str."""
    if res == '' or res.isnumeric():
        if res == '' or not 0 <= int(res) < len(sessions):
            err = input('Incorrect choice. Please repeat: ')
            return choice_session(sessions, err)
        else:
            session_name = sessions[int(res)][:-8]
            return session_name
    elif res.lower() == 'c':
        session_name = input('Enter new session name: ')
        app = Client(
            session_name, os.environ.get('API_ID'),
            os.environ.get('API_HASH'),
            hide_password=True
        )
        app.start()
        app.stop()
        return session_name
    elif res.lower() == 'q':
        exit()


def message_from_file() -> str:
    """Check existing message and return str."""
    if os.path.isfile('message'):
        with open('message') as file:
            msg = file.read().replace('\n', '')
            return msg
    else:
        return None


def target_list_from_file() -> list:
    """Check existing target_list and return list."""
    target_list = []
    if os.path.isfile('target_list'):
        with open('target_list') as file:
            for i in file.readlines():
                i = i[i.find('t.me/')+5:].strip(' \n')
                if i.rfind('/') > 0:
                    i = i[:i.rfind('/')]
                target_list.append(i)
    return target_list


def choice_target_list(session_name: str, app: object) -> list:
    """Request target_list and return list."""
    os.system('clear')
    print(f'Current session: {session_name}')
    target = input('Enter target ([Q] - Quit, [F] - File): ')
    if target.lower() == 'q':
        app.stop()
        exit()
    elif target.lower() == 'f':
        target_list = target_list_from_file()
    else:
        target_list = [target]
    return target_list


def choice_message() -> str:
    """Get message and return str."""
    msg = message_from_file()
    print(f'Send a message: \n{msg}')
    consent = input('Consent? (Y/n): ')
    if consent.lower() == 'n':
        msg = input('Enter new message: ')
        save_msg = input('Save your message for the future? (y/N): ')
        if save_msg == 'y':
            with open('message', 'w+') as file:
                file.write(f'{msg}')
    return msg


def get_session() -> str:
    """Get existing sessions and return str."""
    os.system('clear')
    sessions = glob.glob('*.session')
    print('\nAvailable sessions: ')
    for n, i in enumerate(sessions):
        print(f'[{n}] - {i[:-8]}')
    print('[C] - Create new session')
    print('[Q] - Quit')
    res = input('Select session: ')
    session_name = choice_session(sessions, res)
    return session_name


def input_reports_count(target_list: list) -> int:
    """Request number of reports sent and return int."""
    print(f'Target \n{target_list} \nlocked.')
    reports_count = int(input('Enter reports count: '))
    return reports_count


def bombing(app: object, msg: str, target_list: list, reports_count: int) -> None:
    """Send reports on target_list reports_count times."""
    for target in target_list:
        # Check channel availability
        try:
            t_peer = app.resolve_peer(target)
        except:
            print(f'{target} already blocked :)')
            continue
        if t_peer is not None:
            reports_successful = 0
            print(f'Complain about {target}...')
            # Send report
            while True:
                s = app.invoke(ReportPeer(
                    peer=t_peer,
                    reason=InputReportReasonOther(),
                    message=msg,
                    )
                )
                if 's' in locals():
                    reports_successful += 1
                    print(f'Reports: {reports_successful}/{reports_count}', end='\r')
                    if reports_successful >= reports_count:
                        print(f'Complain about {target}...Done')
                        break
                else:
                    print('\nComplaining ended, sending report failed.')
                    break
                time.sleep(1)
        else:
            print(f'Target \ {target} \ not resolved.')
    print('Complaining ended, all reports sent.')


def choice_repeat(app: object, msg: str, target_list: list,  reports_count: int) -> None:
    """Resend reports with user consent."""
    choice = input('Again? (y/N): ')
    if choice.lower() in ['n', '']:
        app.stop()
        exit()
    elif choice.lower() == 'y':
        bombing(app, msg, target_list, reports_count)
    else:
        print('Incorrect choice. Please repeat')
        choice_repeat(app, msg, target_list, reports_count)


if __name__ == "__main__":
    load_dotenv()
    session_name = get_session()

    app = Client(session_name, os.environ.get('API_ID'), os.environ.get('API_HASH'))
    app.start()

    target_list = choice_target_list(session_name, app)
    msg = choice_message()
    reports_count = input_reports_count(target_list)
    bombing(app, msg, target_list, reports_count)  # TODO: async
    choice_repeat(app, msg, target_list, reports_count)
