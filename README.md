# midishow-downloader-selfhost
 Automatically download midi files on midishow
- - -
# Usage
1. Set up Redis  
Download and install Redis for Windows.  
   Since Redis does not officially support windows, you can download it from [here](https://github.com/tporadowski/redis/releases/tag/v5.0.14.1).
   
2. Start Redis service  
Press `Win+R`, input `services.msc`, and press `Enter`  
   Find `Redis` in the popped up window, and click `Start` on the left.
   
3. Set Redis address  
In general, you don't need to do extra configuration, just leave them default.  
   But if you want to use a remote Redis server, please config it in `./config.toml`

4. Download midishow downloader

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
# Troubleshooting
If you have any problems, please be free to let me know at [Issues](https://github.com/Saobby/midishow-downloader-selfhost/issues).  
Please include the error log while reporting bugs.
# Third-Party Licenses
This project uses the following third-party libraries:  
- wux-ui (Origin repo has been deleted)
- [tabler-icons](https://github.com/tabler/tabler-icons)
- [Tone.js](https://www.npmjs.com/package/tone)
- [@magenta/music](https://www.npmjs.com/package/@magenta/music)
- [focus-visible](https://www.npmjs.com/package/focus-visible)
- [html-midi-player](https://www.npmjs.com/package/html-midi-player)

Their licenses can be found at `./third_party_licenses`