import os,win32con,json,math
import win32utils
from utils.config import globalconfig ,magpie10_config
from utils.hwnd import  letfullscreen,recoverwindow,ListProcess
from traceback import print_exc
from utils.subproc import subproc_w
import time,threading

class fullscreen():
    def __init__(self,_externalfsend) -> None: 
        self.savewindowstatus=None 
        self._externalfsend=_externalfsend
        if self.fsmethod==1:self.runmagpie10() 
    @property
    def fsmethod(self):return globalconfig['fullscreenmethod_2']
    def runmagpie10(self):
        exes=[_[1] for _ in ListProcess()]  
        if os.path.join(globalconfig['magpie10path'],'Magpie.exe').replace('/','\\') not in exes: 
            subproc_w(os.path.join(globalconfig['magpie10path'],'Magpie.exe'),cwd=globalconfig['magpie10path'] ,name='magpie10' ) 
     
    def _1(self,hwnd,full):
        self.runmagpie10()  
        win32utils.SetForegroundWindow(hwnd )   
        time.sleep(0.1)
        configpath=os.path.join(globalconfig['magpie10path'],'config/config.json')
        if os.path.exists(configpath)==False:
            configpath=os.path.join(os.environ['LOCALAPPDATA'],'Magpie/config/config.json')
        if os.path.exists(configpath)==False:
            return 
        with open(configpath,'r',encoding='utf8') as ff:
            config=json.load(ff)
        shortcuts=config['shortcuts']['scale']
        mp1={'SHIFT': 16, 'WIN': 91,'CTRL': 17,'ALT': 18}
        mp={
            0x100:'WIN',
            0x200:'CTRL',
            0x400:'ALT',
            0x800:'SHIFT'
        }
        
        
        for k in mp:
            if shortcuts&k !=0:
                win32utils.keybd_event(mp1[mp[k]],0,0,0)
        
        k2=shortcuts &0xff
        win32utils.keybd_event(k2,0,0,0)      
        win32utils.keybd_event(k2, 0, win32con.KEYEVENTF_KEYUP, 0)
        for k in mp:
            if shortcuts&k !=0:
                win32utils.keybd_event(mp1[mp[k]],0,win32con.KEYEVENTF_KEYUP,0)
        
    def _0(self,hwnd,full):
        if full:  
            profiles_index=globalconfig['profiles_index']
            if profiles_index>len(magpie10_config['profiles']):
                profiles_index=0
                
            jspath=os.path.abspath('./userconfig/magpie10_config.json')
            with open(jspath,'w',encoding='utf-8') as ff:
                    ff.write(json.dumps(magpie10_config,ensure_ascii=False,sort_keys=False, indent=4))
            self.engine= subproc_w(f'./files/plugins/Magpie10/Magpie.Core.exe {profiles_index} {hwnd} "{jspath}"',cwd='./files/plugins/Magpie10/')
            def _waitexternalend():
                self.engine.wait()
                self._externalfsend()
            threading.Thread(target=_waitexternalend ).start()
        else:
            endevent = win32utils.CreateEvent(False, False,'MAGPIE_WAITFOR_STOP_SIGNAL')
            win32utils.SetEvent(endevent)
            win32utils.CloseHandle(endevent)
             
    # magpie9
    # def _0(self,hwnd,full):
    #     if full:
    #         win32utils.SetForegroundWindow(hwnd )    
    #         callmagpie(('./files/plugins/Magpie_v0.9.1'),hwnd,globalconfig['magpiescalemethod'],globalconfig['magpieflags'],globalconfig['magpiecapturemethod'])
    #     else:
    #         hwnd=win32utils.FindWindow('Window_Magpie_967EB565-6F73-4E94-AE53-00CC42592A22',None) 
    #         if hwnd==0:
    #             return
    #         WM_DESTORYHOST=win32utils.RegisterWindowMessage( "MAGPIE_WM_DESTORYHOST") 
    #         win32utils.SendMessage(hwnd, WM_DESTORYHOST)
    def _2(self,hwnd,full):
        win32utils.SetForegroundWindow(hwnd )   
        win32utils.keybd_event(18,0,0,0)     # alt
        win32utils.keybd_event(13,0,0,0)     # enter
                            
        win32utils.keybd_event(13, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32utils.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)
    def _3(self,hwnd,full):
        if full: 
            self.savewindowstatus=letfullscreen(hwnd)
        else:
            recoverwindow(hwnd,self.savewindowstatus)
    def __call__(self, hwnd=0,full=False):  
        try: 
            [
                self._0,
                self._1,
                self._2,
                self._3
            ][self.fsmethod](hwnd,full) 
        except:
            print_exc()