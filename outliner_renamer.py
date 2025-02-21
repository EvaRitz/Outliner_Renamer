""" Developed by Eva Ritz"""

import maya.cmds as cmds
from PySide2.QtWidgets import (
    QWidget, QDialog, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QFrame, 
    QSpinBox, QRadioButton, QButtonGroup, QMessageBox, QSizePolicy
)
from PySide2.QtCore import Qt
from PySide2.QtGui import QIntValidator 
import shiboken2  # To wrap Maya's Qt widgets into PySide2
import maya.OpenMayaUI as omui

def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(int(main_window_ptr), QWidget)

class RenameTool(QDialog):  # Changed to QDialog to match your class definition
    def __init__(self, parent=maya_main_window()):
        super(RenameTool, self).__init__(parent)

        # Set window flags to allow minimize and close buttons, ensure it's a normal dialog
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)

        # Make this QDialog non-modal
        self.setModal(False)
        self.init_ui()
        self.show()

    def init_ui(self):
        # Main layout
        self.main_layout = QVBoxLayout()

        self.init_name_section()
        self.main_layout.addWidget(self.separator())  # Separator line

        self.init_incrementation_section()
        self.main_layout.addWidget(self.separator())  # Separator line

        self.init_prefix_section()
        self.main_layout.addWidget(self.separator())  # Separator line

        self.init_suffix_section()
        self.main_layout.addWidget(self.separator())  # Separator line

        self.prefix_selected()
        self.suffix_selected()
        self.set_stylesheet()

        # Add apply button
        self.apply_btn = QPushButton("Apply")
        self.apply_btn.clicked.connect(self.apply_new_name)
        self.main_layout.addWidget(self.apply_btn)

        # Set main layout
        self.setLayout(self.main_layout)
        self.setWindowTitle("Outliner Renamer")
        self.resize(600, 800)

    def init_name_section(self):
        """Initializes the Name section."""
        self.name_layout = QVBoxLayout()
        self.name_h_layout = QHBoxLayout()

        self.name_title = QLabel("Name")
        self.name_label = QLabel("New Name: ")
        self.name_edit = QLineEdit()

        # Set the size policy of the title to expanding
        self.name_title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.name_h_layout.addWidget(self.name_label)
        self.name_h_layout.addWidget(self.name_edit)

        self.name_layout.addWidget(self.name_title)
        self.name_layout.addLayout(self.name_h_layout)

        # Add to main layout
        self.main_layout.addLayout(self.name_layout)

    def init_incrementation_section(self):
        """Initializes the Incrementation section."""
        
        self.incrementation_layout = QHBoxLayout()
        self.padding_layout = QHBoxLayout()

        # Title for the Incrementation section
        self.incrementation_title = QLabel("Incrementation")
        self.incrementation_title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Widgets for start number and padding
        self.incrementation_label = QLabel("Start number: ")
        self.incrementation_edit = QLineEdit('1')
        self.incrementation_edit.setValidator(QIntValidator())  # Integer input only

        self.padding_label = QLabel("Padding:")
        self.padding_edit = QSpinBox()
        self.padding_edit.setMinimum(0)
        self.padding_edit.setMaximum(4)

        # Set size policies for the line edit and spin box
        self.incrementation_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.padding_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Layouts for the input fields
        self.incrementation_h_layout = QHBoxLayout()
        self.incrementation_h_layout.addWidget(self.incrementation_label)
        self.incrementation_h_layout.addWidget(self.incrementation_edit)

        self.padding_h_layout = QHBoxLayout()
        self.padding_h_layout.addWidget(self.padding_label)
        self.padding_h_layout.addWidget(self.padding_edit)

        # Add the horizontal layouts to the group box layout
        self.incrementation_layout.addLayout(self.incrementation_h_layout)
        self.incrementation_layout.addLayout(self.padding_h_layout)

        # Add the title and the QGroupBox to the main layout
        self.main_layout.addWidget(self.incrementation_title)  # Add title before the group box
        self.main_layout.addLayout(self.incrementation_layout)  # Add group box


    def init_prefix_section(self):
        """Initializes the Prefix section."""
        self.prefix_layout = QVBoxLayout()
        self.prefix_btn_layout = QHBoxLayout()

        # Create button group for prefixes
        self.prefix_group = QButtonGroup()
        
        # Widgets
        self.prefix_buttons = {
            "None": QRadioButton("None"),
            "L_": QRadioButton("L_"),
            "R_": QRadioButton("R_"),
            "Custom": QRadioButton("Custom")
        }
        self.prefix_title = QLabel("Prefix")
        # Set the size policy of the title to expanding
        self.prefix_title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.prefix_edit = QLineEdit()

        # Automatically select none first
        self.prefix_buttons["None"].setChecked(True)

        # Disable QLineEdit
        self.prefix_edit.setDisabled(True)

        # Add buttons to button group
        for button in self.prefix_buttons.values():
            self.prefix_group.addButton(button)
            button.clicked.connect(self.prefix_selected)

        # Add to layouts
        for button in self.prefix_buttons.values():
            self.prefix_btn_layout.addWidget(button)
        self.prefix_btn_layout.addWidget(self.prefix_edit)

        self.prefix_layout.addWidget(self.prefix_title)
        self.prefix_layout.addLayout(self.prefix_btn_layout)

        # Add to main layout
        self.main_layout.addLayout(self.prefix_layout)

    def init_suffix_section(self):
        """Initializes the Suffix section."""
        self.suffix_layout = QVBoxLayout()
        self.suffix_layout_1 = QHBoxLayout()
        self.suffix_layout_2 = QHBoxLayout()
        self.suffix_layout_3 = QHBoxLayout()

        self.suffix_title = QLabel("Suffix")
        # Set the size policy of the title to expanding
        self.suffix_title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Create button group for suffixes
        self.suffix_group = QButtonGroup()

        # Widgets
        self.suffix_buttons = {
            "None": QRadioButton("None"),
            "_geo": QRadioButton("_geo"),
            "_crv": QRadioButton("_crv"),
            "_loc": QRadioButton("_loc"),
            "_jnt": QRadioButton("_jnt"),
            "_ctrl": QRadioButton("_ctrl"),
            "_grp": QRadioButton("_grp"),
            "Custom": QRadioButton("Custom")
        }
        self.suffix_edit = QLineEdit()
        # Automatically select none first
        self.suffix_buttons["None"].setChecked(True)

        # Disable QLineEdit
        self.suffix_edit.setDisabled(True)

        # Add buttons to button group
        for button in self.suffix_buttons.values():
            self.suffix_group.addButton(button)
            button.clicked.connect(self.suffix_selected)

        # Horizontal layouts
        for index, (key, button) in enumerate(self.suffix_buttons.items()):
            if index < 3:
                self.suffix_layout_1.addWidget(button)
            elif index < 6:
                self.suffix_layout_2.addWidget(button)
            else:
                self.suffix_layout_3.addWidget(button)

        self.suffix_layout_3.addWidget(self.suffix_edit)

        # Add to suffix layout
        self.suffix_layout.addWidget(self.suffix_title)
        self.suffix_layout.addLayout(self.suffix_layout_1)
        self.suffix_layout.addLayout(self.suffix_layout_2)
        self.suffix_layout.addLayout(self.suffix_layout_3)

        # Add to main layout
        self.main_layout.addLayout(self.suffix_layout)

    def separator(self):
        """Creates a horizontal line separator."""        
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        return line

    def prefix_selected(self):
        """Handles the selection of a prefix radio button."""
        prefix = ""
        selected_button = self.prefix_group.checkedButton()
        if selected_button:
            key = selected_button.text()
            if key == "Custom":
                self.prefix_edit.setDisabled(False)
                prefix_text = self.prefix_edit.text()  # Get text from QLineEdit
                self.prefix_edit.setStyleSheet("background-color: #292929;") # Color when enabled
                if prefix_text:
                    prefix = f"{prefix_text}_"
            else:
                prefix = key  # Use the key from the button
                self.prefix_edit.setDisabled(True)
                self.prefix_edit.setStyleSheet("background-color: #414141;") # Color when disabled

            return prefix if key != "None" else ""

    def suffix_selected(self):
        """Handles the selection of a suffix radio button."""
        suffix =""
        selected_button = self.suffix_group.checkedButton()
        if selected_button:
            key = selected_button.text()
            if key == "Custom":
                self.suffix_edit.setDisabled(False)
                suffix_text = self.suffix_edit.text() # Get text from QLineEdit
                self.suffix_edit.setStyleSheet("background-color: #292929;") # Color when enabled
                if suffix_text:
                    suffix = f"_{suffix_text}"
            else:
                suffix = key  # Use the key from the button
                self.suffix_edit.setDisabled(True)
                self.suffix_edit.setStyleSheet("background-color: #414141;") # Color when disabled

            return suffix if key != "None" else ""

    def apply_new_name(self):
        """Applies the new name based on the selected prefix and suffix."""
        name = self.name_edit.text()
        number = int(self.incrementation_edit.text())
        padding = self.padding_edit.text()
        prefix = self.prefix_selected()
        suffix = self.suffix_selected()
        if not name:
            QMessageBox.warning(self, "Error", f"Please input name!")
            return
        elif not number: 
            QMessageBox.warning(self, "Error", f"Please input number!")
            return
        elif not padding:
            QMessageBox.warning(self, "Error", f"Please input padding!")
            return

        selected_objects = cmds.ls(selection=True)
        if not selected_objects:
            QMessageBox.warning(self, "Error", "No objects selected!")
            return

        for index, obj in enumerate(selected_objects):
            new_name = f"{prefix}{name}_{number + index:0{padding}d}{suffix}"
            cmds.rename(obj, new_name)
            print(f"Renamed {obj} to {new_name}")

        QMessageBox.information(self, "Success", "Objects renamed successfully!")



    def set_stylesheet(self):
        """Sets the styles for various UI components."""
        # Set background color for the title
        self.name_title.setStyleSheet("""
                                    background-color: DimGray;
                                    padding: 5px;
                                    color: LightGray;
                                    font-weight: bold; 
                                      """)
        self.incrementation_title.setStyleSheet("""
                                    background-color: DimGray;
                                    padding: 5px;
                                    color: LightGray;
                                    font-weight: bold; 
                                      """)  # Change the color here
        self.prefix_title.setStyleSheet("""
                                    background-color: DimGray;
                                    padding: 5px;
                                    color: LightGray;
                                    font-weight: bold; 
                                      """)  # Change the color here
        self.suffix_title.setStyleSheet("""
                                    background-color: DimGray;
                                    padding: 5px;
                                    color: LightGray;
                                    font-weight: bold; 
                                      """)  # Change the color here

# Create and show the dialog
rename_tool = RenameTool()