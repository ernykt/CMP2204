import socket
import json
import os
import math
import datetime

def update_available_chunks(user_input):
    data_filename = "content_dictionary.txt"

    with open(data_filename, 'r+') as f:
        cont_json = f.read()
        extnd = [user_input + "_1", user_input + "_2", user_input + "_3", user_input + "_4", user_input + "_5"]
        cont = json.loads(cont_json)

        if 'chunks' not in cont:
            cont['chunks'] = []

        extnd_set = set(extnd)
        cont_set = set(cont['chunks'])

        if extnd_set.issubset(cont_set):
            print(f"Chunks for {user_input} are already available")
            f.seek(0)
        else:
            cont['chunks'].extend(extnd)
            f.seek(0)
            cont_json = json.dumps(cont)
            f.write(cont_json)

while True:
    user_input = input("What content do you want to download: ")

    print("------------------------------------------------------------")

    data = {"requested_content": user_input}

    filename = 'content_dictionary.txt'
    file_log = 'Download_Log.txt'

    downloaded = 0
    Flag = True
    Flag_Success = False
    Flag_Key_Error = False
    itr = 1

    while itr <= 5:
        downloaded = 0
        Flag_Success = 0
        with open(filename, 'r+') as fl:
            ips_json = fl.read()
            ips = json.loads(ips_json)
            indx = "{}{}{}".format(user_input, "_", itr)
            try:
                for ip in ips[indx]:
                    try:
                        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                            s.connect((ip, 5000))
                            req_content = "{}{}{}".format(user_input, "_", itr)
                            print(f"Requesting : {req_content}")
                            data['requested_content'] = req_content
                            json_data = json.dumps(data)
                            s.send(bytes(json_data, 'utf-8'))
                            while True:
                                chunk_recv = s.recv(262144)
                                print(f"Received chunk {req_content}")
                                print("------------------------------------------------------------")
                                timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                                with open(file_log, 'a') as log_file:
                                    log_data = "{} | {} | {} | {}".format(timestamp, req_content, ip, datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
                                    log_file.write(log_data)
                                    log_file.write("\n")

                                with open(req_content + '_recv', 'wb+') as chunk_file:
                                    chunk_file.write(chunk_recv)
                                    downloaded = 1
                                    itr += 1
                                    Flag_Success = True
                                    break
                    except TimeoutError:
                        print(f"No response from {ip}")
                        print(f"Cannot download chunk {req_content} from peer {ip}")
                        print(f"Trying other peers...")
                        print("------------------------------------------------------------")
                        downloaded = 0
                    except ConnectionRefusedError:
                        print(f"Connection refused by {ip}, try opening Chunk_Uploader in {ip}")
                        print(f"Cannot download chunk {req_content} from peer {ip}")
                        print(f"Trying other peers...")
                        print("------------------------------------------------------------")
                        downloaded = 0

                    if Flag_Success == True:
                        break

                    if ip == ips[indx][len(ips[indx]) - 1] and downloaded == 0:
                        Flag = False
                        print(f"CHUNK {req_content} CANNOT BE DOWNLOADED FROM ONLINE PEERS.")
                        break
            except KeyError:
                print(f"Content {user_input} is not available in peers")
                print("------------------------------------------------------------")
                Flag_Key_Error = True
                break
        if Flag == False:
            break

    if Flag == True and Flag_Key_Error == False:
        update_available_chunks(user_input)

        # STITCH IMAGE BACK TOGETHER
        content_name = user_input
        result_filename = content_name + "_result.png"

        with open(result_filename, 'wb') as outfile:
            for chunk_num in range(1, 6):
                chunk_filename = f"{content_name}_{chunk_num}_recv"
                with open(chunk_filename, 'rb') as infile:
                    outfile.write(infile.read())
