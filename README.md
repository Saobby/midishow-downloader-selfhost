# midishow-downloader-selfhost
 Automatically download midi files on midishow
- - -
[简体中文](https://github.com/Saobby/midishow-downloader-selfhost/blob/main/README_CHS.md)
# Usage
1. Set up Redis  
Download and install Redis for Windows.  
   Since Redis does *not* officially support windows, you can download it from [here](https://github.com/tporadowski/redis/releases/tag/v5.0.14.1).
   
2. Start Redis service  
Press `Win+R`, input `services.msc`, and press `Enter`  
   Find `Redis` in the popped up window, and click `Start` on the left.
   
3. Set Redis address  
In general, you don't need to do extra configuration, just leave them default.  
   But if you want to use a remote Redis server, please config it in `./config.toml`

4. Download midishow downloader  
Download the latest build of the downloader.  
   - [32bit download](https://nightly.link/Saobby/midishow-downloader-selfhost/workflows/build.yaml/main/midishow_downloader-x86.zip)
    - [64bit download](https://nightly.link/Saobby/midishow-downloader-selfhost/workflows/build.yaml/main/midishow_downloader-x64.zip)
    
    If you don't know your computer's architecture, just download the `32-bit` version.  
    You are supposed to get a .zip archive. **Please extract it after you download.**

5. Set your midishow account  
Open `config.toml` and put your midishow username and password below `midishow.accounts` section.  
   If you have multiple accounts, write like this:  
    ```toml
    [[midishow.accounts]]
    username = "username1"
    password = "password1"
    
    [[midishow.accounts]]
    username = "username2"
    password = "password2"
    
    [[midishow.accounts]]
    username = "username3"
    password = "password3"
    ```
   The downloader will use a random account every download.

6. Start the downloader  
Double click `./server.exe` to run the downloader.  
   If everything goes well, your browser should automatically open the downloader's webpage.  
   Type in the midi's url and enjoy!
# Troubleshooting
1. Internal server error, and logs say `redis.exceptions.ConnectionError: Error 10061 connecting to 127.0.0.1:6379.`  
Please make sure you have installed and started Redis. (Please see `Usage` section)  
2. Failed to login  
Please make sure you have set your midishow username and password in `config.toml`  
3. Could not download midi. Please check if your link is correct.  
Please type in the url of the viewing page of the midi, where you can see a piano keyboard, not the download page.
4. Your account is under risk control.  
Please register a new midishow account and retry.

If you have any other problems, please be free to let me know at [Issues](https://github.com/Saobby/midishow-downloader-selfhost/issues).  
Please include the error log while reporting bugs.
# Disclaimer
This tool is built for only educational purpose. It is designed to download midis conveniently. Please respect intellectual property rights. **Do not repost the midi you download to other website without the author's permission. Do not sell the midi you download to others.** The developers of this project shall not be held liable for any damages, losses, or legal issues arising from the use or misuse of this tool. This includes, but is not limited to, any direct, indirect, incidental, or consequential damages. **Users assume all risks associated with the use of this tool.** This disclaimer may be updated or modified at any time without prior notice. Users are encouraged to review it periodically to stay informed about their responsibilities and obligations.
# Contributing
Please feel free to make any contributions.
# Third-Party Licenses
This project uses the following third-party libraries:  
- wux-ui (Original repo has been deleted)
- [tabler-icons](https://github.com/tabler/tabler-icons)
- [Tone.js](https://www.npmjs.com/package/tone)
- [@magenta/music](https://www.npmjs.com/package/@magenta/music)
- [focus-visible](https://www.npmjs.com/package/focus-visible)
- [html-midi-player](https://www.npmjs.com/package/html-midi-player)

Their licenses can be found at `./third_party_licenses`

