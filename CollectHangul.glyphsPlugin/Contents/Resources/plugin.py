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

import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
import traceback

class CollectHangul(GeneralPlugin):
	def settings(self):
		# self.menuName = Glyphs.localize({'en': u'_Collect Hangul', 'ko': u'_한글 모으기'})
		self.menuName = u'_한글 모으기'
		self.numWindows = [0]

	def start(self):
		try: 
			targetMenu = FILTER_MENU
			separator = NSMenuItem.separatorItem()
			newMenuItem = NSMenuItem(self.menuName, self.showWindow)
			Glyphs.menu[targetMenu].insert(2, newMenuItem)
		except:
			mainMenu = Glyphs.mainMenu()
			s = objc.selector(self.showWindow, signature='v@:@')
			newMenuItem = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(self.menuName, s, "")
			newMenuItem.setTarget_(self)
			mainMenu.itemWithTag_(11).submenu().insertItem_atIndex_(newMenuItem, 2)#addItem_(newMenuItem)
			print traceback.format_exc()

	def showWindow(self, sender):
		""" Do something like show a window"""
 		try:
 			if 0 == len(Glyphs.fonts):
				Message(u'❓ 오류 ❓', u'활성화된 폰트 창이 없습니다!')
				return
 			if self.numWindows[0] != 0:
 				return

 			Glyphs.clearLog()
 			import Common as CM
 			reload(CM)
			cm = CM.Common()

 			value = cm.gL()
 			if value[0] in [0, 1] and 0 <= value[1]:
		 		import CollectHangulModule as CH
		 		reload(CH)
	 			w = CH.Collect(self.numWindows, value[0])
	 			w.run()
	 		else:
	 			Message(u'❓ 오류 ❓', u'사용 기간이 만료되었거나 인증 정보가 없습니다.\n등록 후 사용 가능합니다!')
		 		import CollectHangulModule as CH
		 		reload(CH)
		 		strChallenge = cm.gC()
	 			wAuth = CH.Authorize(strChallenge, self.numWindows)
	 			wAuth.w.center()
	 			wAuth.w.open()
 		except:
 			print traceback.format_exc()

	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
