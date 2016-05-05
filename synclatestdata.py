'''
Created on 5 Mei 2016

@author: ewien
'''

import sys
sys.path.append("zklib")

import zklib
import time
import zkconst
import syncAttendance
import datetime
import logging

ip = "192.168.20.9"
port = 4370
logFile = "synclog.txt"

zk = zklib.ZKLib(ip, port)

logging.basicConfig(filename=logFile,level=logging.DEBUG)

ret = zk.connect()
print "Pesan Koneksi:", ret
timeStart = datetime.datetime.now()
logging.info(" Inisiasi koneksi pada: "+ str(timeStart))

if ret == True:
    logging.info(" Koneksi berhasil")
    print "Pesan Disable Device", zk.disableDevice()
    
    data_user = zk.getUser()
    logging.info (" Jumlah user pada mesin: %s" % (len(data_user)))
    
    attendance = zk.getAttendance()
    logging.info (" Jumlah data kehadiran pada mesin: %s" % (len(attendance)))
    
    if ( attendance ):
        i = syncAttendance.Synchronizer()
        cnt = 1
        
        for lattendance in attendance:
            i.insert(lattendance)
        
        logging.info(" Sync sukses, " + str(i.databaru) +" data baru berhasil disinkronisasi ke database")
       
    print "Pesan Enable Device", zk.enableDevice()
    
    timeEnd = datetime.datetime.now()
    connectDuration = timeEnd - timeStart
    logging.info(" Durasi koneksi "+ str(connectDuration))
    print "Pesan Disconnect:", zk.disconnect()

else:
     logging.info(" Koneksi gagal")
     
logging.info("_____________________END________________________")