from Log import Log

Log.print("Here's a print")
Log.debug("Here's a debug")
Log.error("Here's an error")
Log.section_header("Here's a section header")


#You can also use this bot to write lines directly to a file using
Log.write_to_file("Here's an example of writing directly to the log file, and using csv formatting... in case you want to skip the output to console", filename="prompts.log", type=",")