import servicemanager
import win32serviceutil
import win32service
import win32event
import winerror
import os, sys, time
class tornado_wsserver(win32serviceutil.ServiceFramework):
    _svc_name_ = "tornado_wsserver"   #  服务名
    _svc_display_name_ = "tornado_wsserver "   # 服务在windows系统中显示的名称
    _svc_description_ = "tornado_wsserver"   #服务的描述
    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.License = self._LicenseExist()
        self.run = True
    def _LicenseExist(self):
        is_exist=os.path.exists(r'D:\daimaku\IACS\dist\tornado_wsserver')
        string_key='d8838bccad0c19e847b9e73f4432b951b6f035fd8c19f5474e30db5a0e4fa4c99b57c01af79161850b95d3f99a6b0b6074f18224ec7c44f28bc243be06f8f2b96e370f5ca724c01f1bd0e289afdd9eeef7e33d42a5113ddd4818a47b33449487baec2099a50d5e3dde32bdf66d979982a68d0d60a1200990ebf8a4827b7db3d1e83f9ad9d9946267fe830c48bbe025a5ebb99b85c7f1cf93de2beb22c8e9766e5ef526242b01f5251d8a768780026add2d2d8fb9ffccb86f8779221b01d206e586d96b83839b30006910a4bca6438fb5d5b2900431f8ecab50a9f18d0e7e8abec7b212fdc9ab667f08dd3eef14ecbdb24910466f45be92d0a085ff81d7362b828847c29be579942b63b9eb26b2441b5ef20f5a012431d263ded3f5fe434111b833612464bf4df18ae06c536b6895d240387774c3b438d5f0745c7a0d3ce963e82fc8df603f6fa526e8bd1fc51e2509e0840f3bbbde7bc3fec9e837b5aa744a9ae4449c974e26d787e475f73dbc3ee9c73cc258f38b79c413453fd4fe732bed57ba9d0312d2bcaf333a5c82d92a269a7ccaf27273a178feb95028f8f0805675a6199abbd8b47756b4543269a35025438794cd32410ac19c77526c4b94b93d091069056df1dda0f49298d753a317850c7104f94067ac9cc4d5b3d377f10627d21c12a4c066347eb05370fbe9e0658c1ec1803d43ed71509f5cdb25d60f505ef7527c405d3ea05bb381436dd3622484a1ff7263e4d93f275493332af3f77d28a13a0fa0eb810b7d25a378f6b8313ab3bcb44131ca3500670b0321aa95b077cef85d348e13315c2d2d42795e41569162986755709d099b59ee320e6caf422497234251d07d697bb3f3e5ad6d15d80fd85da016e7075bf84522aa6339e8b66ecd4b71d02fd01f4f57a0147ceaddbf9e5f32e7ec60ae35ff73d2f386d9d0133cb697731773b55fc2615c584e9f4013253d3fc53fa13a9e982a2493e1145861759c30cf9064d333bb184e378b52e7dd8bbbd0c17774549fabb44014dab2e0a903c53d0da1c9d3a223c69f3b9bcc7925ba21a464fc9fa43e20574ffedb7a27f2cd7ae7b6b46c5cb4e0b176ece7d59ff199b74b3436ead185df5c79d74b35d644bb02315130131772db21fcd1d535014b10c4cbbb8e1f847cd00be52992ab94a7b5a7b1c27d87abe3fc605972ceb3463a07924c816a04642adcabbc7b18a40a24a3af217d0390c1102cb5b4573b1816c76667f50d33631a97e986255644e8e0c26d63cd1f29f501ff51673509822c1bf8158ceee752024dcbe0e24941803ebd8afc0bded3598012ba5431060f0db7fad7fd4960972da9a6cfaa0850c43470498236ef7b22fbf79d491e054cf142815e6c04e573a52e22ccaa2d406167c6442db40456cd93752349b2968132388b51edbe13aa349abc34696453d1a4b39f8311284f8afbae'
        if is_exist:
            for line in open(r"D:\daimaku\IACS\dist\tornado_wsserver"):
                if line!=string_key:
                    self.writer(string_key)
        else:
            self.writer(string_key)
    # 写入License
    def writer(self, string_key):
        f=open(r'D:\daimaku\IACS\dist\tornado_wsserver','w')
        f.write(string_key)
        f.close()
    def SvcDoRun(self):
        while self.run:
            import os
            main = r'D:\daimaku\IACS\dist\tornado_wsserver.exe'
            f = os.popen(main)
            data = f.readlines()
            f.close()
    def SvcStop(self):
        # 服务已经停止
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.run = False
if __name__=='__main__':
    if len(sys.argv) == 1:
        try:
            evtsrc_dll = os.path.abspath(servicemanager.__file__)
            servicemanager.PrepareToHostSingle(tornado_wsserver)
            servicemanager.Initialize('tornado_wsserver', evtsrc_dll)
            servicemanager.StartServiceCtrlDispatcher()
        except win32service.error as details:
            print(details)
            if details == winerror.ERROR_FAILED_SERVICE_CONTROLLER_CONNECT:
                win32serviceutil.usage()
    else:
        win32serviceutil.HandleCommandLine(tornado_wsserver)
