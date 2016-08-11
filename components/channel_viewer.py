from PyQt4 import QtGui as gui, QtCore as core

###########################
## ChannelInstance class ##
###########################
class ChannelInstance(object):
	def __init__(
		self,
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
class ChannelSelectorWidget(gui.QWidget):
	def __init__(self,parent,connection):
		super(ChannelSelectorWidget,self).__init__(parent)
		self.connection = connection
		self.vds        = connection.virtual_device_server

		self.VBoxName = gui.QVBoxLayout();self.VBoxName.setSpacing(0)
		self.VBoxID   = gui.QVBoxLayout();self.VBoxID.setSpacing(0)
		self.HBoxMain = gui.QHBoxLayout();self.HBoxMain.setSpacing(0)

		self.ch_name = gui.QListWidget(self)
		self.ch_id   = gui.QListWidget(self)
		self.ch_name.currentRowChanged.connect(self.ch_id.setCurrentRow)
		self.ch_id.currentRowChanged.connect(self.ch_name.setCurrentRow)
		self.ch_name.verticalScrollBar().valueChanged.connect(self.ch_id.verticalScrollBar().setValue)
		self.ch_id.verticalScrollBar().valueChanged.connect(self.ch_name.verticalScrollBar().setValue)
		
		self.channels = []

		self.label_name    = gui.QLineEdit("name",self); self.label_name.setReadOnly(True)
		self.label_id      = gui.QLineEdit("ID",self)  ; self.label_id.setReadOnly(True)

		self.VBoxName.addWidget(self.label_name)
		self.VBoxName.addWidget(self.ch_name)
		self.VBoxID.addWidget(self.label_id)
		self.VBoxID.addWidget(self.ch_id)
		self.HBoxMain.addLayout(self.VBoxName, 4)
		self.HBoxMain.addLayout(self.VBoxID  , 1)

		self.setLayout(self.HBoxMain)
		self.populate()

	def populate(self):
		"""Reloads channel info from registry. This should be called whenever a setting is updated/added/deleted."""
		self.ch_name.clear()
		self.ch_id.clear()
		self.channels = self.vds.list_channels()
		for channel in self.channels:
			self.ch_name.addItem(channel[1])
			self.ch_id.addItem(channel[0])

	def set_editing_mode(self,mode):
		if mode not in ['viewing','editing','creating']:
			return
		self.set_enabled(mode == 'viewing')

	def set_enabled(self,is_enabled):
		self.ch_name.setEnabled(is_enabled)
		self.ch_id.setEnabled(is_enabled)


class ChannelDescriptiveInfoWidget(gui.QWidget):
	def __init__(self,parent):
		super(ChannelDescriptiveInfoWidget,self).__init__(parent)

		self.label_name  = gui.QLineEdit("name" , self); self.label_name.setReadOnly(True)
		self.label_id    = gui.QLineEdit("ID"   , self); self.label_id.setReadOnly(True)
		self.label_label = gui.QLineEdit("label", self); self.label_label.setReadOnly(True)
		self.input_name  = gui.QLineEdit("",self); self.input_name.setPlaceholderText("channel name")
		self.input_id    = gui.QLineEdit("",self); self.input_id.setPlaceholderText("channel ID")
		self.input_label = gui.QLineEdit("",self); self.input_label.setPlaceholderText("channel axis label")
		self.VBoxUpperLabels = gui.QVBoxLayout(); self.VBoxUpperLabels.setSpacing(0)
		self.VBoxUpperInputs = gui.QVBoxLayout(); self.VBoxUpperInputs.setSpacing(0)
		self.HBoxUpper       = gui.QHBoxLayout(); self.HBoxUpper.setSpacing(0)
		self.VBoxUpperLabels.addWidget(self.label_name)
		self.VBoxUpperLabels.addWidget(self.label_id)
		self.VBoxUpperLabels.addWidget(self.label_label)
		self.VBoxUpperInputs.addWidget(self.input_name)
		self.VBoxUpperInputs.addWidget(self.input_id)
		self.VBoxUpperInputs.addWidget(self.input_label)
		self.HBoxUpper.addLayout(self.VBoxUpperLabels,1)
		self.HBoxUpper.addLayout(self.VBoxUpperInputs,4)


		self.label_description  = gui.QLineEdit("description",self);self.label_description.setReadOnly(True)
		self.input_description = gui.QPlainTextEdit(self)
		self.VBoxDescription   = gui.QVBoxLayout()
		self.VBoxDescription.addWidget(self.label_description,1)
		self.VBoxDescription.addWidget(self.input_description,4)


		self.label_tags        = gui.QLineEdit("tags",self);self.label_tags.setReadOnly(True)
		self.input_add_tag     = gui.QLineEdit("",self);self.input_add_tag.setPlaceholderText("tag to add")
		self.button_add_tag    = gui.QPushButton("add",self)
		self.list_tags         = gui.QListWidget(self)
		self.button_del_tag    = gui.QPushButton("delete",self)
		self.button_clear_tags = gui.QPushButton("clear",self)
		self.cb_clear_tags     = gui.QCheckBox("confirm clear",self)
		self.HBoxTagsUpper = gui.QHBoxLayout()
		self.HBoxTagsLower = gui.QHBoxLayout()
		self.VBoxTags      = gui.QVBoxLayout()
		self.HBoxTagsUpper.addWidget(self.label_tags,1)
		self.HBoxTagsUpper.addWidget(self.input_add_tag,3)
		self.HBoxTagsUpper.addWidget(self.button_add_tag,1)
		self.HBoxTagsLower.addWidget(self.button_del_tag,1)
		self.HBoxTagsLower.addWidget(self.button_clear_tags,1)
		self.HBoxTagsLower.addWidget(self.cb_clear_tags,3)
		self.VBoxTags.addLayout(self.HBoxTagsUpper,1)
		self.VBoxTags.addWidget(self.list_tags,3)
		self.VBoxTags.addLayout(self.HBoxTagsLower,1)


		self.VBoxMain = gui.QVBoxLayout(); self.VBoxMain.setSpacing(0)
		self.VBoxMain.addLayout(self.HBoxUpper,0)
		self.VBoxMain.addLayout(self.VBoxDescription,1)
		self.VBoxMain.addLayout(self.VBoxTags,1)

		self.setLayout(self.VBoxMain)
		self.channel = None
		self.set_editing_mode("viewing") # modes are "viewing", "editing", "creating"


		self.button_add_tag.clicked.connect(self.add_tag)
		self.input_add_tag.returnPressed.connect(self.add_tag)
		self.button_del_tag.clicked.connect(self.del_tag)
		self.button_clear_tags.clicked.connect(self.clear_tags)

	def add_tag(self):
		tag = str(self.input_add_tag.text())
		if len(tag) > 0:
			items = [str(self.list_tags.item(n).text()) for n in range(self.list_tags.count())]
			if not (tag in items):
				self.list_tags.addItem(tag)
				self.input_add_tag.setText('')

	def del_tag(self):
		row=self.list_tags.currentRow()
		if row >= 0: # row = -1 if no object selected
			self.list_tags.takeItem(row)

	def clear_tags(self):
		if self.cb_clear_tags.isChecked():
			self.list_tags.clear()
			self.cb_clear_tags.setChecked(False)

	def set_editing_mode(self,mode):
		if not (mode in ['viewing','editing','creating']):
			return

		self.input_name.setReadOnly( mode != 'creating' ) # can only set/edit name/ID if 
		self.input_id.setReadOnly(   mode != 'creating' ) # we are creating the channel.

		self.input_label.setReadOnly(       mode == 'viewing' )
		self.input_description.setReadOnly( mode == 'viewing' )
		self.input_add_tag.setReadOnly(     mode == 'viewing' )

		self.button_add_tag.setEnabled( mode != 'viewing' )
		self.button_del_tag.setEnabled( mode != 'viewing' )
		self.button_clear_tags.setEnabled( mode != 'viewing' )

		self.cb_clear_tags.setEnabled( mode != 'viewing' )

	def new_channel(self):
		self.channel = None # no active channel (active channels correspond to a channel being modified)
		self.clear_fields()
		self.set_editing_mode('creating')

	def load_channel(self,channel):
		self.channel = channel
		self.input_name.setText(channel.name)
		self.input_id.setText(channel.ID)
		self.input_label.setText(channel.label)
		self.input_description.setPlainText(channel.description)

		self.list_tags.clear()
		for tag in channel.tags:
			self.list_tags.addItem(str(tag))

	def clear_fields(self):
		self.input_name.setText('')
		self.input_id.setText('')
		self.input_label.setText('')
		self.input_description.setPlainText('')
		self.input_add_tag.setText('')
		self.list_tags.clear()
		self.cb_clear_tags.setChecked(False)


class ChannelDeviceInfoWidget(gui.QWidget):
	def __init__(self,parent):
		super(ChannelDeviceInfoWidget,self).__init__(parent)

		self.channel = None

		self.cb_has_get   = gui.QCheckBox("has get", self)
		self.cb_has_set   = gui.QCheckBox("has set", self)
		self.label_min    = gui.QLineEdit("minimum", self); self.label_min.setReadOnly(True)
		self.label_max    = gui.QLineEdit("maximum", self); self.label_max.setReadOnly(True)
		self.label_offset = gui.QLineEdit("offset" , self); self.label_offset.setReadOnly(True)
		self.label_scale  = gui.QLineEdit("scale"  , self); self.label_scale.setReadOnly(True)
		self.input_min    = gui.QLineEdit(self)
		self.input_max    = gui.QLineEdit(self)
		self.input_offset = gui.QLineEdit(self)
		self.input_scale  = gui.QLineEdit(self)
		self.VBoxScaleLabels = gui.QVBoxLayout(); self.VBoxScaleLabels.setSpacing(0)
		self.VBoxScaleInputs = gui.QVBoxLayout(); self.VBoxScaleInputs.setSpacing(0)
		self.HBoxScale       = gui.QHBoxLayout(); self.HBoxScale.setSpacing(0)
		
		self.VBoxScaleLabels.addWidget(self.label_min)
		self.VBoxScaleLabels.addWidget(self.label_max)
		self.VBoxScaleLabels.addWidget(self.label_offset)
		self.VBoxScaleLabels.addWidget(self.label_scale)
		self.VBoxScaleInputs.addWidget(self.input_min)
		self.VBoxScaleInputs.addWidget(self.input_max)
		self.VBoxScaleInputs.addWidget(self.input_offset)
		self.VBoxScaleInputs.addWidget(self.input_scale)
		self.HBoxScale.addLayout(self.VBoxScaleLabels,1)
		self.HBoxScale.addLayout(self.VBoxScaleInputs,4)

		self.tabs_get_set = gui.QTabWidget(self)
		self.tab_get = ChannelGetInfoWidget(self)
		self.tab_set = ChannelSetInfoWidget(self)
		self.tabs_get_set.addTab(self.tab_get,"get")
		self.tabs_get_set.addTab(self.tab_set,"set")

		self.VBoxMain = gui.QVBoxLayout()
		self.VBoxMain.addWidget(self.cb_has_get,0)
		self.VBoxMain.addWidget(self.cb_has_set,0)
		self.VBoxMain.addLayout(self.HBoxScale,0)
		self.VBoxMain.addWidget(self.tabs_get_set,1)

		self.setLayout(self.VBoxMain)
		self.set_editing_mode('viewing')

	def set_editing_mode(self,mode):
		if not (mode in ['viewing','editing','creating']):
			return

		self.cb_has_get.setEnabled( mode != 'viewing' )
		self.cb_has_set.setEnabled( mode != 'viewing' )
		self.input_min.setReadOnly(    mode=='viewing' )
		self.input_max.setReadOnly(    mode=='viewing' )
		self.input_offset.setReadOnly( mode=='viewing' )
		self.input_scale.setReadOnly(  mode=='viewing' )

		self.tab_get.set_editing_mode(mode)
		self.tab_set.set_editing_mode(mode)

	def new_channel(self):
		self.channel = None
		self.clear_fields()
		self.set_editing_mode('creating')

	def load_channel(self,channel):
		self.channel = channel

		self.cb_has_get.setChecked(channel.has_get)
		self.cb_has_set.setChecked(channel.has_set)
		self.input_min.setText(str(channel.set_min))
		self.input_max.setText(str(channel.set_max))
		self.input_offset.setText(str(channel.set_offset))
		self.input_scale.setText(str(channel.set_scale))

		self.tab_get.load_channel(channel)
		self.tab_set.load_channel(channel)

	def clear_fields(self):
		self.cb_has_get.setChecked(False)
		self.cb_has_set.setChecked(False)
		self.input_min.setText("")
		self.input_max.setText("")
		self.input_offset.setText("")
		self.input_scale.setText("")
		self.tab_get.clear_fields()
		self.tab_set.clear_fields()


class ChannelGetInfoWidget(gui.QWidget):
	def __init__(self,parent):
		super(ChannelGetInfoWidget,self).__init__(parent)

		self.label_server  = gui.QLineEdit("server",self) ; self.label_server.setReadOnly(True)
		self.label_device  = gui.QLineEdit("device",self) ; self.label_device.setReadOnly(True)
		self.label_setting = gui.QLineEdit("setting",self); self.label_setting.setReadOnly(True)
		self.input_server  = gui.QLineEdit(self)
		self.input_device  = gui.QLineEdit(self)
		self.input_setting = gui.QLineEdit(self)

		self.inputs = [] # list of [ [value, units], ... ]
		self.label_inputs     = gui.QLineEdit("inputs",self); self.label_inputs.setReadOnly(True)
		self.input_value      = gui.QLineEdit(self); self.input_value.setPlaceholderText("value")
		self.input_units      = gui.QLineEdit(self); self.input_units.setPlaceholderText("units")
		self.button_add_input = gui.QPushButton("add",self)
		self.list_inputs      = gui.QListWidget(self)
		self.button_del_input    = gui.QPushButton("delete",self)
		self.button_clear_inputs = gui.QPushButton("clear",self)
		self.cb_clear_inputs     = gui.QCheckBox("confirm clear",self)

		self.VBoxLabels = gui.QVBoxLayout(); self.VBoxLabels.setSpacing(0)
		self.VBoxInputs = gui.QVBoxLayout(); self.VBoxInputs.setSpacing(0)
		self.HBoxTop    = gui.QHBoxLayout(); self.HBoxTop.setSpacing(0)
		self.VBoxLabels.addWidget(self.label_server);self.VBoxLabels.addWidget(self.label_device);self.VBoxLabels.addWidget(self.label_setting)
		self.VBoxInputs.addWidget(self.input_server);self.VBoxInputs.addWidget(self.input_device);self.VBoxInputs.addWidget(self.input_setting)
		self.HBoxTop.addLayout(self.VBoxLabels,1);self.HBoxTop.addLayout(self.VBoxInputs,4)

		self.HBoxInputsListTop = gui.QHBoxLayout(); self.HBoxInputsListTop.setSpacing(0)
		self.HBoxInptusListBot = gui.QHBoxLayout(); self.HBoxInptusListBot.setSpacing(0)
		self.VBoxInputsList    = gui.QVBoxLayout(); self.VBoxInputsList.setSpacing(0)
		self.HBoxInputsListTop.addWidget(self.label_inputs,1);self.HBoxInputsListTop.addWidget(self.input_value,2);self.HBoxInputsListTop.addWidget(self.input_units,1);self.HBoxInputsListTop.addWidget(self.button_add_input,1)
		self.HBoxInptusListBot.addWidget(self.button_del_input);self.HBoxInptusListBot.addWidget(self.button_clear_inputs);self.HBoxInptusListBot.addWidget(self.cb_clear_inputs)
		self.VBoxInputsList.addLayout(self.HBoxInputsListTop,0)
		self.VBoxInputsList.addWidget(self.list_inputs,1)
		self.VBoxInputsList.addLayout(self.HBoxInptusListBot,0)

		self.VBoxMain = gui.QVBoxLayout()
		self.VBoxMain.addLayout(self.HBoxTop,0)
		self.VBoxMain.addLayout(self.VBoxInputsList,1)
		self.setLayout(self.VBoxMain)

		self.button_add_input.clicked.connect(self.add_input)
		self.input_value.returnPressed.connect(self.add_input)
		self.input_units.returnPressed.connect(self.add_input)
		self.button_del_input.clicked.connect(self.del_input)
		self.button_clear_inputs.clicked.connect(self.clear_inputs)

	def add_input(self):
		value = str(self.input_value.text())
		units = str(self.input_units.text())
		if len(value) and len(units):
			self.inputs.append([value,units])
			self.list_inputs.addItem("{value} ({units})".format(value=value,units=units))
			self.input_value.setText("")
			self.input_units.setText("")

	def del_input(self):
		row = self.list_inputs.currentRow()
		if row >= 0:
			self.list_inputs.takeItem(row)
			del self.inputs[row]

	def clear_inputs(self):
		if self.cb_clear_inputs.isChecked():
			self.list_inputs.clear()
			self.inputs = []
			self.cb_clear_inputs.setChecked(False)

	def set_editing_mode(self,mode):
		if not (mode in ['viewing','editing','creating']):
			return

		self.input_server.setReadOnly(mode == 'viewing')
		self.input_device.setReadOnly(mode == 'viewing')
		self.input_setting.setReadOnly(mode == 'viewing')
		self.input_value.setReadOnly(mode == 'viewing')
		self.input_units.setReadOnly(mode == 'viewing')
		self.button_add_input.setEnabled(mode != 'viewing')
		self.button_del_input.setEnabled(mode != 'viewing')
		self.button_clear_inputs.setEnabled(mode != 'viewing')
		self.cb_clear_inputs.setEnabled(mode != 'viewing')

	def load_channel(self,channel):
		self.clear_fields()
		self.input_server.setText(channel.get_setting[0])
		self.input_device.setText(channel.get_setting[1])
		self.input_setting.setText(channel.get_setting[2])
		
		for inp in range(len(channel.get_inputs)):
			self.inputs.append([channel.get_inputs[inp],channel.get_inputs_units[inp]])
			self.list_inputs.addItem("{input} ({units})".format(input=channel.get_inputs[inp],units=channel.get_inputs_units[inp]))

	def clear_fields(self):
		self.inputs = []
		self.list_inputs.clear()
		self.input_server.setText('')
		self.input_device.setText('')
		self.input_setting.setText('')
		self.input_value.setText('')
		self.input_units.setText('')
		self.cb_clear_inputs.setChecked(False)


class ChannelSetInfoWidget(gui.QWidget):
	def __init__(self,parent):
		super(ChannelSetInfoWidget,self).__init__(parent)
		self.label_server  = gui.QLineEdit("server",self) ; self.label_server.setReadOnly(True)
		self.label_device  = gui.QLineEdit("device",self) ; self.label_device.setReadOnly(True)
		self.label_setting = gui.QLineEdit("setting",self); self.label_setting.setReadOnly(True)
		self.input_server  = gui.QLineEdit(self)
		self.input_device  = gui.QLineEdit(self)
		self.input_setting = gui.QLineEdit(self)

		self.label_var_slot  = gui.QLineEdit("variable slot",self) ; self.label_var_slot.setReadOnly(True)
		self.label_var_units = gui.QLineEdit("variable units",self); self.label_var_units.setReadOnly(True)
		self.input_var_slot  = gui.QLineEdit(self)
		self.input_var_units = gui.QLineEdit(self)

		self.inputs = [] # list of [ [value, units], ... ]
		self.label_inputs     = gui.QLineEdit("inputs",self); self.label_inputs.setReadOnly(True)
		self.input_value      = gui.QLineEdit(self); self.input_value.setPlaceholderText("value")
		self.input_units      = gui.QLineEdit(self); self.input_units.setPlaceholderText("units")
		self.button_add_input = gui.QPushButton("add",self)
		self.list_inputs      = gui.QListWidget(self)
		self.button_del_input    = gui.QPushButton("delete",self)
		self.button_clear_inputs = gui.QPushButton("clear",self)
		self.cb_clear_inputs     = gui.QCheckBox("confirm clear",self)

		self.VBoxLabels = gui.QVBoxLayout(); self.VBoxLabels.setSpacing(0)
		self.VBoxInputs = gui.QVBoxLayout(); self.VBoxInputs.setSpacing(0)
		self.HBoxTop    = gui.QHBoxLayout(); self.HBoxTop.setSpacing(0)
		self.VBoxLabels.addWidget(self.label_server);self.VBoxLabels.addWidget(self.label_device);self.VBoxLabels.addWidget(self.label_setting)
		self.VBoxInputs.addWidget(self.input_server);self.VBoxInputs.addWidget(self.input_device);self.VBoxInputs.addWidget(self.input_setting)
		self.HBoxTop.addLayout(self.VBoxLabels,1);self.HBoxTop.addLayout(self.VBoxInputs,4)

		self.VBoxVarLabels = gui.QVBoxLayout();self.VBoxVarLabels.setSpacing(0)
		self.VBoxVarInputs = gui.QVBoxLayout();self.VBoxVarInputs.setSpacing(0)
		self.HBoxVar       = gui.QHBoxLayout();self.HBoxVar.setSpacing(0)
		self.VBoxVarLabels.addWidget(self.label_var_slot);self.VBoxVarLabels.addWidget(self.label_var_units)
		self.VBoxVarInputs.addWidget(self.input_var_slot);self.VBoxVarInputs.addWidget(self.input_var_units)
		self.HBoxVar.addLayout(self.VBoxVarLabels);self.HBoxVar.addLayout(self.VBoxVarInputs)

		self.HBoxInputsListTop = gui.QHBoxLayout(); self.HBoxInputsListTop.setSpacing(0)
		self.HBoxInptusListBot = gui.QHBoxLayout(); self.HBoxInptusListBot.setSpacing(0)
		self.VBoxInputsList    = gui.QVBoxLayout(); self.VBoxInputsList.setSpacing(0)
		self.HBoxInputsListTop.addWidget(self.label_inputs,1);self.HBoxInputsListTop.addWidget(self.input_value,2);self.HBoxInputsListTop.addWidget(self.input_units,1);self.HBoxInputsListTop.addWidget(self.button_add_input,1)
		self.HBoxInptusListBot.addWidget(self.button_del_input);self.HBoxInptusListBot.addWidget(self.button_clear_inputs);self.HBoxInptusListBot.addWidget(self.cb_clear_inputs)
		self.VBoxInputsList.addLayout(self.HBoxInputsListTop,0)
		self.VBoxInputsList.addWidget(self.list_inputs,1)
		self.VBoxInputsList.addLayout(self.HBoxInptusListBot,0)

		self.VBoxMain = gui.QVBoxLayout()
		self.VBoxMain.addLayout(self.HBoxTop,0)
		self.VBoxMain.addLayout(self.HBoxVar,0)
		self.VBoxMain.addLayout(self.VBoxInputsList,1)
		self.setLayout(self.VBoxMain)
		self.set_editing_mode('viewing')

		self.button_add_input.clicked.connect(self.add_input)
		self.input_value.returnPressed.connect(self.add_input)
		self.input_units.returnPressed.connect(self.add_input)
		self.button_del_input.clicked.connect(self.del_input)
		self.button_clear_inputs.clicked.connect(self.clear_inputs)

	def add_input(self):
		value = str(self.input_value.text())
		units = str(self.input_units.text())
		if len(value) and len(units):
			self.inputs.append([value,units])
			self.list_inputs.addItem("{value} ({units})".format(value=value,units=units))
			self.input_value.setText("")
			self.input_units.setText("")

	def del_input(self):
		row = self.list_inputs.currentRow()
		if row >= 0:
			self.list_inputs.takeItem(row)
			del self.inputs[row]

	def clear_inputs(self):
		if self.cb_clear_inputs.isChecked():
			self.list_inputs.clear()
			self.inputs = []
			self.cb_clear_inputs.setChecked(False)

	def set_editing_mode(self,mode):
		if not (mode in ['viewing','editing','creating']):
			return

		self.input_server.setReadOnly(mode == 'viewing')
		self.input_device.setReadOnly(mode == 'viewing')
		self.input_setting.setReadOnly(mode == 'viewing')
		self.input_value.setReadOnly(mode == 'viewing')
		self.input_units.setReadOnly(mode == 'viewing')
		self.input_var_slot.setReadOnly(mode == 'viewing')
		self.input_var_units.setReadOnly(mode == 'viewing')

		self.button_add_input.setEnabled(mode != 'viewing')
		self.button_del_input.setEnabled(mode != 'viewing')
		self.button_clear_inputs.setEnabled(mode != 'viewing')
		self.cb_clear_inputs.setEnabled(mode != 'viewing')


	def load_channel(self,channel):
		self.clear_fields()
		self.input_server.setText(channel.set_setting[0])
		self.input_device.setText(channel.set_setting[1])
		self.input_setting.setText(channel.set_setting[2])
		self.input_var_slot.setText(str(channel.set_var_slot))
		self.input_var_units.setText(str(channel.set_var_units))
		
		for inp in range(len(channel.set_statics)):
			self.inputs.append([channel.set_statics[inp],channel.set_statics_units[inp]])
			self.list_inputs.addItem("{input} ({units})".format(input=channel.set_statics[inp],units=channel.set_statics_units[inp]))


	def clear_fields(self):
		self.inputs = []
		self.list_inputs.clear()
		self.input_server.setText('')
		self.input_device.setText('')
		self.input_setting.setText('')
		self.input_value.setText('')
		self.input_units.setText('')
		self.input_var_slot.setText('')
		self.input_var_units.setText('')
		self.cb_clear_inputs.setChecked(False)

class ChannelModificationControlWidget(gui.QWidget):
	def __init__(self,parent):
		super(ChannelModificationControlWidget,self).__init__(parent)

		self.mode = 'viewing' # mode can be 'viewing' 'editing' and 'creating'

		self.button_edit_channel = gui.QPushButton("edit channel"   , self)
		self.button_new_channel  = gui.QPushButton("new channel"    , self)
		self.button_save         = gui.QPushButton("save changes"   , self)
		self.button_discard      = gui.QPushButton("discard changes", self)
		self.cb_confirm_save     = gui.QCheckBox("confirm",self)
		self.cb_confirm_discard  = gui.QCheckBox("confirm",self)

		self.HBoxTopButtons  = gui.QHBoxLayout(); self.HBoxTopButtons.setSpacing(0)
		self.VBoxSaveDiscard = gui.QVBoxLayout(); self.VBoxSaveDiscard.setSpacing(0)
		self.VBoxConfirm     = gui.QVBoxLayout(); self.VBoxConfirm.setSpacing(0)
		self.HBoxBottom      = gui.QHBoxLayout(); self.HBoxBottom.setSpacing(0)
		self.VBoxMain        = gui.QVBoxLayout(); self.VBoxMain.setSpacing(0)

		self.HBoxTopButtons.addWidget(self.button_edit_channel)
		self.HBoxTopButtons.addWidget(self.button_new_channel)
		self.VBoxSaveDiscard.addWidget(self.button_save)
		self.VBoxSaveDiscard.addWidget(self.button_discard)
		self.VBoxConfirm.addWidget(self.cb_confirm_save)
		self.VBoxConfirm.addWidget(self.cb_confirm_discard)
		self.HBoxBottom.addLayout(self.VBoxSaveDiscard,2)
		self.HBoxBottom.addLayout(self.VBoxConfirm,1)

		self.VBoxMain.addLayout(self.HBoxTopButtons,0)
		self.VBoxMain.addLayout(self.HBoxBottom,0)
		self.VBoxMain.addStretch(1)
		self.setLayout(self.VBoxMain)

		self.set_editing_mode('viewing')

	def set_editing_mode(self,mode,send=True):
		if not (mode in ['viewing','editing','creating']):
			return
		
		self.mode = mode

		self.button_edit_channel.setEnabled( mode == 'viewing' )
		self.button_new_channel.setEnabled(  mode == 'viewing' )
		self.button_save.setEnabled(         mode != 'viewing' )
		self.button_discard.setEnabled(      mode != 'viewing' )
		self.cb_confirm_save.setEnabled(     mode != 'viewing' )
		self.cb_confirm_discard.setEnabled(  mode != 'viewing' )

class MainInterface(gui.QWidget):
	def __init__(self,parent,connection):
		super(MainInterface,self).__init__(parent)
		self.connection = connection
		self.vds        = connection.virtual_device_server

		self.HBoxMain = gui.QHBoxLayout()
		self.channel_selector   = ChannelSelectorWidget(self,connection)
		self.channel_descripive = ChannelDescriptiveInfoWidget(self)
		self.channel_device     = ChannelDeviceInfoWidget(self)
		self.controls           = ChannelModificationControlWidget(self)

		self.HBoxMain.addWidget(self.channel_selector  , 2)
		self.HBoxMain.addWidget(self.channel_descripive, 2)
		self.HBoxMain.addWidget(self.channel_device    , 2)
		self.HBoxMain.addWidget(self.controls          , 1)
		self.setLayout(self.HBoxMain)

		self.channel = None
		self.change_mode('viewing')

		self.channel_selector.ch_name.itemActivated.connect(self.load_channel)
		self.channel_selector.ch_id.itemActivated.connect(self.load_channel)

		self.controls.button_edit_channel.clicked.connect(self.start_editing_channel)
		self.controls.button_new_channel.clicked.connect(self.start_new_channel)

		self.controls.button_discard.clicked.connect(self.discard_changes)


	def load_channel(self,channel):
		"""Called upon activating an item in the channel list. Sends the channel to each component."""
		if self.mode == 'viewing':
			ID      = self.channel_selector.channels[self.channel_selector.ch_name.currentRow()][0]
			self.channel = ChannelInstance(*self.vds.list_channel_details(ID))
			self.channel_descripive.load_channel(self.channel)
			self.channel_device.load_channel(self.channel)
			# Note that mode is not changed by loading a channel

	def start_new_channel(self):
		pass
		# if self.mode == 'viewing':
		# 	self.channel_descripive.new_channel()
		# 	self.channel_device.new_channel()
		# 	self.change_mode('creating')

	def start_editing_channel(self):
		if self.mode == 'viewing':
			if not (self.channel is None):
				self.change_mode('editing')

	def change_mode(self,mode):
		if mode not in ['viewing','editing','creating']:
			return
		self.mode = mode
		self.channel_selector.set_editing_mode(mode)
		self.channel_descripive.set_editing_mode(mode)
		self.channel_device.set_editing_mode(mode)
		self.controls.set_editing_mode(mode)

	def discard_changes(self):
		if self.controls.cb_confirm_discard.isChecked():
			self.channel = None
			self.change_mode('viewing')
			self.channel_descripive.clear_fields()
			self.channel_device.clear_fields()
			self.controls.cb_confirm_discard.setChecked(False)
