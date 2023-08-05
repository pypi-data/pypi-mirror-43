# mailgun-cli
control mailgun account using cli and python api

## Features
- easily create routes for 1-on-1 forwarding mail using a csv file or Google Spreadsheet

## Usages
### Cli
set the mailgun api key
```bash
# bash shell
$ export MAILGUN_API_KEY [your private API key]
# fish shell
$ set -X MAILGUN_API_KEY [your private API key]
```
You could permanently set it in `~/.bash_profile` or `~/.config/fish/config.fish`

*list all routes*
```bash
$ mailgun routes
```
*forward using a csv*
```bash
$ mailgun 
```

## install
```
$ pip install mailgun-cli 
```
✨🍰✨

## Forward templete
1. Grab Google Spreadsheet, [Here is a templete](https://docs.google.com/spreadsheets/d/1JOKoNcUMIYtUiahQfP309BhpqU-5uPir1UcsAmLkKaY/edit?usp=sharing). 
   1. First publish your Google sheet to the web by going to File > Publish to the web...
   2. Choose the tab you want, then select Comma-separated values (.csv) as the export format
   3. Grab the URL

## Learning Path
https://codingdose.info/2018/08/02/develop-and-publish-with-poetry/