from burp import IBurpExtender
from burp import IContextMenuFactory
from javax.swing import JMenuItem
from javax.swing import JFileChooser
import java.util.ArrayList as ArrayList


class BurpExtender(IBurpExtender, IContextMenuFactory):
    # Registers the extension in Burp
    def registerExtenderCallbacks(self, callbacks):
        self._ctxMenuInvocation = None
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Save response body")
        callbacks.registerContextMenuFactory(self)
        print('[+] Extension registered')
        return

    # Registers the menu item in the context menu
    def createMenuItems(self, ctxMenuInvocation):
        self._ctxMenuInvocation = ctxMenuInvocation
        menuItems = ArrayList()
        menuItems.add(JMenuItem("Save response body",
                                actionPerformed=self.saveResponseBody))
        return menuItems

    # Defines the method for the 'Save response body' context menu
    def saveResponseBody(self, event):
        messages = self._ctxMenuInvocation.getSelectedMessages()
        for message in messages:
            response = message.getResponse()
            body_offset = self._helpers.analyzeResponse(
                response).getBodyOffset()
            # Create a JFileChooser object, to be able to show a save dialog
            jfc = JFileChooser()
            if (jfc.showOpenDialog(None) == JFileChooser.APPROVE_OPTION):
                path = jfc.getSelectedFile().getAbsolutePath()
                print('[+] Opening {0} for writing'.format(path))
                f = open(path, 'wb')
                f.write(response.tostring()[body_offset:])
                f.close()
        return
