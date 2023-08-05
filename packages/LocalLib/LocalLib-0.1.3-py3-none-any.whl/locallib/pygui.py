from win10toast import ToastNotifier
import platform

class PlatformError(Exception):
    pass

def Notification(title, msg, dur, threaded=None):
    if platform.system() + " " + platform.release() == "Windows 10":
        if threaded == None:
            toaster = ToastNotifier()
            toaster.show_toast(title, msg, icon_path=None, duration=dur)
        elif threaded == True:            
            toaster = ToastNotifier()
            toaster.show_toast(title, msg, icon_path=None, duration=dur, threaded=True)
        elif threaded == False:
            toaster = ToastNotifier()
            toaster.show_toast(title, msg, icon_path=None, duration=dur, threaded=False)  
    else:
        raise PlatformError("This function cannot be run on your platform.")
