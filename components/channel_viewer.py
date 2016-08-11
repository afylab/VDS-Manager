from PyQt4 import QtGui as gui, QtCore as core

###########################
## ChannelInstance class ##
###########################
class ChannelInstance(object):
	def __init__(
		self,
		context,
		ID,
		name,
		label,
		description,
		tags,
		has_get,
		has_set,
		get_setting,
		get_inputs,
		get_inputs_units,
		set_setting,
		set_var_slot,
		set_var_units,
		set_statics,
		set_statics_units,
		set_min,
		set_max,
		set_offset,
		set_scale,
		):

			self.context     = context
			self.ID          = ID
			self.name        = name
			self.label       = label
			self.description = description
			self.tags        = tags
			self.has_get = has_get
			self.has_set = has_set
			self.get_setting      = get_setting
			self.get_inputs       = get_inputs
			self.get_inputs_units = get_inputs_units

			self.set_setting       = set_setting
			self.set_var_slot      = set_var_slot
			self.set_var_units     = set_var_units
			self.set_statics       = set_statics
			self.set_statics_units = set_statics_units
			self.set_min           = set_min
			self.set_max           = set_max
			self.set_offset        = set_offset
			self.set_scale         = set_scale




#########################
## INTERFACE / WIDGETS ##
#########################

class ChannelModificationControlWidget(gui.QWidget):
	def __init__(self,parent):
		super(ChannelModificationControlWidget,self).__init__(parent)

		self.VBoxMain     = gui.QVBoxLayout(); self.VBoxMain.setContentsMargins(0,0,0,0)    ; self.VBoxMain.setSpacing(0)
		self.VBoxButtons  = gui.QVBoxLayout(); self.VBoxButtons.setContentsMargins(0,0,0,0) ; self.VBoxButtons.setSpacing(0)
		self.VBoxConfirm  = gui.QVBoxLayout(); self.VBoxConfirm.setContentsMargins(0,0,0,0) ; self.VBoxConfirm.setSpacing(0)
		self.HBoxControls = gui.QHBoxLayout(); self.HBoxControls.setContentsMargins(0,0,0,0); self.HBoxControls.setSpacing(0)

		self.button_save_changes   = gui.QPushButton("save changes",self)
		self.checkbox_save_changes = gui.QCheckBox("confirm",self)
		self.button_discard_changes   = gui.QPushButton("discard changes",self)
		self.checkbox_discard_changes = gui.QCheckBox("confirm",self)

		self.checkbox_enable_modification = gui.QCheckBox("enable modification",self)

		self.VBoxButtons.addWidget(self.button_save_changes)
		self.VBoxButtons.addWidget(self.button_discard_changes)
		self.VBoxConfirm.addWidget(self.checkbox_save_changes)
		self.VBoxConfirm.addWidget(self.checkbox_discard_changes)
		self.HBoxControls.addLayout(self.VBoxButtons)
		self.HBoxControls.addLayout(self.VBoxConfirm)

		self.VBoxMain.addWidget(self.checkbox_enable_modification)
		self.VBoxMain.addLayout(self.HBoxControls)
		self.setLayout(self.VBoxMain)

		self.button_save_changes.clicked.connect(self.save_changes)
		self.button_discard_changes.clicked.connect(self.discard_changes)
		self.checkbox_enable_modification.stateChanged.connect(self.update_modification_permission)

	def save_changes(self,event):
		if self.checkbox_save_changes.isChecked():
			print("SAVE CHANGES")
		else:
			print("MUST CHECK 'CONFIRM' TO SAVE CHANGES")

	def discard_changes(self,event):
		if self.checkbox_discard_changes.isChecked():
			print("DISCARD CHANGES")
		else:
			print("MUST CHECK 'CONFIRM' TO DISCARD CHANGES")

	def update_modification_permission(self,event):
		if self.checkbox_enable_modification.isChecked():
			print("ENABLING MODIFICATION")
		else:
			print("DISABLING MODIFICATION")