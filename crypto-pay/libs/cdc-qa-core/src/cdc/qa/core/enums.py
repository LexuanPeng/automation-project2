from enum import Enum


class Agent(Enum):
    LOCAL = "local"
    REMOTE = "remote"
    BROWSERSTACK = "browserstack"


class Platform(Enum):
    ANDROID = "android"
    IOS = "ios"
    CHROME = "chrome"
    FIREFOX = "firefox"
    SAFARI = "safari"


class AndroidClassName(Enum):
    Button = "android.widget.Button"
    CheckBox = "android.widget.CheckBox"
    CheckedTextView = "android.widget.CheckedTextView"
    EditText = "android.widget.EditText"
    ListView = "android.widget.ListView"
    ImageButton = "android.widget.ImageButton"
    ImageView = "android.widget.ImageView"
    Spinner = "android.widget.Spinner"
    TextView = "android.widget.TextView"
    Switch = "android.widget.Switch"
    RadioButton = "android.widget.RadioButton"
    View = "android.view.View"


class IosClassName(Enum):
    Button = "XCUIElementTypeButton"
    Image = "XCUIElementTypeImage"
    StaticText = "XCUIElementTypeStaticText"
    Other = "XCUIElementTypeOther"
    PickerWheel = "XCUIElementTypePickerWheel"
    TextField = "XCUIElementTypeTextField"
    Switch = "XCUIElementTypeSwitch"
    TextView = "XCUIElementTypeTextView"
