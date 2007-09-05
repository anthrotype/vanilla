from AppKit import *
from nsSubclasses import getNSSubclass
from vanillaBase import VanillaBaseObject, VanillaCallbackWrapper


class _VanillaTextEditorDelegate(NSObject):
    
    def textDidChange_(self, notification):
        if hasattr(self, '_target'):
            textView = notification.object()
            self._target.action_(textView)


class TextEditor(VanillaBaseObject):
    
    """
    Standard long text entry control.
    
    pre.
    from vanilla import *
     
    class TextEditorDemo(object):
            
        def __init__(self):
            self.w = Window((200, 200))
            self.w.textEditor = TextEditor((10, 10, -10, 22),
                                callback=self.textEditorCallback)
            self.w.open()
            
        def textEditorCallback(self, sender):
            print 'text entry!', sender.get()
        
    TextEditorDemo()
    """

    def __init__(self, posSize, text="", callback=None, readOnly=False, checksSpelling=False):
        """
        *posSize* Tuple of form (left, top, width, height) representing the position and size of the text entry control.
        
        *text* The text to be displayed in the text entry control.
        
        *callback* The method to be called when the user presses the text entry control.
        
        *readOnly* Boolean representing if the text can be edited or not.
        
        *checksSpelling* Boolean representing if spelling should be automatically checked or not.
        """
        self._posSize = posSize
        self._nsObject = NSScrollView.alloc().init()  # no need to do getNSSubclass() here
        self._nsObject.setHasVerticalScroller_(True)
        self._nsObject.setBorderType_(NSBezelBorder)
        self._nsObject.setDrawsBackground_(True)
        self._textView = getNSSubclass("NSTextView")(self)
        self._textView.setAllowsUndo_(True)
        self._textView.setString_(text)
        self._textView.setContinuousSpellCheckingEnabled_(checksSpelling)
        self._textView.setAutoresizingMask_(NSViewWidthSizable | NSViewHeightSizable)
        self._textView.setEditable_(not readOnly)
        self._nsObject.setDocumentView_(self._textView)
        # do the base object init methods
        self._setCallback(callback)
        self._setAutosizingFromPosSize(posSize)

    def getNSScrollView(self):
        """
        Return the _NSScrollView_ that this object wraps.
        """
        return self._nsObject
    
    def getNSTextView(self):
        """
        Return the _NSTextView_ that this object wraps.
        """
        return self._textView

    def _setCallback(self, callback):
        if callback is not None:
            self._target = VanillaCallbackWrapper(callback)
            delegate = self._textView.delegate()
            if delegate is None:
                self._textViewDelegate = delegate = _VanillaTextEditorDelegate.alloc().init()
                self._textView.setDelegate_(delegate)
            delegate._target = self._target

    def get(self):
        """
        Get the contents of the text entry control.
        """
        return self._textView.string()

    def set(self, value):
        """
        Set the contents of the text box.
        
        *value* A string representing the contents of the text box.
        """
        self._textView.setString_(value)

    def selectAll(self):
        """
        Select all text in the text entry control.
        """
        self._textView.selectAll_(None)

    #def selectLine(self, lineNumber, charOffset=0):
    #    raise NotImplementedError
    #
    #def getSelection(self):
    #    """
    #    Get the selected text.
    #    """
    #    selStart, selEnd = self._textView.selectedRange()
    #    return selStart, selStart+selEnd
    #
    #def setSelection(self, selStart, selEnd):
    #    selEnd = selEnd - selStart
    #    self._textView.setSelectedRange_((selStart, selEnd))
    #
    #def getSelectedText(self):
    #    selStart, selEnd = self.getSelection()
    #    return self._textView.string()[selStart:selEnd]
    #
    #def expandSelection(self):
    #    raise NotImplementedError
    #
    #def insert(self, text):
    #    self._textView.insert_(text)