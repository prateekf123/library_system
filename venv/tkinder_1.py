import wx
   2 
   3 
   4 class Form(wx.Panel):
   5     ''' The Form class is a wx.Panel that creates a bunch of controls
   6         and handlers for callbacks. Doing the layout of the controls is 
   7         the responsibility of subclasses (by means of the doLayout()
   8         method). '''
   9 
  10     def __init__(self, *args, **kwargs):
  11         super(Form, self).__init__(*args, **kwargs)
  12         self.referrers = ['friends', 'advertising', 'websearch', 'yellowpages']
  13         self.colors = ['blue', 'red', 'yellow', 'orange', 'green', 'purple',
  14                        'navy blue', 'black', 'gray']
  15         self.createControls()
  16         self.bindEvents()
  17         self.doLayout()
  18 
  19     def createControls(self):
  20         self.logger = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY)
  21         self.saveButton = wx.Button(self, label="Save")
  22         self.nameLabel = wx.StaticText(self, label="Your name:")
  23         self.nameTextCtrl = wx.TextCtrl(self, value="Enter here your name")
  24         self.referrerLabel = wx.StaticText(self, 
  25             label="How did you hear from us?")
  26         self.referrerComboBox = wx.ComboBox(self, choices=self.referrers, 
  27             style=wx.CB_DROPDOWN)
  28         self.insuranceCheckBox = wx.CheckBox(self, 
  29             label="Do you want Insured Shipment?")
  30         self.colorRadioBox = wx.RadioBox(self, 
  31             label="What color would you like?", 
  32             choices=self.colors, majorDimension=3, style=wx.RA_SPECIFY_COLS)
  33 
  34     def bindEvents(self):
  35         for control, event, handler in \
  36             [(self.saveButton, wx.EVT_BUTTON, self.onSave),
  37              (self.nameTextCtrl, wx.EVT_TEXT, self.onNameEntered),
  38              (self.nameTextCtrl, wx.EVT_CHAR, self.onNameChanged),
  39              (self.referrerComboBox, wx.EVT_COMBOBOX, self.onReferrerEntered),
  40              (self.referrerComboBox, wx.EVT_TEXT, self.onReferrerEntered),
  41              (self.insuranceCheckBox, wx.EVT_CHECKBOX, self.onInsuranceChanged),
  42              (self.colorRadioBox, wx.EVT_RADIOBOX, self.onColorchanged)]:
  43             control.Bind(event, handler)
  44 
  45     def doLayout(self):
  46         ''' Layout the controls that were created by createControls(). 
  47             Form.doLayout() will raise a NotImplementedError because it 
  48             is the responsibility of subclasses to layout the controls. '''
  49         raise NotImplementedError 
  50 
  51     # Callback methods:
  52 
  53     def onColorchanged(self, event):
  54         self.__log('User wants color: %s'%self.colors[event.GetInt()])
  55 
  56     def onReferrerEntered(self, event):
  57         self.__log('User entered referrer: %s'%event.GetString())
  58 
  59     def onSave(self,event):
  60         self.__log('User clicked on button with id %d'%event.GetId())
  61 
  62     def onNameEntered(self, event):
  63         self.__log('User entered name: %s'%event.GetString())
  64 
  65     def onNameChanged(self, event):
  66         self.__log('User typed character: %d'%event.GetKeyCode())
  67         event.Skip()
  68 
  69     def onInsuranceChanged(self, event):
  70         self.__log('User wants insurance: %s'%bool(event.Checked()))
  71 
  72     # Helper method(s):
  73 
  74     def __log(self, message):
  75         ''' Private method to append a string to the logger text
  76             control. '''
  77         self.logger.AppendText('%s\n'%message)
  78 
  79 
  80 class FormWithAbsolutePositioning(Form):
  81     def doLayout(self):
  82         ''' Layout the controls by means of absolute positioning. '''
  83         for control, x, y, width, height in \
  84                 [(self.logger, 300, 20, 200, 300),
  85                  (self.nameLabel, 20, 60, -1, -1),
  86                  (self.nameTextCtrl, 150, 60, 150, -1),
  87                  (self.referrerLabel, 20, 90, -1, -1),
  88                  (self.referrerComboBox, 150, 90, 95, -1),
  89                  (self.insuranceCheckBox, 20, 180, -1, -1),
  90                  (self.colorRadioBox, 20, 210, -1, -1),
  91                  (self.saveButton, 200, 300, -1, -1)]:
  92             control.SetDimensions(x=x, y=y, width=width, height=height)
  93 
  94 
  95 class FormWithSizer(Form):
  96     def doLayout(self):
  97         ''' Layout the controls by means of sizers. '''
  98 
  99         # A horizontal BoxSizer will contain the GridSizer (on the left)
 100         # and the logger text control (on the right):
 101         boxSizer = wx.BoxSizer(orient=wx.HORIZONTAL)
 102         # A GridSizer will contain the other controls:
 103         gridSizer = wx.FlexGridSizer(rows=5, cols=2, vgap=10, hgap=10)
 104 
 105         # Prepare some reusable arguments for calling sizer.Add():
 106         expandOption = dict(flag=wx.EXPAND)
 107         noOptions = dict()
 108         emptySpace = ((0, 0), noOptions)
 109     
 110         # Add the controls to the sizers:
 111         for control, options in \
 112                 [(self.nameLabel, noOptions),
 113                  (self.nameTextCtrl, expandOption),
 114                  (self.referrerLabel, noOptions),
 115                  (self.referrerComboBox, expandOption),
                   emptySpace,
                  (self.insuranceCheckBox, noOptions),
                   emptySpace,
                  (self.colorRadioBox, noOptions),
                   emptySpace, 
                  (self.saveButton, dict(flag=wx.ALIGN_CENTER))]:
             gridSizer.Add(control, **options)
 
         for control, options in \
                 [(gridSizer, dict(border=5, flag=wx.ALL)),
                  (self.logger, dict(border=5, flag=wx.ALL|wx.EXPAND, 
                     proportion=1))]:
             boxSizer.Add(control, **options)
         self.SetSizerAndFit(boxSizer)
 
 
 class FrameWithForms(wx.Frame):
    def __init__(self, *args, **kwargs):
         super(FrameWithForms, self).__init__(*args, **kwargs)
         notebook = wx.Notebook(self)
         form1 = FormWithAbsolutePositioning(notebook)
         form2 = FormWithSizer(notebook)
         notebook.AddPage(form1, 'Absolute Positioning')
         notebook.AddPage(form2, 'Sizers')
         # We just set the frame to the right size manually. This is feasible
         # for the frame since the frame contains just one component. If the
         # frame had contained more than one component, we would use sizers
         # of course, as demonstrated in the FormWithSizer class above.
         self.SetClientSize(notebook.GetBestSize()) 
 

if __name__ == '__main__':
     app = wx.App(0)
    frame = FrameWithForms(None, title='Demo with Notebook')
    frame.Show()
    app.MainLoop()