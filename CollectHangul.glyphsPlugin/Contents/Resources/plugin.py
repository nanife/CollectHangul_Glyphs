# encoding: utf-8
from __future__ import division, print_function, unicode_literals
###########################################################################################################
#
#	Collect Hangul plugin that print composed text in glyph view or select composed text in font view
#
###########################################################################################################

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
import traceback
import imp
import sys

LANGUAGES = {'Eng':0, 'Kor': 1}
defaultID = u'com.LineGap.CollectHangul'

class CollectHangul(GeneralPlugin):
	def settings(self):
		if Glyphs.defaults['%s.language' % defaultID] == 1:
			self.menuName = u'_한글 모으기'
		else:
			self.menuName = '_Collect Hangul'

		# Glyphs 2
		self.lang = LANGUAGES['Eng']
		langValue = Glyphs.defaults['%s.language' % defaultID] 
		if langValue in [0, 1]:
			self.lang = langValue
		self.numWindows = [0]

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
			if sys.version[0] == '3':
				import CollectHangulModule3 as CH3
				imp.reload(CH3)
				CH3.Run()
			else:	# Glyphs 2
				if 0 == len(Glyphs.fonts):
					strError = [u'❓ error ❓', u'❓ 오류 ❓'][self.lang]
					strMessage = ['There is no opened font!', u'활성화된 폰트 창이 없습니다!'][self.lang]
					Message(strError, strMessage)
					return
				if [0] != self.numWindows:
					strError = [u'❓ error ❓', u'❓ 오류 ❓'][self.lang]
					strMessage = ['The plugin window already opened!', u'플러그인 창이 이미 열려 있습니다!'][self.lang]
					return

				Glyphs.clearLog()
				import CollectHangulModule as CH

				reload(CH)
				CH.Run(self.numWindows, self.lang)
		except:
			print(traceback.format_exc())

	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
