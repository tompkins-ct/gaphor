"""
This plugin extends Gaphor with XMI alignment actions.
"""

from zope import interface, component
from gaphor.core import inject, transactional, action, build_action_group
from gaphor.interfaces import IService, IActionProvider
from gaphor.ui.interfaces import IDiagramSelectionChange


class Alignment(object):

    interface.implements(IService, IActionProvider)

    gui_manager = inject('gui_manager')

    menu_xml = """
      <ui>
        <menubar action="mainwindow">
          <menu action="diagram">
            <placeholder name="ternary">
		<separator />
		<menuitem action="align-left" />
		<menuitem action="align-center" />
		<menuitem action="align-right" />
		<separator />
		<menuitem action="align-top" />
		<menuitem action="align-middle" />
		<menuitem action="align-bottom" />
            </placeholder>
          </menu>
        </menubar>
      </ui>"""

    def __init__(self):
        self.action_group = build_action_group(self)
        self._last_update = None

    def init(self, app):
	self._app = app
        app.register_handler(self.update)
    
    def shutdown(self):
        self._app.unregister_handler(self.update)

    @component.adapter(IDiagramSelectionChange)
    def update(self, event=None):
        self._last_update = event
        sensitive = event and len(event.selected_items) > 1
	self.action_group.get_action('align-left').set_sensitive(sensitive)
	self.action_group.get_action('align-center').set_sensitive(sensitive)
	self.action_group.get_action('align-right').set_sensitive(sensitive)
	self.action_group.get_action('align-top').set_sensitive(sensitive)
	self.action_group.get_action('align-middle').set_sensitive(sensitive)
	self.action_group.get_action('align-bottom').set_sensitive(sensitive)

    def get_items(self):
        return (self._last_update and self._last_update.selected_items) or []
            
    def getXCoordsLeft(self, items):
        return [item.matrix[4] for item in items]
	
    def getXCoordsRight(self, items):
        return [item.matrix[4] + item.width for item in items]

    def getYCoordsTop(self, items):
        return [item.matrix[5] for item in items]
	
    def getYCoordsBottom(self, items):
        return [item.matrix[5] + item.height for item in items]

    @action(name='align-left', label='Left',
            tooltip="Vertically align diagram elements on the left")
    @transactional
    def align_left(self):
        items = self.get_items()
        target_x=min(self.getXCoordsLeft(items))
        for item in items:
            x = target_x - item.matrix[4]
            item.matrix.translate(x,0)
            item.request_update()
	
    @action(name='align-center', label='Center',
            tooltip="Vertically align diagram elements on their centers")
    @transactional
    def align_center(self):
        items = self.get_items()
        min_x=min(self.getXCoordsLeft(items))
	max_x=max(self.getXCoordsRight(items))
	center_x = max_x - min_x
        for item in items:
            x = center_x - (item.width / 2) - item.matrix[4]
            item.matrix.translate(x,0)
            item.request_update()
	
    @action(name='align-right', label='Right',
            tooltip="Vertically align diagram elements on the right")
    @transactional
    def align_right(self):
        items = self.get_items()
        target_x=max(self.getXCoordsRight(items))
        for item in items:
            x = target_x - item.width - item.matrix[4]
            item.matrix.translate(x,0)
            item.request_update()

    @action(name='align-top', label='Top',
            tooltip="Horizontally align diagram elements on their tops")
    @transactional
    def align_top(self):
        items = self.get_items()
        target_y = min(self.getYCoordsTop(items))
        for item in items:
            y = target_y - item.matrix[5]
            item.matrix.translate(0,y)
            item.request_update()
	    
    @action(name='align-middle', label='Middle',
            tooltip="Horizontally align diagram elements on their middles")
    @transactional
    def align_middle(self):
        items = self.get_items()
        min_y = min(self.getYCoordsTop(items))
	max_y = max(self.getYCoordsBottom(items))
	middle_y = max_y - min_y
        for item in items:
	    y = middle_y - (item.height / 2) - item.matrix[5]
            item.matrix.translate(0,y)
            item.request_update()
	    
    @action(name='align-bottom', label='Bottom',
            tooltip="Horizontally align diagram elements on their bottoms")
    @transactional
    def align_bottom(self):
        items = self.get_items()
        target_y = min(self.getYCoordsBottom(items))
        for item in items:
            y = target_y - item.height - item.matrix[5]
            item.matrix.translate(0,y)
            item.request_update()
	


# vim:sw=4:et:ai
