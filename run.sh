#!/bin/sh
# capture output of script to pass info to applescript
# this is done to send the title of the post
var=$(./get_cats.py); osascript personal_msg_cat.scpt "$var"
