# encoding: utf-8

###########################################################################################################
#
#
#	General Plugin
#
#	Read the docs:
#	https://github.com/schriftgestalt/GlyphsSDK/tree/master/Python%20Templates/General%20Plugin
#
#
###########################################################################################################

from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
import traceback

defaultID = u'com.LineGap.CollectHangul'

class CollectHangul(GeneralPlugin):
	@objc.python_method
	def settings(self):
		self.menuName = Glyphs.localize({'en': '_Collect Hangul',
										 'ko': '_한글 모으기'})
		self.numWindows = [0]

	@objc.python_method
	def start(self):
		try: 
			targetMenu = FILTER_MENU
			newMenuItem = NSMenuItem(self.menuName, self.showWindow_)
			Glyphs.menu[targetMenu].insert(2, newMenuItem)
		except:
			mainMenu = Glyphs.mainMenu()
			s = objc.selector(self.showWindow_, signature='v@:@')
			newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(self.menuName, s, "")
			newMenuItem.setTarget_(self)
			mainMenu.itemWithTag_(11).submenu().insertItem_atIndex_(newMenuItem, 2)#addItem_(newMenuItem)
			print(traceback.format_exc())

	def showWindow_(self, sender):
		""" Do something like show a window"""
		try:
			if 0 == len(Glyphs.fonts):
				strError = Glyphs.localize({'en': '❓ error ❓',
											'ko': '❓ 오류 ❓'})
									
				strMessage = Glyphs.localize({'en': 'There is no opened font!',
											  'ko': '활성화된 폰트 창이 없습니다!'})
				Message(strError, strMessage)
				return
			if [0] != self.numWindows:
				strError = Glyphs.localize({'en': '❓ error ❓',
											'ko': '❓ 오류 ❓'})
				strMessage = Glyphs.localize({'en': 'The plugin window already opened!', 
											  'ko': '플러그인 창이 이미 열려 있습니다!'})
				return

			Glyphs.clearLog()
			import CollectHangulModule as CH

			reload(CH)
			CH.Run(self.numWindows, self.lang)

		except:
			print(traceback.format_exc())

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
