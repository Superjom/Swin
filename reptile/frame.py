# -*- coding: utf-8 -*-
import dialog


class SwinFrame:
    '''
    界面
    '''
    def __init__(self):
        self.d = dialog.Dialog(dialog="dialog")

    def handle_exit_code(self, code):
        if code in (self.d.DIALOG_CANCEL, self.d.DIALOG_CANCEL):
            if code == self.d.DIALOG_CANCEL:
                msg = "You chose cancel in the last dialog box. Do you want to " \
                      "exit Swin reptile system?"
            else:
                msg = "You pressed ESC in the last dialog box. Do you want to " \
                      "exit Swin reptile system?"
            if self.d.yesno(msg) == self.d.DIALOG_OK:
                sys.exit(0)
            return 0
        else:
            return 1                        # code is d.DIALOG_OK

    def howManyClient(self):
        '''
        选取本平台为单平台工作
        还是分布计算模式
        '''
        while True:
            (code, tag) = self.d.radiolist(
                "请选择本系统工作模式",
                width = 75,
                choices = [
                    ("单个平台模式", "只有一台服务器工作", 1),
                    ("分布式模式", "多台服务器分布式计算", 0),
                ]
            )
            if self.handle_exit_code(code) :
                break
        return tag

    def modeSelect(self):
        '''
        选择本平台为服务器or客户端
        '''
        while True:
            (code, tag) = self.d.radiolist(
                "你想要将本机器作为爬虫控制服务器还是爬取子平台工作？",
                width = 75,
                choices = [
                    ("控制主服务器", "Centre Server 作为本系统查询服务器，同一控制子平台工作.", 0),
                    ("爬取子平台", "Client Reptile，由CentreServer控制进行爬取任务.", 1),
                ]
            )

            if self.handle_exit_code(code) :
                break
        return tag
    
    def howManyClient(self):
        '''
        选取本平台为单平台工作
        还是分布计算模式
        '''
        while True:
            (code, tag) = self.d.radiolist(
                "请选择本系统工作模式",
                width = 75,
                choices = [
                    ("单个平台模式", "只有一台服务器工作", 1),
                    ("分布式模式", "多台服务器分布式计算", 0),
                ]
            )


    def modeSelect(d):
        '''
        选择本平台为服务器or客户端
        '''
        while True:
            (code, tag) = d.radiolist(
                "你想要将本机器作为爬虫控制服务器还是爬取子平台工作？",
                width = 85,
                choices = [
                    ("控制主服务器", "Centre Server 作为本系统查询服务器，同一控制子平台工作.", 0),
                    ("爬取子平台", "Client Reptile，由CentreServer控制进行爬取任务.", 1),
                ]
            )

        return tag

    def ipConfig(self):
        '''
        输入主服务器IP
        '''
        while True:
            (code, answer) = d.inputbox("请输入控制主服务器ip", init = "127.0.0.1")
            if self.handle_exit_code(code):
                break
        return answer

    def socConfig(self):
        '''
        输入端口
        '''
        while True:
            (code, answer) = d.inputbox("请输入控制主服务器端口", init = "24567")
            if self.handle_exit_code(code):
                break
        return answer




if __name__ == '__main__':
    f = SwinFrame()
    f.modeSelect()




def modeSelect(d):
    '''
    选择本平台为服务器or客户端
    '''
    while True:
        (code, tag) = d.radiolist(
            "你想要将本机器作为爬虫控制服务器还是爬取子平台工作？",
            width = 85,
            choices = [
                ("控制主服务器", "Centre Server 作为本系统查询服务器，同一控制子平台工作.", 0),
                ("爬取子平台", "Client Reptile，由CentreServer控制进行爬取任务.", 1),
            ]
        )

    return tag


if __name__ == '__main__':
    f = SwinFrame()
    f.modeSelect()


