# BloomSky-2-Weather-Underground
A quick and dirty Python Script to get BloomSky to report to Weather Underground given BloomSky native integration to WU has recently stopped working (as of approx. 24 January 2022).
This is intended to help existing BloomSky users who have Weather Underground ("WU") Personal Weather Stations ("PWS") to sustain them.   
I hope BloomSky gets the integration working again.  Guess we'll see.....

I am not related to BloomSky, Inc or its affiliates. I am just a BloomSky owner with a problem since BloomSky's integration stopped.
There is no warranty expressed or implied in this script.
There are some BloomSky data elements not covered by the script (like UV, and some rain measurements, luminence etc)
Do not use this for any mission critical, life supporting, or other sensitive uses (not that I think NASA uses a BloomSky to schedule launches or anything but....)

It is a simple standalone simple script that reads the data for a BloomSky station from the BloomSky API, then parses that data and uploads it to a WU PWS.

It requires
1. A BloomSky API Key (you find that for your station at https://dashboard.bloomsky.com/user
   then click on "Developers" on the lower left and your API Key should be shown (will look
   like sN-vtc_XXXXXXXXXXXXXXXXXXXXd8qtg== (not a real key)
2. A Weather Underground Account and Private Weather Station configured, and the WU PWS ID and Key
   See https://www.wunderground.com/member/devices.
   Station ID looks like KUTXXXXXX, and Key looks KhExz5qS (not a real key)
3. Configuration below to be updated within
4. A task scheduler / cron job to run this script every X minutes (I do 5 and use Windows Task Scheduler in the background 
5. A python instance to run the script with (I used a new install of Python 3.10.2 on Windows without any issues or need to add any modules etc.)


Good luck!   If you have any issues post to the BloomSky Weather User's Group or leave a comment on the GitHub
