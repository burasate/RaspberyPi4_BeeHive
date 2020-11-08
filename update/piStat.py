import os

def getFreeSpaceStat(*_):
    st = os.statvfs('/')
    # free blocks available * fragment size
    bytes_avail = (st.f_bavail * st.f_frsize)
    gigabytes = bytes_avail / 1024 / 1024 / 1024
    return (round(gigabytes,2))

def getCPUTemp(*_):
    def measure_temp():
        temp = os.popen('vcgencmd measure_temp').readline()
        temp = temp.replace('temp=','')
        temp = temp.replace('\'C','')
        try:
            return float(temp)
        except:
            return (temp)