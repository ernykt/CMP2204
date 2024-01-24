# CMP2204
P2P file sharing application

We divide image to 5 equal sized chunks.

You may need to specify the local adress of the file(s) you want to share in the uploader code which the name goes as CHUNKS_DIRECTORY.
One can open the chunk_announcer.py (use CMD in windows) and type in the file_name.png (extension is a must) they want to share.
One can open the chunk_discovery.py (use CMD in windows) and check which file comes from where.
One can open the chunk_downloader.py (use CMD in windows) and specify the file they want to download (without the extensions just the file name).
Every peer needs to open their own chunk_uploader.py (use CMD in windows) and needs to modify the code for their own IP adress.
One can check out the content_dictionary.txt for file names and where they come from.
One can check the log.txt files to see what is happening for uploading, downloading.

!!! THE PROGRAM ONLY DOWNLOADS AND UPLOADS PNG FILES DO NOT FORGET TO CHANGE THE CHUNK_DIRECTORY AND IP ADRESS FROM THE UPLOADER.PY !!!

The code tests were done with logmein Hamachi.
