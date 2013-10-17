#######################################################################
#
#    MyMetrix
#    Coded by iMaxxx (c) 2013
#    MOD by BiNiCKNiCH & arn354 & svox
#
#
#  This plugin is licensed under the Creative Commons
#  Attribution-NonCommercial-ShareAlike 3.0 Unported License.
#  To view a copy of this license, visit http://creativecommons.org/licenses/by-nc-sa/3.0/
#  or send a letter to Creative Commons, 559 Nathan Abbott Way, Stanford, California 94305, USA.
#
#  Alternatively, this plugin may be distributed and executed on hardware which
#  is licensed by Dream Multimedia GmbH.
#
#
#  This plugin is NOT free software. It is open source, you are allowed to
#  modify it (if you keep the license), but it may not be commercially
#  distributed other than under the conditions noted above.
#
#
#######################################################################

from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.ChoiceBox import ChoiceBox
from Screens.Console import Console
from Screens.Standby import TryQuitMainloop
from Components.ActionMap import ActionMap
from Components.AVSwitch import AVSwitch
from Components.config import config, configfile, ConfigYesNo, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigNumber, ConfigText, ConfigInteger
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.Language import language
from os import environ, listdir, remove, rename, system
from shutil import move
from skin import parseColor
from Components.Pixmap import Pixmap
from Components.Label import Label
import gettext
from enigma import ePicLoad
from Tools.Directories import fileExists, resolveFilename, SCOPE_LANGUAGE, SCOPE_PLUGINS

#############################################################

lang = language.getLanguage()
environ["LANGUAGE"] = lang[:2]
gettext.bindtextdomain("enigma2", resolveFilename(SCOPE_LANGUAGE))
gettext.textdomain("enigma2")
gettext.bindtextdomain("MyMetrixMOD", "%s%s" % (resolveFilename(SCOPE_PLUGINS), "Extensions/MyMetrixMOD/locale/"))

def _(txt):
	t = gettext.dgettext("MyMetrixMOD", txt)
	if t == txt:
		t = gettext.gettext(txt)
	return t

def translateBlock(block):
	for x in TranslationHelper:
		if block.__contains__(x[0]):
			block = block.replace(x[0], x[1])
	return block

#############################################################

# key name is equal to "help image" file name (example MyMetrixHD_MOD/lib/enigma2/python/Plugins/Extensions/MyMetrixMOD/images/channelsel-fontsize-20-thin.jpg)
channelselFontStyles = [
			{"key":"channelsel-fontsize-20","font":"Regular; 20", "height":"322"},
			{"key":"channelsel-fontsize-20-thin","font":"RegularLight; 20", "height":"322"},
			{"key":"channelsel-fontsize-22","font":"Regular; 22", "height":"315"},
			{"key":"channelsel-fontsize-22-thin","font":"RegularLight; 22", "height":"315"},
			{"key":"channelsel-fontsize-24","font":"Regular; 24", "height":"311"},
			{"key":"channelsel-fontsize-24-thin","font":"RegularLight; 24", "height":"311"}
			]

channelInfoFontSizes = [
			{"key":"channelInfo-fontsize-140","font":"Block; 140","y":"420"},
			{"key":"channelInfo-fontsize-120","font":"Block; 120","y":"437"},
			{"key":"channelInfo-fontsize-100","font":"Block; 100","y":"455"},
			{"key":"channelInfo-fontsize-80","font":"Block; 80","y":"474"},
			{"key":"channelInfo-fontsize-60","font":"Block; 60","y":"493"},
			{"key":"channelInfo-fontsize-40","font":"Block; 40","y":"511"}
			]

#############################################################

config.plugins.MyMetrixMOD = ConfigSubsection()
config.plugins.MetrixWeather = ConfigSubsection()

				#General
config.plugins.MyMetrixMOD.Image = ConfigSelection(default="main-custom-openatv", choices = [
				("main-custom-openatv", _("openATV")),
				("main-custom-openmips", _("openMips"))
				])
config.plugins.MyMetrixMOD.SkinColor = ConfigSelection(default="00149baf", choices = [
				("00F0A30A", _("Amber")),
				("00825A2C", _("Brown")),
				("000050EF", _("Cobalt")),
				("00911d10", _("Crimson")),
				("001BA1E2", _("Cyan")),
				("00a61d4d", _("Magenta")),
				("00A4C400", _("Lime")),
				("006A00FF", _("Indigo")),
				("0070ad11", _("Green")),
				("00008A00", _("Emerald")),
				("0076608A", _("Mauve")),
				("006D8764", _("Olive")),
				("00c3461b", _("Orange")),
				("00F472D0", _("Pink")),
				("00E51400", _("Red")),
				("007A3B3F", _("Sienna")),
				("00647687", _("Steel")),
				("00149baf", _("Teal")),
				("006c0aab", _("Violet")),
				("00bf9217", _("Yellow"))
				])
config.plugins.MyMetrixMOD.SkinColorProgress = ConfigSelection(default="skincolor-progess-none", choices = [
				("skincolor-progess-color", _("On")),
				("skincolor-progess-none", _("Off"))
				])
				#MetrixWeather
config.plugins.MetrixWeather.refreshInterval = ConfigNumber(default=10)
config.plugins.MetrixWeather.woeid = ConfigNumber(default=640161) #Location (visit metrixhd.info)
config.plugins.MetrixWeather.tempUnit = ConfigSelection(default="Celsius", choices = [
				("Celsius", _("Celsius")),
				("Fahrenheit", _("Fahrenheit"))
				])
				#InfoBar
config.plugins.MyMetrixMOD.InfobarWeatherWidget = ConfigSelection(default="infobar-weatherwidget-image", choices = [
				("infobar-weatherwidget-image", _("On")),
				("infobar-weatherwidget-none", _("Off"))
				])
config.plugins.MyMetrixMOD.InfobarResolutionInfo = ConfigSelection(default="infobar-resolutioninfo", choices = [
				("infobar-resolutioninfo", _("On")),
				("infobar-resolutioninfo-none", _("Off"))
				])
config.plugins.MyMetrixMOD.InfobarCryptInfo = ConfigSelection(default="infobar-cryptinfo-none", choices = [
				("infobar-cryptinfo", _("On")),
				("infobar-cryptinfo-none", _("Off"))
				])
config.plugins.MyMetrixMOD.InfobarShowChannelInfo = ConfigSelection(default="infobar-channelinfo-name", choices = [
				("infobar-channelinfo-number", _("Channelnumber")),
				("infobar-channelinfo-name", _("Channelname")),
				("infobar-channelinfo-number-name", _("Channelnumber and name")),
				("infobar-channelinfo-none", _("Off"))
				])
config.plugins.MyMetrixMOD.InfobarChannelInfoFontsize = ConfigSelection(default="channelInfo-fontsize-120", choices = [
				("channelInfo-fontsize-140", "140"),
				("channelInfo-fontsize-120", "120"),
				("channelInfo-fontsize-100", "100"),
				("channelInfo-fontsize-80", "80"),
				("channelInfo-fontsize-60", "60"),
				("channelInfo-fontsize-40", "40"),
				])
config.plugins.MyMetrixMOD.InfobarECMInfo = ConfigSelection(default="infobar-ecminfo-none", choices = [
				("infobar-ecminfo", _("On")),
				("infobar-ecminfo-none", _("Off"))
				])
config.plugins.MyMetrixMOD.InfobarSatPosition = ConfigSelection(default="infobar-satposition-none", choices = [
				("infobar-satposition", _("On")),
				("infobar-satposition-none", _("Off"))
				])
config.plugins.MyMetrixMOD.InfobarSNR = ConfigSelection(default="infobar-snr-none", choices = [
				("infobar-snr", _("On")),
				("infobar-snr-none", _("Off"))
				])
config.plugins.MyMetrixMOD.InfobarTunerInfo = ConfigSelection(default="infobar-tunerinfo-none", choices = [
				("infobar-tunerinfo-none", _("Off")),
				("infobar-tunerinfo-ab", _("2 Tuner")),
				("infobar-tunerinfo-abc", _("3 Tuner")),
				("infobar-tunerinfo-abcd", _("4 Tuner"))
				])
				#ChannelSelection
config.plugins.MyMetrixMOD.ChannelSelectionFontSize = ConfigSelection(default="channelsel-fontsize-20", choices = [
				("channelsel-fontsize-20", _("20 Regular")),
				("channelsel-fontsize-20-thin", _("20 Thin")),
				("channelsel-fontsize-22", _("22 Regular")),
				("channelsel-fontsize-22-thin", _("22 Thin")),
				("channelsel-fontsize-24", _("24 Regular")),
				("channelsel-fontsize-24-thin", _("24 Thin"))
				])
config.plugins.MyMetrixMOD.EPGSelectionStyle = ConfigSelection(default="epgselection-default", choices = [
				("epgselection-default", _("Default")),
				("epgselection-picon", _("Picon"))
				])
config.plugins.MyMetrixMOD.ButtonStyle = ConfigSelection(default="buttons-light", choices = [
				("buttons-light", _("Light")),
				("buttons-dark", _("Dark")),
				("buttons-darktrans", _("Dark Transparent"))
				])
#######################################################################

class MyMetrixMOD(ConfigListScreen, Screen):
	skin = """
  <screen name="MyMetrixMOD-Setup" position="0,0" size="1280,720" flags="wfNoBorder" backgroundColor="#90000000">
    <eLabel name="new eLabel" position="40,40" zPosition="-2" size="1200,640" backgroundColor="#20000000" transparent="0" />
    <eLabel font="Regular; 20" foregroundColor="unffffff" backgroundColor="#20000000" halign="left" position="77,645" size="250,33" text="Cancel" transparent="1" />
    <eLabel font="Regular; 20" foregroundColor="unffffff" backgroundColor="#20000000" halign="left" position="375,645" size="250,33" text="Save" transparent="1" />
    <eLabel font="Regular; 20" foregroundColor="unffffff" backgroundColor="#20000000" halign="left" position="682,645" size="250,33" text="Reboot" transparent="1" />
    <widget name="config" position="61,114" size="590,500" scrollbarMode="showOnDemand" transparent="1" />
    <eLabel position="60,55" size="348,50" text="MyMetrixMOD" font="Regular; 40" valign="center" transparent="1" backgroundColor="#20000000" />
    <eLabel position="343,58" size="349,50" text="Setup" foregroundColor="unffffff" font="Regular; 30" valign="center" backgroundColor="#20000000" transparent="1" halign="left" />
    <eLabel position="665,640" size="5,40" backgroundColor="#e5dd00" />
    <eLabel position="360,640" size="5,40" backgroundColor="#61e500" />
    <eLabel position="60,640" size="5,40" backgroundColor="#e61700" />
    <widget name="helperimage" position="669,112" size="550,500" zPosition="1" />
    <eLabel text="by iMaxxx. OpenPLI mod by IPMAN and Misenko" position="692,48" size="540,25" zPosition="1" font="Regular; 15" halign="right" valign="top" backgroundColor="#20000000" transparent="1" />
    <eLabel text="MOD by BiNiCKNiCH" position="692,70" size="540,25" zPosition="1" font="Regular; 15" halign="right" valign="top" backgroundColor="#20000000" transparent="1" />
  </screen>
"""

	def __init__(self, session, args = None, picPath = None):
		self.skin_lines = []
		Screen.__init__(self, session)
		self.session = session
		self.datei = "/usr/share/enigma2/MetrixHD_MOD/skin.xml"
		self.dateiTMP = self.datei + ".tmp"
		self.daten = "/usr/lib/enigma2/python/Plugins/Extensions/MyMetrixMOD/data/"
		self.komponente = "/usr/lib/enigma2/python/Plugins/Extensions/MyMetrixMOD/comp/"
		self.picPath = picPath
		self.Scale = AVSwitch().getFramebufferScale()
		self.PicLoad = ePicLoad()
		self["helperimage"] = Pixmap()
		list = []
		list.append(getConfigListEntry(_("MetrixImage"), config.plugins.MyMetrixMOD.Image))
		list.append(getConfigListEntry(_("MetrixColor"), config.plugins.MyMetrixMOD.SkinColor))
		list.append(getConfigListEntry(_("MetrixColor on Progressbar"), config.plugins.MyMetrixMOD.SkinColorProgress))
		list.append(getConfigListEntry(_("----------------------------- MetrixWeather  --------------------------------"), ))
		list.append(getConfigListEntry(_("MetrixWeather ID"), config.plugins.MetrixWeather.woeid))
		list.append(getConfigListEntry(_("Unit"), config.plugins.MetrixWeather.tempUnit))
		list.append(getConfigListEntry(_("Refresh Interval (min)"), config.plugins.MetrixWeather.refreshInterval))
		list.append(getConfigListEntry(_("-------------------------------- InfoBar ------------------------------------"), ))
		list.append(getConfigListEntry(_("Weather Widget"), config.plugins.MyMetrixMOD.InfobarWeatherWidget))
		list.append(getConfigListEntry(_("Channel info"), config.plugins.MyMetrixMOD.InfobarShowChannelInfo))
		list.append(getConfigListEntry(_("Channel info fontsize"), config.plugins.MyMetrixMOD.InfobarChannelInfoFontsize))
		list.append(getConfigListEntry(_("Show resolution info"), config.plugins.MyMetrixMOD.InfobarResolutionInfo))
		list.append(getConfigListEntry(_("Show crypt info"), config.plugins.MyMetrixMOD.InfobarCryptInfo))
		list.append(getConfigListEntry(_("Show ECM info"), config.plugins.MyMetrixMOD.InfobarECMInfo))
		list.append(getConfigListEntry(_("Show Sat Position"), config.plugins.MyMetrixMOD.InfobarSatPosition))
		list.append(getConfigListEntry(_("Show SNR"), config.plugins.MyMetrixMOD.InfobarSNR))
		list.append(getConfigListEntry(_("Show tuner info"), config.plugins.MyMetrixMOD.InfobarTunerInfo))
		list.append(getConfigListEntry(_("---------------------------- ChannelSelection -------------------------------"), ))
		list.append(getConfigListEntry(_("Extended Description Fontsize"), config.plugins.MyMetrixMOD.ChannelSelectionFontSize))
		list.append(getConfigListEntry(_("------------------------------ EPGSelection ---------------------------------"), ))
		list.append(getConfigListEntry(_("EPGSelection Style"), config.plugins.MyMetrixMOD.EPGSelectionStyle))
		list.append(getConfigListEntry(_("------------------------------- ButtonStyle ----------------------------------"), ))
		list.append(getConfigListEntry(_("Button Style"), config.plugins.MyMetrixMOD.ButtonStyle))

		ConfigListScreen.__init__(self, list)
		self["actions"] = ActionMap(["OkCancelActions","DirectionActions", "InputActions", "ColorActions"], {"left": self.keyLeft,"down": self.keyDown,"up": self.keyUp,"right": self.keyRight,"red": self.exit,"yellow": self.reboot, "blue": self.showInfo, "green": self.save,"cancel": self.exit}, -1)
		self.onLayoutFinish.append(self.UpdatePicture)

	def GetPicturePath(self):
		try:
			returnValue = self["config"].getCurrent()[1].value
			path = "/usr/lib/enigma2/python/Plugins/Extensions/MyMetrixMOD/images/" + returnValue + ".jpg"
			return path
		except:
			return "/usr/lib/enigma2/python/Plugins/Extensions/MyMetrixMOD/images/metrixweather.jpg"

	def UpdatePicture(self):
		self.PicLoad.PictureData.get().append(self.DecodePicture)
		self.onLayoutFinish.append(self.ShowPicture)

	def ShowPicture(self):
		self.PicLoad.setPara([self["helperimage"].instance.size().width(),self["helperimage"].instance.size().height(),self.Scale[0],self.Scale[1],0,1,"#002C2C39"])
		self.PicLoad.startDecode(self.GetPicturePath())

	def DecodePicture(self, PicInfo = ""):
		ptr = self.PicLoad.getData()
		self["helperimage"].instance.setPixmap(ptr)

	def keyLeft(self):
		ConfigListScreen.keyLeft(self)
		self.ShowPicture()

	def keyRight(self):
		ConfigListScreen.keyRight(self)
		self.ShowPicture()

	def keyDown(self):
		self["config"].instance.moveSelection(self["config"].instance.moveDown)
		self.ShowPicture()

	def keyUp(self):
		self["config"].instance.moveSelection(self["config"].instance.moveUp)
		self.ShowPicture()

	def reboot(self):
		restartbox = self.session.openWithCallback(self.restartGUI,MessageBox,_("Do you really want to reboot now?"), MessageBox.TYPE_YESNO)
		restartbox.setTitle(_("Restart GUI"))

	def showInfo(self):
		self.session.open(MessageBox, _("Information"), MessageBox.TYPE_INFO)

	def getDataByKey(self, list, key):
		for item in list:
			if item["key"] == key:
				return item
		return list[0]

	def getFontStyleData(self, key):
		return self.getDataByKey(channelselFontStyles, key)

	def getFontSizeData(self, key):
		return self.getDataByKey(channelInfoFontSizes, key)

	def save(self):
		for x in self["config"].list:
			if len(x) > 1:
					x[1].save()
			else:
					pass

		try:
			#global tag search and replace in all skin elements
			self.skinSearchAndReplace = []
			self.skinSearchAndReplace.append(["00149bae", config.plugins.MyMetrixMOD.SkinColor.value])
			self.skinSearchAndReplace.append(["buttons-light", config.plugins.MyMetrixMOD.ButtonStyle.value])

			if config.plugins.MyMetrixMOD.SkinColorProgress.value == 'skincolor-progess-color':
				self.skincolorprogresscolor = config.plugins.MyMetrixMOD.SkinColor.value
				self.pbar = ("p_bar_" + self.skincolorprogresscolor + ".png")
				self.skinSearchAndReplace.append(["p_bar.png", self.pbar])
				self.pbar2 = ("colors/" + self.skincolorprogresscolor + ".png")
				self.skinSearchAndReplace.append(["colors/00ffffff.png", self.pbar2])

			###Header XML
			self.appendSkinFile(self.daten + "header.xml")

			###InfoBar
			self.appendSkinFile(self.daten + "infobar-header.xml")
			#WeatherWidget
			self.appendSkinFile(self.daten + config.plugins.MyMetrixMOD.InfobarWeatherWidget.value + ".xml")

			#ChannelInfo
			fontSizeData = self.getFontSizeData(config.plugins.MyMetrixMOD.InfobarChannelInfoFontsize.value)
			self.appendSkinFile(self.daten + config.plugins.MyMetrixMOD.InfobarShowChannelInfo.value + ".xml", [["{font}", fontSizeData["font"]], ["{y}", fontSizeData["y"]]])

			#ResolutionInfo
			self.appendSkinFile(self.daten + config.plugins.MyMetrixMOD.InfobarResolutionInfo.value + ".xml")
			#CryptInfo
			self.appendSkinFile(self.daten + config.plugins.MyMetrixMOD.InfobarCryptInfo.value + ".xml")
			#ECMInfo
			self.appendSkinFile(self.daten + config.plugins.MyMetrixMOD.InfobarECMInfo.value + ".xml")
			#SatPosition
			self.appendSkinFile(self.daten + config.plugins.MyMetrixMOD.InfobarSatPosition.value + ".xml")
			#SNR
			self.appendSkinFile(self.daten + config.plugins.MyMetrixMOD.InfobarSNR.value + ".xml")
			#TunerInfo
			self.appendSkinFile(self.daten + config.plugins.MyMetrixMOD.InfobarTunerInfo.value + ".xml")
			#Footer
			self.appendSkinFile(self.daten + "screen-footer.xml")

			###ChannelSelection
			self.appendSkinFile(self.daten + "channelsel-header.xml")

			#FontStyle
			fontStyleData = self.getFontStyleData(config.plugins.MyMetrixMOD.ChannelSelectionFontSize.value)
			self.appendSkinFile(self.daten + "channelsel-fontsize.xml", [["{font}", fontStyleData["font"]], ["{height}", fontStyleData["height"]]])

			#Footer
			self.appendSkinFile(self.daten + "screen-footer.xml")

			###EPGSelection
			self.appendSkinFile(self.daten + config.plugins.MyMetrixMOD.EPGSelectionStyle.value + ".xml")

			###Main XML
			self.appendSkinFile(self.daten + "main.xml")

			###custom-main XML
			self.appendSkinFile(self.daten + config.plugins.MyMetrixMOD.Image.value + ".xml")

			xFile = open(self.dateiTMP, "w")
			for xx in self.skin_lines:
				xFile.writelines(xx)
			xFile.close()

			move(self.dateiTMP, self.datei)

			#system('rm -rf ' + self.dateiTMP)
		except:
			self.session.open(MessageBox, _("Error creating Skin!"), MessageBox.TYPE_ERROR)

		configfile.save()
		restartbox = self.session.openWithCallback(self.restartGUI,MessageBox,_("GUI needs a restart to apply a new skin.\nDo you want to Restart the GUI now?"), MessageBox.TYPE_YESNO)
		restartbox.setTitle(_("Restart GUI"))

	def appendSkinFile(self, appendFileName, skinPartSearchAndReplace=None):
		"""
		add skin file to main skin content

		appendFileName:
		 xml skin-part to add

		skinPartSearchAndReplace:
		 (optional) a list of search and replace arrays. first element, search, second for replace
		"""
		skFile = open(appendFileName, "r")
		file_lines = skFile.readlines()
		skFile.close()

		tmpSearchAndReplace = []

		if skinPartSearchAndReplace is not None:
			tmpSearchAndReplace = self.skinSearchAndReplace + skinPartSearchAndReplace
		else:
			tmpSearchAndReplace = self.skinSearchAndReplace

		for skinLine in file_lines:
			for item in tmpSearchAndReplace:
				skinLine = skinLine.replace(item[0], item[1])
			self.skin_lines.append(skinLine)

	def restartGUI(self, answer):
		if answer is True:
			configfile.save()
			self.session.open(TryQuitMainloop, 3)
		else:
			self.close()

	def exit(self):
		for x in self["config"].list:
			if len(x) > 1:
					x[1].cancel()
			else:
					pass
		self.close()

#############################################################

def main(session, **kwargs):
	session.open(MyMetrixMOD,"/usr/lib/enigma2/python/Plugins/Extensions/MyMetrixMOD/images/metrixcolors.jpg")

def Plugins(**kwargs):
	return PluginDescriptor(name="MyMetrixMOD", description=_("Configuration tool for MetrixHD_MOD"), where = PluginDescriptor.WHERE_PLUGINMENU, icon="plugin.png", fnc=main)