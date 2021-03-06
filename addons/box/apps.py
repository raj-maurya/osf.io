from addons.base.apps import BaseAddonConfig

from website.addons.box.views import box_root_folder

class BoxAddonConfig(BaseAddonConfig):

    name = 'addons.box'
    label = 'addons_box'
    full_name = 'Box'
    short_name = 'box'
    configs = ['accounts', 'node']
    has_hgrid_files = True
    max_file_size = 250  # MB

    @property
    def get_hgrid_data(self):
        return box_root_folder

    FOLDER_SELECTED = 'box_folder_selected'
    NODE_AUTHORIZED = 'box_node_authorized'
    NODE_DEAUTHORIZED = 'box_node_deauthorized'

    actions = (FOLDER_SELECTED, NODE_AUTHORIZED, NODE_DEAUTHORIZED, )

    @property
    def user_settings(self):
        return self.get_model('UserSettings')

    @property
    def node_settings(self):
        return self.get_model('NodeSettings')
