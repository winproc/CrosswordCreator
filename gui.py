import wx
import crossword
import math

Settings = crossword.LoadSettingFile()
CrosswordStrings = crossword.LoadStrings()

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
            Id = '{0}{1}'.format(str(XIndex),str(YIndex))
            Box = wx.Window.FindWindowById(int(Id))

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

        CharacterBlock = wx.Button(TopWindow, label="-", size=wx.Size(30, 30), pos=wx.Point(30*XIndex, 30*YIndex), id=int('{0}{1}'.format(str(XIndex + 1), str(YIndex + 1))))
        BlockList.append(CharacterBlock)

        def OnHover(Event):
            RefreshCanvas()

            Text = CrosswordStrings[CurrentSelection]

            Origin = Event.GetEventObject()
            Origin.SetLabel(Text[0])

            if CanvasData[str(Origin.GetId())] != "-":
                Origin.SetForegroundColour('red')

            for Index in range(1, len(Text)):
                Position = [int(i) for i in [x for x in str(Origin.GetId())]]

                XOffsetRatio = math.cos(Rotation)
                YOffsetRatio = math.sin(Rotation)

                # Expressions with ternary operators prevent inaccuracies due to computer arithmetic limitations
                Offset = [int(math.copysign(math.ceil(0 if abs(XOffsetRatio) < 0.1 else abs(XOffsetRatio)), XOffsetRatio)) * Index, int(math.copysign(math.ceil(0 if abs(YOffsetRatio) < 0.1 else abs(YOffsetRatio)), YOffsetRatio)) * Index]
                

                Position[0] += Offset[0]
                Position[1] += Offset[1]


                Box = wx.Window.FindWindowById(int('{0}{1}'.format(str(Position[0]), str(Position[1]))))

                if CanvasData['{0}{1}'.format(str(Position[0]), str(Position[1]))] != "-":
                    Box.SetForegroundColour('red')

                Box.SetLabel(Text[Index])


        def OnClick(Event):
            Text = CrosswordStrings[CurrentSelection]

            Origin = Event.GetEventObject()
            CanvasData[str(Origin.GetId())] = Text[0]

            for Index in range(1, len(Text)):
                Position = [int(i) for i in [x for x in str(Origin.GetId())]]

                XOffsetRatio = math.cos(Rotation)
                YOffsetRatio = math.sin(Rotation)

                Offset = [int(math.copysign(math.ceil(0 if abs(XOffsetRatio) < 0.1 else abs(XOffsetRatio)), XOffsetRatio)) * Index, int(math.copysign(math.ceil(0 if abs(YOffsetRatio) < 0.1 else abs(YOffsetRatio)), YOffsetRatio)) * Index]
                

                Position[0] += Offset[0]
                Position[1] += Offset[1]

                CanvasData['{0}{1}'.format(str(Position[0]), str(Position[1]))] = Text[Index]

            RefreshCanvas()
            

        def ChangeRotation(Event):

            global Rotation
            Rotation += (math.pi/4)

            OnHover(Event)
            

        CharacterBlock.Bind(wx.EVT_LEFT_DOWN, OnClick)
        CharacterBlock.Bind(wx.EVT_RIGHT_DOWN, ChangeRotation)
        CharacterBlock.Bind(wx.EVT_ENTER_WINDOW, OnHover)
        
ClearButton = wx.Button(TopWindow, label="Clear", pos=wx.Point(15, 30 * GridSide + 15))
RandomizeButton = wx.Button(TopWindow, label="Randomize", pos=wx.Point(ClearButton.GetPosition().x + ClearButton.GetSize().GetWidth() + 15, 30 * GridSide + 15))
MetadataButton = wx.Button(TopWindow, label="Metadata", pos=wx.Point(RandomizeButton.GetPosition().x + RandomizeButton.GetSize().GetWidth() + 15, 30 * GridSide + 15))






App.MainLoop()