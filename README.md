# Telegram channels report
[Pyrogram](https://github.com/pyrogram/pyrogram)-based telegram 🇺🇦LOIC.
###### Warning! Made for educational purposes only. Use at own risk.
## Preparing:
`git clone https://github.com/Melhin8/telegram_channels_report.git`
`cd telegram_channels_report`
`pipenv install`

Create file `.env` and set variables `API_ID` and `API_HASH` as string [your credentials] (https://my.telegram.org/apps)

Optionally, make changes to the `target_list` file by including a list of links to telegram complaint channels. Each link is on a new line.

## Using:
Run `pipenv run channels_reports.py`.