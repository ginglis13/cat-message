# cat-message
gets images/gifs/videos of cats from reddit, sends to mom via an Applescript.

## get_cats.py

As the name of the file suggests, this script is for finding cat media posts on reddit and downloading these posts to the working directory. The script names each file `cat.[relevant extension]`, and before writing this file, the script deletes each file named `cat.*`. There are a few shortcomings to this file as are outlined in the section titled Shortcomings. If the script runs into any errors/can't get the media type, a message is printed to `stderr`.

## msg_cat.scpt

This is the Applescript for sending a cat file to the recipient of your choice. Since GitHub doesn't really deal with Applescripts very well, the entire script is copied below:

```applescript
# to customize: change the things in all caps
# PATH_TO_REPOSITORY, RECIPIENT_PHONE_NUMBER, YOUR_APPLE_ID

# ginglis

on run argv
	# find the cat file
	set path_to_file to do shell script "find PATH_TO_REPOSITORY -mindepth 1 -name 'cat*'"
	
	# set it as a POSIX file
	set my_file to (path_to_file as POSIX file)
	
	set post_title to (item 1 of argv)
	
	# send stuff
	tell application "Messages"
		set theBuddy to buddy "RECIPIENT_PHONE_NUMBER" of service "E:YOUR_APPLE_ID"
		send post_title to theBuddy
		send my_file to theBuddy
	end tell
end run
```

As you can see from the comments, the three elements of the script to change in order to get it to work are `PATH_TO_REPOSITORY`, `RECIPIENT_PHONE_NUMBER`, and `YOUR_APPLE_ID`. Of course, in order to run this script, you must be using a Mac and have an Apple ID.

## run.sh

This is a short and simple shell script I made just to consolidate the Python script and the Applescript to essentially one script. It simply runs `get_cats.py`, captures the output (the post title), and passes this output as an argument to the Applescript, which sends the post title in addition with the post media. I run this script on a cronjob that executes daily.

## Subreddits

- [cats](https://www.reddit.com/r/cats)
- [catsstandingup](https://www.reddit.com/r/catsstandingup)
- [catslaps](https://www.reddit.com/r/catslaps)
- [catsareassholes](https://www.reddit.com/r/catsareassholes)
- [chonkers](https://www.reddit.com/r/chonkers)
- [bigcatgifs](https://www.reddit.com/r/bigcatgifs)
- [babybigcatgifs](https://www.reddit.com/r/babybigcatgifs)
- [holdmycatnip](https://www.reddit.com/r/holdmycatnip)

## Checklist

- [X] Find and save images
- [X] Handle gyfcat
- [X] Handle imgur
- [ ] Handle YouTube
- [X] Applescript to send iMessage
- [X] Include the post title in iMessage
- [ ] Comment Code, clean up, document

## Shortcomings

Unfortunately, requesting videos from reddit (sources that include `v.redd.it`) resulted in reddit detecting that a script was making too many requests to the site. Since posts of that format from these subreddits seems to be a rarity, I will not be attempting a workaround. Also, no implementation has been made for YouTube posts. My reasononing for not finding a workaround to these issues is that the rate of finding other media types is high enough to justify the script not working occasionally when it finds media from these sources. I use this once a day to send a cat to my mom, and if on one day it doesn't work, it's not a huge deal.
