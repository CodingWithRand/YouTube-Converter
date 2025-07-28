# YouTube Converter - *By Rand*

Thank you so much to download my YouTube converter and downloader program.

This program create in Python programming language
I use the pytube library for the conversion system and tkinter library for the whole UI.
Right now the progress on fixing some mistakes and glitches is probably 95% which mean the program can be mostly used without facing any problem!


# Version Update Logs

## *__v1.0__*
- Released the program
- *__Describe more about the program here (Remind my self)__*

## *__v1.0.1__* 
- Fixed pytube conversion bug
- Fixed problem on downloading the video that has the unsupported character in the file name

## *__v1.1__* 
- Completely fixed pytube conversion bug
- Playlist conversion is fully available
- Fixed some minor bugs.

## *__v1.2__* 
- Audio mp3 format is a proper format now!

## *__v1.2.1__*
- Fixed moviepy package glitches

## *__v1.3__*
- Create thread for downloading process to prevent the app crash

## *__v1.3.1__*
- One video downloading process has been isolated from the main thread!

## *__v1.3.2__*
- Playlist video downloading process has been isolated from the main thread!

## *__v1.4__*
- Migrate to pytubefix

## *__v1.4.1__*
- Upgrade pytubefix to version 8.12.3

## *__v1.5__*
- Upgrade pytubefix to version 9.4.1
- Change the methodology of conversion
    <br>
    __Old:__ Download as mp4 and convert it to mp3 for audio conversion
    <br>
    __New:__ Download mp4 and mp3 separately and merge them using ffmpeg.exe for video conversion
- Resolution option is added for video conversion.
- Resolve the problem with bot detection by introducing oauth verification portal*

## *__Additional Notes__*
### \* ###
__Oauth verification__ is required for new users. They will receive a code from the message box that shows up when they do their first conversion, and the verification portal will be opened in their default browser. Users will have to enter the code in the input field, and then link their google account to a device (If you concern about your account security, you may use an alternative google account. But from what I've tried so far, nothing yet happened to my account.) After the verification process is finished, you may close the portal page, and click the "OK" button on the message box to continue the conversion. __DON'T CLICK THE "OK" BUTTON BEFORE FINISHING THE VERIFICATION PROCESS AS THE PROGRAM WILL SHOW AN ERROR!__
