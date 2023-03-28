import argparse
import os
import sqlite3
import csv

def get_userMessages(cursor):
    '''
    This function gets all the message conversations to & from the user.
    '''
    cursor.execute(
        '''
        SELECT
        	datetime(messages.sent_at/1000,'unixepoch') AS "Sent At",
        	datetime(messages.expirationStartTimestamp/1000, 'unixepoch') AS "Expiration Start Time",
        	datetime((json_extract(messages.json,'$.reactions[0].targetTimestamp'))/1000,'unixepoch') AS "Reaction reacted Time",
        	datetime((json_extract(messages.json,'$.reactions[0].timestamp'))/1000,'unixepoch') AS "Reaction seen Time",
        	messages.type,
        	messages.readStatus,
        	messages.seenStatus,
        	messages.source AS "Sent Mobile Number",
        	messages.body,
        	json_extract(messages.json,'$.reactions[0].emoji') AS "Emoji Reacted",
        	json_extract(messages.json,'$.reactions[0].targetAuthorUuid') AS "Target Author UUID",
        	json_extract(messages.json,'$.reactions[0].fromId') AS "Sent Author ID", 
        	CASE
        		WHEN json_extract(messages.json,'$.reactions[0].source') == 1 THEN "Incoming"
        		WHEN json_extract(messages.json,'$.reactions[0].source') == 0 THEN "Outgoing"
        		ELSE json_extract(messages.json,'$.reactions[0].source')
        	END AS "Reaction reacted direction",
        	conversationId,
        	CASE
        		WHEN messages.hasAttachments == 0 THEN "False"
        		WHEN messages.hasAttachments == 1 THEN "True"
        		ELSE messages.hasAttachments
        	END AS "HasAttachments",
        	CASE
        		WHEN messages.hasFileAttachments == 0 THEN "False"
        		WHEN messages.hasFileAttachments == 1 THEN "True"
        		ELSE messages.hasFileAttachments
        	END AS "HasFileAttachments",
        	CASE 
        		WHEN messages.hasAttachments == 1 THEN datetime((JSON_Extract(messages.json,'$.attachments[0].uploadTimestamp'))/1000,'unixepoch')
        		ELSE "No attachments" 
        	END AS "Attachment Upload Time",
        	CASE 
        		WHEN messages.hasAttachments == 1 THEN JSON_Extract(messages.json,'$.attachments[0].fileName')
        		ELSE "No attachments" 
        	END AS "Attachment Name",
        	CASE 
        		WHEN messages.hasAttachments == 1 THEN JSON_Extract(messages.json,'$.attachments[0].path')
        		ELSE "No attachments" 
        	END AS "Attachment Path",
        	CASE 
        		WHEN messages.hasAttachments == 1 THEN JSON_Extract(messages.json,'$.attachments[0].url')
        		ELSE "No attachments" 
        	END AS "Attachment Url",
        	CASE
        		WHEN messages.hasVisualMediaAttachments == 0 THEN "False"
        		WHEN messages.hasVisualMediaAttachments == 1 THEN "True"
        		ELSE messages.hasVisualMediaAttachments
        	END AS "HasVisualMediaAttachments",
        	CASE
        		WHEN messages.isErased == 0 THEN "False"
        		WHEN messages.isErased == 1 THEN "True"
        		ELSE messages.isErased
        	END AS "IsErased",
        	CASE
        		WHEN messages.isViewOnce == 0 THEN "False"
        		WHEN messages.isViewOnce == 1 THEN "True"
        		ELSE messages.isViewOnce
        	END AS "IsViewOnce",
        	messages.sourceUuid,
        	messages.sourceDevice,
        	messages.json AS "Raw Data"
        FROM
        	messages
        LEFT JOIN conversations ON conversations.id == messages.conversationId;
        '''
    )
    all_rows = cursor.fetchall()
    return all_rows, "Signal_Messages.csv"

def get_installedStickers(cursor):
    '''
    This function gets all the installed stickers packs on Signal
    '''
    cursor.execute(
        '''
        SELECT 
        	datetime(sticker_packs.createdAt/1000,'unixepoch') AS "Created on",
        	datetime(sticker_packs.installedAt/1000,'unixepoch') AS "Installed on",
        	datetime(sticker_packs.lastUsed/1000, 'unixepoch') AS "Last Used",
        	sticker_packs.title as "Sticker Title",
        	sticker_packs.stickerCount as "No of stickers",
        	sticker_packs.status as "Status",
        	sticker_packs.downloadAttempts AS "No of Download Attempts",
        	sticker_packs.attemptedStatus as "Attempted Status",
        	sticker_packs.author as "Author",
        	sticker_packs.id as "Sticker ID",
        	sticker_packs.coverStickerId as "Cover Sticker ID",
        	sticker_packs.storageID as "Storage ID",
        	CASE
        		WHEN sticker_packs.storageNeedsSync == 0 THEN "FALSE"
        		WHEN sticker_packs.storageNeedsSync == 1 THEN "True"
        		ELSE sticker_packs.storageNeedsSync
        	END AS "Storage SYNC Needed?",
        	sticker_packs.key
        FROM
        	sticker_packs;
        '''
    )
    all_rows = cursor.fetchall()
    return all_rows, "Signal_Installed_Stickers.csv"

def get_signalContacts(cursor):
    '''
    This function get all the contacts who are on Signal
    '''
    cursor.execute(
        '''
        SELECT
	        datetime(conversations.active_at/1000,'unixepoch') as "Last Active at",
	        conversations.name as "Name",
	        conversations.profileFullName as "Profile Full Name",
	        conversations.e164 as "Mobile Number",
	        conversations.type,
	        conversations.uuid as "User UUID",
	        conversations.id as "conversation Id",
	        conversations.groupId as "Group ID",
	        json_extract(json,'$.unreadCount') as "Unread Messages count",
	        json_extract(json,'$.sentMessageCount') as "Sent Messages count",
	        json_extract(json,'$.messageCount') as "Total Message count",
	        json_extract(json,'$.profileAvatar.path') as "Profile Avatar Path",
	        json_extract(json,'$.isArchived') as "Archived?",
	        json_extract(json,'$.lastMessage') as "Last Sent Message",
	        json_extract(json,'$.lastMessageStatus') as "Last Message status"
        FROM
	        conversations;
        '''
    )
    all_rows = cursor.fetchall()
    return all_rows, "Signal_Contacts.csv"

def generateCSV(results, output_folder, filename):
    '''
    Generates CSV Reports
    
    If output folder exists then proceeds in report generation,
    else creates the output folder and starts the report generation.
    If output folder argument is not set then default folder is
    created in the path script was run.
    '''

    if(os.path.exists(output_folder)):
        pass
    elif(output_folder == 'Reports'):
        print(f"[+] Output folder does not exist. Creating the '{output_folder}' folder.\n")
        os.mkdir(output_folder)
    else:
        print("[+] Output Folder doesn't exist!")

    output = os.path.join(os.path.abspath(output_folder), filename)      # Get absolute path to the file

    # Creating CSV file
    out = open(output, 'w', encoding="utf-8")
    csv_out = csv.writer(out, lineterminator='\n')

    # CSV Report headers based on filename
    if(filename == "Signal_Messages.csv"):
        csv_out.writerow(['Sent At', 'Expiration Start time', 'Reaction reacted time', 'Reaction seen time', 'type', 'Read Status', 'Seen Status', 'Sent Mobile Number', 'Sent/Received Message', 'Emoji Reacted', 'Target Author UUID', 'Sent Author UUID', 'Reaction direction', 'Conversation ID', 'Has Attachments?', 'Has File Attachments?', 'Attachment Upload Time', 'Attachment Name', 'Attachment Path', 'Attachment URL', 'Has Visual Media Attachments', 'Erased?', 'View Once?', 'Source UUID', 'Source Device', 'JSON Raw Data'])
    elif(filename == "Signal_Installed_Stickers.csv"):
        csv_out.writerow(['Created on', 'Installed on', 'Last Used', 'Sticker title', 'No of Stickers', 'Status', 'No of Download attempts', 'Attempted Status', 'Author', 'Sticker ID', 'Cover Sticker ID', 'Storage ID', 'Storage SYNC needed?', 'Key'])
    elif(filename == "Signal_Contacts.csv"):
        csv_out.writerow(['Last Active at', 'Name', 'Profile Full Name', 'Mobile Number', 'Type', 'User UUID', 'Conversation ID', 'Group ID', 'Unread Messages count', 'Sent Messages count', 'Total Messages count', 'Profile Avatar Path', 'Archived?', 'Last Sent Message', 'Last sent message status'])
    for row in results:
        csv_out.writerow(row)

    # Checking if the CSV report generated or not
    if(os.path.exists(output)):
        print(f"[+] Report Successfully generated and saved to {os.path.abspath(output)}")
    else:
        print('[+] Report generation Failed')

def SignalDesktopParser(input_db, output_folder):
    file_in = str(input_db)
    db = sqlite3.connect(file_in)
    cursor = db.cursor()

    messages,out_filenameM = get_userMessages(cursor)
    stickers, out_filenameS = get_installedStickers(cursor)
    contacts, out_filenameC = get_signalContacts(cursor)

    if(len(messages)>0):
        generateCSV(messages,output_folder,out_filenameM)
    else:
        print("[+] No messages were found!")
    
    if(len(stickers)>0):
        generateCSV(stickers,output_folder,out_filenameS)
    else:
        print("[+] No installed stickers were found!")

    if(len(contacts)>0):
        generateCSV(contacts, output_folder, out_filenameC)
    else:
        print("[+] No Signal Contacts were found!")

    db.close()

def main():
    parser = argparse.ArgumentParser(description="Signal Desktop Parser")
    parser.add_argument('-f', '--input_db', required=True, action="store", help="Path to decrypted Signal database.")
    parser.add_argument('-o', '--output_folder', required=False, action="store", help="Path to store parsed CSV files")

    args = parser.parse_args()
    in_file = args.input_file
    out_folder = args.output_folder

    # Checking if output folder is current folder or No output folder
    if (os.path.exists(in_file) and (out_folder == None or (os.path.abspath(out_folder) == os.getcwd()))):
        SignalDesktopParser(in_file, 'Reports')
    elif(os.path.exists(in_file) and os.path.exists(out_folder)):
        SignalDesktopParser(in_file, out_folder)
    elif(not (os.path.exists(out_folder))):
        print('[+] Output path does not exist.')
    else:
        print(parser.print_help())

if __name__ == '__main__':
    main()