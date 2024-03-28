from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget,QWizardPage,QVBoxLayout,QPushButton
from PyQt6.QtCore import QUrl, pyqtSlot
from PyQt6.QtWebEngineCore import QWebEngineSettings,QWebEnginePage
import os
import subprocess
import sys

class CustomPage(QWizardPage):
    def __init__(self, html_view, parent=None):
        super().__init__(parent)

        self.setTitle("Custom Page")
        self.setSubTitle("This is a custom page with an HTML view.")

        layout = QVBoxLayout(self)

        layout.addWidget(html_view)

        button = QPushButton("Next")
        button.clicked.connect(self.nextButtonClicked)
        layout.addWidget(button)

    def nextButtonClicked(self):
        # Add your custom logic for handling the "Next" button click
        # For example, you can check conditions and decide whether to allow navigation
        if self.validateNavigation():
            self.completeChanged.emit()

    def isComplete(self):
        print("is pagecomplted")
        # You can implement additional logic here to determine if the page is complete
        return True

    def validateNavigation(self):
        # Add your custom logic for validating navigation
        # For example, check conditions before allowing navigation
        return True
    
class CustomWebEnginePage(QWebEnginePage):

    def acceptNavigationRequest(self, url, navigation_type, is_main_frame):
        print(url,navigation_type,is_main_frame)
        # Implement your custom navigation logic here
        # Return True to allow navigation, or False to block it
        current_path = url.path()
        allowed = ["/","/ab/account-security/login","/nx/find-work/"]
        if current_path in allowed:
            return True
        else:
            if  "/ab/proposals/job/" in current_path:
                return True
            else:
                if  "/ab/proposals/" in current_path:
                    return True
                elif  "/nx/search/jobs/" in current_path:
                    return True
                elif  "/ab/messages/rooms/" in current_path:
                    return False
                else:
                    return False
                
    def javaScriptConsoleMessage(self, level, message, lineNumber, sourceID):
        custom_script = """
                    // Your custom JavaScript code goes here
                    var elm=document.querySelector('div[data-test="sidebar-collapsible-card"]');

                    if(elm){
                        elm.style="display:none;";
                    }

                    var pdropdown=document.querySelector(".nav-dropdown-account ul");

                    if(pdropdown){
                        document.querySelector(".nav-dropdown-account ul").remove()
                    }

                    var alists=document.querySelectorAll(".rooms-panel-items a");

                    if(alists.length>0){
                        alists.forEach((list,index)=>{
                            if(index!=0){
                                if(list.querySelector(".timestamp")){
                                    var date=list.querySelector(".timestamp").innerText;

                                    if(date){
                                        var givenDate = new Date(date);
                                        var targetDate = new Date("2024-03-17");

                                        if (givenDate < targetDate) {
                                            list.remove()
                                        }   
                                    }
                                }
                            }
                        })
                    }

                    setInterval(()=>{
                        var ccontainer=document.querySelector(".composer-container");
                        var uploadcontainer=document.querySelector(".air3-image-upload-wrapper");

                        if(ccontainer){
                            document.querySelector(".sticky-rooms-panel-header").style='pointer-events: none;'
                            document.querySelector(".header-row").style='pointer-events: none;'
                            document.querySelector(".desktop-room").style='pointer-events: none;'
                            ccontainer.style='pointer-events: none;';
                        }

                        if(uploadcontainer){
                            uploadcontainer.style='pointer-events: none;';
                        }
                    },500)
                """
        self.runJavaScript(custom_script)
        print(f"JavaScript Console Message ({level}): {message}, line {lineNumber}, source {sourceID}")
                
    def loadFinished(self, ok):
        if ok:
            print("Page has finished loading")
            
            # Access the DOM elements using JavaScript
            self.runJavaScript("document.title", lambda result: print(f"Page title: {result}"))
        
class HtmlView(QWebEngineView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tab = self.parent()
        self.tabs=[]
        

    def closeClicked(self,index):
        tab_widget = self.parent().parent()
        tab_widget.removeTab(index)

    def createWindow(self, windowType):
        if windowType == QWebEnginePage.WebWindowType.WebBrowserTab:
            webView = HtmlView(self.tab)
            webView.setPage(CustomWebEnginePage(self.tab));
            ix = self.tab.addTab(webView, "Upwork")
            self.tab.tabCloseRequested.connect(self.closeClicked)
            self.tab.setTabsClosable(True)
            self.tabs.append(ix)
            print("tabs",self.tabs)
            
            self.tab.setCurrentIndex(ix)
            
            return webView
        return super().createWindow(windowType)

class TabWidget(QTabWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        url = QUrl("https://www.upwork.com")
        view = HtmlView(self)
        print("view",view.setPage)
        view.setPage(CustomWebEnginePage(self));
        
        view.load(url)
        
        ix = self.addTab(view, "Upwork")

def find_qtwebengineprocess():
    # Try to find QtWebEngineProcess using the find command
    try:
        result = subprocess.check_output("find / -name QtWebEngineProcess 2>/dev/null", shell=True)
        paths = result.decode().strip().split('\n')
        if paths:
            return paths[0]
    except subprocess.CalledProcessError:
        pass

    return None

def set_qtwebengineprocess_path():
    # Find the path to QtWebEngineProcess
    qtwebengineprocess_path = "/System/Volumes/Data/Users/ravi/browser/myenv/lib/python3.11/site-packages/PyQt6/Qt6/lib/QtWebEngineCore.framework/Helpers/QtWebEngineProcess.app/Contents/MacOS/QtWebEngineProcess"

    # Set the QTWEBENGINEPROCESS_PATH environment variable
    os.environ['QTWEBENGINEPROCESS_PATH'] = qtwebengineprocess_path
    print(f"QTWEBENGINEPROCESS_PATH set to: {qtwebengineprocess_path}")

def set_qtwebengineprocess_resource():
    # Find the path to QtWebEngineProcess
    qtwebengineprocess_path = "/System/Volumes/Data/Users/ravi/browser/myenv/lib/python3.11/site-packages/PyQt6/Qt6/lib/QtWebEngineCore.framework/Resources"

    # Set the QTWEBENGINEPROCESS_PATH environment variable
    os.environ['QTWEBENGINE_RESOURCES_PATH'] = qtwebengineprocess_path
    print(f"QTWEBENGINE_RESOURCES_PATH set to: {qtwebengineprocess_path}")

def set_qtwebengineprocess_locale():
    # Find the path to QtWebEngineProcess
    qtwebengineprocess_path = "/System/Volumes/Data/Users/ravi/browser/myenv/lib/python3.11/site-packages/PyQt6/Qt6/lib/QtWebEngineCore.framework/Resources/qtwebengine_locales"

    # Set the QTWEBENGINEPROCESS_PATH environment variable
    os.environ['QTWEBENGINE_LOCALES_PATH'] = qtwebengineprocess_path
    print(f"QTWEBENGINE_LOCALES_PATH set to: {qtwebengineprocess_path}")
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = TabWidget()
    main.show()
    sys.exit(app.exec())
