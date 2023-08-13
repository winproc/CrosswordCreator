import wx
import crossword
import math

Settings = crossword.LoadSettingFile()
CrosswordStrings = crossword.LoadStrings()

Occurences = crossword.GetCharacterOccurences(CrosswordStrings)

GridSide = crossword.GetMaxLength(CrosswordStrings)
if Settings["OverrideGridSize"] > 0:
    GridSide = Settings["OverrideGridSize"]

CurrentSelection = 0
Rotation = 0

App = wx.App()

TopWindow = wx.Frame(parent=None, title="Crossword Creator", size=wx.Size(600, 600))
TopWindow.SetBackgroundColour("white")

App.SetTopWindow(TopWindow)
TopWindow.Show(True)

BlockList = []

CanvasData = crossword.GenerateCanvas(GridSide)

def RefreshCanvas():
    for XIndex in range(1, GridSide + 1):
        for YIndex in range(1, GridSide + 1):
            Id = '{0},{1}'.format(str(XIndex),str(YIndex))
            Box = wx.Window.FindWindowByName(Id)

            Box.SetForegroundColour('black')
            Box.SetLabel(CanvasData[Id])

StringSelection = wx.ListBox(TopWindow, pos=wx.Point(30 * GridSide, 0), size=wx.Size(100, 30 * GridSide))
StringSelection.InsertItems(CrosswordStrings, 0)
StringSelection.SetSelection(CurrentSelection)

def OnSelectionChanged(Event):
    global CurrentSelection
    CurrentSelection = Event.GetSelection()

StringSelection.Bind(wx.EVT_LISTBOX, OnSelectionChanged)

for XIndex in range(0, GridSide):
    for YIndex in range(0, GridSide):

        CharacterBlock = wx.Button(TopWindow, label="-", size=wx.Size(30, 30), pos=wx.Point(30*XIndex, 30*YIndex), name='{0},{1}'.format(str(XIndex + 1), str(YIndex + 1)))
        BlockList.append(CharacterBlock)

        def OnHover(Event):
            RefreshCanvas()

            Text = CrosswordStrings[CurrentSelection]

            Origin = Event.GetEventObject()
            Origin.SetLabel(Text[0])

            if CanvasData[str(Origin.GetName())] != "-":
                Origin.SetForegroundColour('red')

            for Index in range(1, len(Text)):
                Position = [int(i) for i in str(Origin.GetName()).split(',')]

                XOffsetRatio = math.cos(Rotation)
                YOffsetRatio = math.sin(Rotation)

                # Expressions with ternary operators prevent inaccuracies due to computer arithmetic limitations
                Offset = [int(math.copysign(math.ceil(0 if abs(XOffsetRatio) < 0.1 else abs(XOffsetRatio)), XOffsetRatio)) * Index, int(math.copysign(math.ceil(0 if abs(YOffsetRatio) < 0.1 else abs(YOffsetRatio)), YOffsetRatio)) * Index]
                

                Position[0] += Offset[0]
                Position[1] += Offset[1]


                Box = wx.Window.FindWindowByName('{0},{1}'.format(str(Position[0]), str(Position[1])))

                if CanvasData['{0},{1}'.format(str(Position[0]), str(Position[1]))] != "-":
                    Box.SetForegroundColour('red')

                Box.SetLabel(Text[Index])


        def OnClick(Event):
            Text = CrosswordStrings[CurrentSelection]

            Origin = Event.GetEventObject()
            CanvasData[str(Origin.GetName())] = Text[0]

            for Index in range(1, len(Text)):
                Position = [int(i) for i in str(Origin.GetName()).split(',')]

                XOffsetRatio = math.cos(Rotation)
                YOffsetRatio = math.sin(Rotation)

                Offset = [int(math.copysign(math.ceil(0 if abs(XOffsetRatio) < 0.1 else abs(XOffsetRatio)), XOffsetRatio)) * Index, int(math.copysign(math.ceil(0 if abs(YOffsetRatio) < 0.1 else abs(YOffsetRatio)), YOffsetRatio)) * Index]
                

                Position[0] += Offset[0]
                Position[1] += Offset[1]

                CanvasData['{0},{1}'.format(str(Position[0]), str(Position[1]))] = Text[Index]

            RefreshCanvas()
            

        def ChangeRotation(Event):

            global Rotation
            Rotation += (math.pi/4)

            OnHover(Event)
            

        CharacterBlock.Bind(wx.EVT_LEFT_DOWN, OnClick)
        CharacterBlock.Bind(wx.EVT_RIGHT_DOWN, ChangeRotation)
        CharacterBlock.Bind(wx.EVT_ENTER_WINDOW, OnHover)
        
ClearButton = wx.Button(TopWindow, label="Clear", pos=wx.Point(15, 30 * GridSide + 15))
ExportButton = wx.Button(TopWindow, label="Export", pos=wx.Point(ClearButton.GetPosition().x + ClearButton.GetSize().GetWidth() + 15, 30 * GridSide + 15))
MetadataButton = wx.Button(TopWindow, label="Metadata", pos=wx.Point(ExportButton.GetPosition().x + ExportButton.GetSize().GetWidth() + 15, 30 * GridSide + 15))

def OnMetadataRequest(Event):
    MetadataWindow = wx.Frame(parent=None, title="Metadata", size=wx.Size(300, 600))

    wx.StaticText(MetadataWindow, label="Common Characters", size=wx.Size(290, 30), style=wx.ALIGN_CENTER_HORIZONTAL, pos=wx.Point(0, 15))
    StringList = wx.ListBox(MetadataWindow, pos=wx.Point(0, 30), size=wx.Size(290, 500))

    Strings = []
    for char, occurrence in Occurences.items():
        Strings.append('{0}: {1}'.format(char, occurrence))

    StringList.InsertItems(Strings, 0)

    MetadataWindow.Show()

def OnClearRequest(Event):
    for Key, Char in CanvasData.items():
        CanvasData[Key] = '-'
    
    RefreshCanvas()

MetadataButton.Bind(wx.EVT_BUTTON, OnMetadataRequest)
ClearButton.Bind(wx.EVT_BUTTON, OnClearRequest)

App.MainLoop()