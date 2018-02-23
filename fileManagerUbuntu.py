import os.path
import sys
import os, re
import hashlib
sys.path.append('printResult\prettytable-0.7.2')
from prettytable import PrettyTable
from os.path import join, getsize
from collections import defaultdict
from collections import Counter
from shutil import copyfile
from shutil import move
clear = lambda: os.system('cls')
fileNameSize = defaultdict(list)
global scaned
scaned = 0

global rollback
rollback = []
global logHistory
logHistory = []
######################################################################
def scanAll():
    try:
        print(r"SCANING SYSTEM...")
        for root, dirs, files in os.walk(r"C:\Users"):
            if "AppData" in root:
                continue
            try:
                for fi in files:
                    fileNameSize[join(root, fi)] = getsize(join(root, fi))
            except Exception as e:
                print (e)

        drives = re.findall(r"[A-Z]+:.*$",os.popen("mountvol /").read(),re.MULTILINE)
        for drive in drives:
            if "C" not in drive:
                 for root, dirs, files in os.walk(drive):
                     try:
                         for fi in files:
                             fileNameSize[join(root, fi)] = getsize(join(root, fi))
                     except Exception as e:
                         print (e)
        global scaned
        scaned = 1
    except Exception as e:
        print(e)
#####################################################################


######################################################################
def largestFiles(largeORsmall):
    global scaned
    if scaned == 0:
        scanAll()
    result = PrettyTable(["Sno","FileName","SystemDrive","FileLocation","FileSize"])
    fileSize = Counter(fileNameSize)

    if largeORsmall == 1:
        num = input("Enter How Many Files You Want To View: ")
        try:
            num = int(num)
        except:
            sys.exit("Enter Number Only")
        fileList =  fileSize.most_common(num)
    elif largeORsmall == 2:
        num = input("Enter How Many Files You Want To View: ")
        try:
            num = int(num)
        except:
            sys.exit("Enter Number Only")
        fileList =  fileSize.most_common()[:-(num+1):-1]

    sno=1
    for k,v in fileList:#fileSize.most_common(num)[:-10:-1]:
        fileName = k.rsplit("\\",1)
        if v < 1024:
            v = str(v) + "B"
        elif v < (1024**2):
            v = str(format(v/1024, '.2f')) + "KB"
        elif v < (1024**3):
            v = str(format((v/(1024**2)), '.2f')) + "MB"
        elif v < (1024**4):
            v = str(format((v/(1024**3)), '.2f')) + "GB"
        driveName = fileName[0][0] + " Drive"
        if "C" in driveName:
            fileName[0] = '\\'.join(fileName[0].split("\\")[3:])
        else:
            fileName[0] = '\\'.join(fileName[0].split("\\")[1:])
        if len(fileName[1]) > 20:
            fileName[1] = fileName[1][0:20].rstrip()+ ".."
        result.add_row([sno,fileName[1],driveName,fileName[0],v])
        sno = sno+1
    result.align = "r"
    print (result)
    global logHistory
    with open("desktopCleaner.log", "a") as myfile:
        if largeORsmall == 1:
            myfile.write("\nLARGEST FILES ON SYSTEM\n")
            logHistory.append("\nLARGEST  FILES ON SYSTEM\n")
        else:
            myfile.write("\nSMALLEST  FILES ON SYSTEM\n")
            logHistory.append("\nSMALLEST  FILES ON SYSTEM\n")
        myfile.write(str(result))
        myfile.close()

        rollback.append(str(result))

######################################################################






######################################################################
def cleanDesktop(fileExtensions):

        clear = lambda: os.system('cls')
        directory =  os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents\\Desktop Files')
        # print(directory)
        if not os.path.exists(directory):
            os.makedirs(directory)


        # desktopFiles = defaultdict(list)
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        # print (desktop)
        shortcutExt = ["ini","lnk","db"]
        # extensions = []
        global rollback
        rowCount =0
        result = PrettyTable(["FileName","ActualPath",r"NewPath(Documents\DesktopFiles\)"])
        for root, dirs, files in os.walk(desktop):
            try:
                for fi in files:
                    # desktopFiles[join(root, fi)] = join(root, fi).split(".")[-1]
                    if "." not in fi:
                        ext = "noExt"
                    else:
                        ext = join(root, fi).split(".")[-1][0:15]
                        print(ext)
                    locOld = '\\'.join(root.split("\\")[3:])

                    #handled shortcut and hidden autosaved files
                    if ext not in shortcutExt and "~$" not in fi[0:3]:
                        # extensions.append(ext)
                        newFolder = ""
                        for key in fileExtensions:
                            if ext in fileExtensions[key]:
                                newFolder =  os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents\\Desktop Files\\'+key)
                                if not os.path.exists(newFolder):
                                    os.makedirs(newFolder)
                                move(join(root, fi),join(newFolder,fi))
                                rollback.append([join(newFolder,fi),join(root, fi)])
                                locNew = '\\'.join(newFolder.split("\\")[5:])
                                result.add_row([fi,locOld,locNew])
                                rowCount = rowCount + 1
            except Exception as e:
                print (e)
        if rowCount == 0:
            clear()
            print("\n\t\t\t\tFILE MANAGER\n")
            print("Desktop Already Cleaned\n")
            return 0
        result.align = "r"
        global logHistory
        with open("desktopCleaner.log", "a") as myfile:
            myfile.write("\nDESKTOP MOVES\n")
            myfile.write(str(result))
            myfile.close()
            logHistory.append("DESKTOP MOVES\n")
            logHistory.append(str(result))
        clear()
        print("\n\t\t\t\tFILE MANAGER\n")
        print (result)

        return 1
######################################################################


######################################################################
def cleanDownloads(fileExtensions):
    clear = lambda: os.system('cls')
    directory =  os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents\\Desktop Files')
    # print(directory)
    if not os.path.exists(directory):
        os.makedirs(directory)


    # desktopFiles = defaultdict(list)
    Downloads = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads')
    # print (Downloads)
    shortcutExt = ["ini","lnk","db"]
    global rollback
    rowCount =0
    result = PrettyTable(["FileName","ActualPath",r"NewPath(Documents\DownloadsFile\)"])
    for root, dirs, files in os.walk(Downloads):
        try:
            for fi in files:
                # desktopFiles[join(root, fi)] = join(root, fi).split(".")[-1]
                if "." not in fi:
                    ext = "noExt"
                else:
                    ext = join(root, fi).split(".")[-1][0:15]
                locOld = '\\'.join(root.split("\\")[3:])
                # print (ext)
                #handled shortcut and hidden autosaved files
                if ext not in shortcutExt and "~$" not in fi[0:3]:
                    # extensions.append(ext)
                    newFolder = ""
                    for key in fileExtensions:
                        if ext in fileExtensions[key]:
                            newFolder =  os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents\\Downloads File\\'+key)
                            if not os.path.exists(newFolder):
                                os.makedirs(newFolder)
                            move(join(root, fi),join(newFolder,fi))
                            rollback.append([join(newFolder,fi),join(root, fi)])
                            locNew = '\\'.join(newFolder.split("\\")[5:])
                            result.add_row([fi,locOld,locNew])
                            rowCount = rowCount + 1
                            print(rowCount)
        except Exception as e:
            print (e)
    if rowCount == 0:
        clear()
        print("\n\t\t\t\tFILE MANAGER\n")
        print("Downloads Already Cleaned\n")
        return 0
    result.align = "r"
    clear()
    print("\n\t\t\t\tFILE MANAGER\n")
    print (result)
    global logHistory
    with open("desktopCleaner.log", "a") as myfile:
        myfile.write("\nDOWNLOADS MOVES\n")
        myfile.write(str(result))
        myfile.close()
        logHistory.append("DOWNLOADS FOLDER MOVES\n")
        logHistory.append(str(result))
    return 1
######################################################################


######################################################################
def docOrDeskClean():
    clear = lambda: os.system('cls')
    clear()
    print("\n\t\t\t\tFILE MANAGER\n")
    flagPreviousAction = 0
    while(1):
        print("CLEAN DESKTOP OR DOWNLOADS")
        print("Press 1. TO CLEAN DESKTOP")
        print("Press 2. TO CLEAN DOWNLOAD FOLDER")
        print("Press 3. TO GO BACK")
        print("Press 4. TO EXIT")
        if flagPreviousAction:
            print("Press 5. TO REDO PREVIOUS ACTIONS")
        num = input()
        try:
            num = int(num)
        except:
            print("Enter Number Only")
            continue

        fileExtensions = {}
        fileExtensions["Music"] = ["mp3","wav","aiff","aac","ogg","wma"]
        fileExtensions["Video"] = ["avi","flv","mov","mpg","wmv","mkv","srt","3gp","mp4"]
        fileExtensions["Images"] = ["bmp","gif","jpg","png","jpeg",".psd"]
        fileExtensions["TextFiles"]  = ["doc","rtf","txt","docx"]
        fileExtensions["DataFiles"] = ["pdf","csv","ppt","pptx","xlr","xls"]
        fileExtensions["Compressed"] = ["tar","zip","gz","rar","7z"]
        fileExtensions["WebFiles"] = ["asp","css","htm","html","js","jsp","php","xhtml","xml"]
        fileExtensions["DevelopmentFiles"] = ["c","class","cpp","cs","java","py","sh","vb"]
        fileExtensions["Softwares"] = ["exe"]


        if num == 1:
            flagPreviousAction = cleanDesktop(fileExtensions)
        elif num == 2:
            flagPreviousAction = cleanDownloads(fileExtensions)
        elif num == 3:
            return
        elif num == 4:
            clear()
            sys.exit()
        elif num ==5 and flagPreviousAction:
            for loc in rollback:
                move(loc[0],loc[1])
            flagPreviousAction = 0
            # print(rollback)
            global logHistory
            logHistory.append("\nROLLED BACK PREVIOUS MOVES")
            with open("desktopCleaner.log", "a") as myfile:
                myfile.write("\nROLLED BACK PREVIOUS MOVES\n")
                myfile.close()

            del rollback[:]
            # print(rollback)
            clear()
            print("\n\t\t\t\tFILE MANAGER\n")
            print("All Prevous Moves Rolled Back\n")
        else:
            print ("Enter Valid Choice")
######################################################################



##########################################################################
def chunk_reader(fobj, chunk_size=8096):
    """Generator that reads a file in chunks of bytes"""
    while True:
        chunk = fobj.read(chunk_size)
        if not chunk:
            return
        yield chunk



def viewDuplicates(hash=hashlib.sha1):
    clear = lambda: os.system('cls')
    clear()
    print(" ")
    print("\n\t\t\t\tFILE MANAGER\n")
    print("ALERT: TO AVOID LONG RUN ONLY \"Desktop,Downloads,Music and Pictures\" FOLDERS WILL BE CHECKED")
    print(" ")
    paths = []
    paths.append(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))
    paths.append(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Downloads'))
    # paths.append(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents'))
    paths.append(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Music'))
    paths.append(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Pictures'))
    # paths.append(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Videos'))
    hashes = {}
    results = []
    Sno = 1
    for path in paths:
        for dirpath, dirnames, filenames in os.walk(path):
            if "." not in dirpath:
                for filename in filenames:
                    try:
                        full_path = os.path.join(dirpath, filename)
                        hashobj = hash()
                        for chunk in chunk_reader(open(full_path, 'rb')):
                            hashobj.update(chunk)
                        file_id = (hashobj.digest(), os.path.getsize(full_path))
                        duplicate = hashes.get(file_id, None)
                        if duplicate:
                            results.append([Sno,full_path,duplicate])
                            Sno = Sno + 1
                            # print ("Duplicate found: %s and %s" % (full_path, duplicate))
                        else:
                            hashes[file_id] = full_path
                    except:
                        continue
    if len(results) == 0:
        print("No Duplicate Found :)")
    else:
        result = PrettyTable(["Sno","(Same File)First Location","(Same File)Second Location"])
        result.align = "r"
        # print (results)
        for row in results:
            result.add_row(row)

        print(result)
        print("ENTER FILENO(Sno) TO DELETE ANY DUPLICATE FILE")
        print("PRESS 0 TO GO BACK")
        try:
            num = int(input())
            if num > len(results):
                print("ENTER CORRECT NUMBER")
        except:
            print("ENTER NUMBER ONLY")
        if num==0:
            print(" ")
            return
        # print(results[num-1][1])
        print("PRESS 1 TO CONFIRM DELETE(PERMANENT)")
        print("PRESS 2 TO CANCEL AND MOVE BACK")
        if int(input())==1:
            os.remove(results[num-1][1])
            result = result.del_row(num-1)
            print("FILE REMOVED")
            return 1
        else:
            print(" ")
            return 0
##########################################################################



################################################################################


if __name__ == "__main__":
    try:
        if not os.path.exists('desktopCleaner.log'):
            open('desktopCleaner.log', 'w').close()
        flagInvalid = 0
        flagNumOnly = 0
        flagOffClear = 0
        flagShowBanner = 0
        actionLogFlag = 0
        while(1):
            if not flagOffClear:
                clear()
                flagOffClear = 0
            if not flagShowBanner:
                print("\n\t\t\t\tFILE MANAGER\n")
            print("Press 1. TO VIEW LARGEST FILES OF SYSTEM")
            print("Press 2. TO VIEW SMALLEST FILES OF SYSTEM")
            print("Press 3. TO CLEAN DESKTOP OR DOWNLOAD FOLDER")
            print("Press 4. TO VIEW AND DELETE DUPLICATE FILES")
            print("Press 5. TO VIEW ACTION LOG")
            print("Press 6. TO EXIT")
            if flagInvalid:
                print("Invalid Choice Choose Again")
                flagInvalid = 0

            if flagNumOnly:
                print("Enter Number Only")
                flagNumOnly = 0
            num = input()
            try:
                num = int(num)
            except:
                flagNumOnly = 1
                continue
            if num == 1:
                largestFiles(num)
                flagOffClear = 1
                flagShowBanner = 1
                actionLogFlag =1
            elif num == 2:
                largestFiles(num)
                flagOffClear = 1
                flagShowBanner = 1
                actionLogFlag =1
            elif num ==3:
                docOrDeskClean()
                flagOffClear = 0
                flagShowBanner = 0
                actionLogFlag =1
            elif num == 4:
                flagOffClear = 1
                flagOffClear = viewDuplicates()
                actionLogFlag =1
            elif num==5:
                clear()
                print("\n\t\t\t\tFILE MANAGER\n")
                print("LOG HISTORY\n")
                if actionLogFlag:
                    for log in logHistory:
                        print(log)
                else:
                    print("NOTHING IN LOG HISTORY")
                flagOffClear = 1
            elif num ==6:
                clear()
                sys.exit()
            else:
                flagInvalid = 1
    except Exception as e:
        print(e)
        sys.exit(e)
