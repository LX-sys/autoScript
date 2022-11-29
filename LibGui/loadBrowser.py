



import os
import sys
from PyQt5.QtWebEngineWidgets import QWebEngineView
from commonHead import (
    QApplication,
    QUrl,
    pyqtSignal
)

'''
    浏览器
'''

class Browser(QWebEngineView):
    contented = pyqtSignal(str)  # 发送网页源码的信号

    def __init__(self,*args,**kwargs):
        super(Browser, self).__init__(*args,**kwargs)

        self.resize(*self.desktopSize())
        # print(self.page().profile().httpUserAgent())
        # print(self.page().profile().httpCacheType())
        # print(self.page().profile().httpAcceptLanguage())

        self.myEvent()

    def get(self,url):
        self.load(QUrl(url))

    # 加载本地html
    def setLocalHtml(self,html:str):
        if os.path.isfile(html):
            with open(html,"r",encoding="utf8") as f:
                html_text = f.read()
        else:
            html_text = html

        self.setHtml(html_text)

    def load_Finish_event(self,b:bool):
        def call(x):
            self.contented.emit(x) # 发送源码

        self.page().toHtml(call)

    # 查找元素,并返回所有可见元素的熟悉
    def xpath(self,xpath_str,call):
        js ='''
function xpath(xpath_str){
    var nodes = []
    var evaluator = new XPathEvaluator();
    var result =evaluator.evaluate(xpath_str,document.documentElement,null,XPathResult.ORDERED_NODE_ITERATOR_TYPE,null);
    var node;
    if (result) {//执行失败会返回null
        while(node=result.iterateNext()) {//这个列表必须使用iterateNext方法遍历
            nodes.push(node)
        }
    }
    // 去除隐藏的
    var show_nodes = []
    for(var i=0;i<nodes.length;i++){
       var w = nodes[i].getBoundingClientRect().height
       var h = nodes[i].getBoundingClientRect().width
       if(w>0 && h>0){
            show_nodes.push(nodes[i])
       }
    }
    var res_list = []
    for(var i=0;i<show_nodes.length;i++){
        var res_dict = {};
        var obj= show_nodes[i].getBoundingClientRect()
        res_dict["tagName"] = show_nodes[i].tagName;
        if(show_nodes[i].text){
            res_dict["text"] = show_nodes[i].text;
        }else if(show_nodes[i].textContent){
            res_dict["text"] = show_nodes[i].textContent;
        }
        
        res_dict["rect"]={"x":obj.x,"y":obj.y,"w":obj.width,"h":obj.height}
        for(var j=0;j<show_nodes[i].attributes.length;j++){
            obj = show_nodes[i].attributes[j]
            res_dict[obj.name]=obj.value;
        }
        res_list.push(res_dict)

    }
    return res_list;
}
xpath('<xpath>');
        '''

        js=js.replace("<xpath>",xpath_str)

        self.runJavaScript(js,call)

    def runJavaScript(self,js:str,*args):
        self.page().runJavaScript(js,*args)

    # 获取屏幕大小
    def desktopSize(self):
        d_size = QApplication.desktop().size()
        count = QApplication.desktop().screenCount()
        return d_size.width()//count,d_size.height()

    def myEvent(self):
        # 浏览器加载完成事件
        self.loadFinished.connect(self.load_Finish_event)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    win = Browser()
    # win.get("https://www.baidu.com/")
    win.get("https://aep-pdp-control.sites.cigna.com/?utm_campaign=0265712&utm_source=search&campaign_ID=0265712&utm_medium=search&sid=0265712&PID=ps_23_19444&customtrack1=0265712&&msclkid=9b1315319682176908f676b453b1178d&gclid=9b1315319682176908f676b453b1178d&gclsrc=3p.ds")
    win.show()

    sys.exit(app.exec_())