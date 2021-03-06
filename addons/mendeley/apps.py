from addons.base.apps import BaseAddonConfig


class MendeleyAddonConfig(BaseAddonConfig):

    name = 'addons.mendeley'
    label = 'addons_mendeley'
    full_name = 'Mendeley'
    short_name = 'mendeley'
    configs = ['accounts', 'node']
    views = ['widget']
    categories = ['citations']
    has_hgrid_files = False

    FOLDER_SELECTED = 'mendeley_folder_selected'
    NODE_AUTHORIZED = 'mendeley_node_authorized'
    NODE_DEAUTHORIZED = 'mendeley_node_deauthorized'

    actions = (
        FOLDER_SELECTED,
        NODE_AUTHORIZED,
        NODE_DEAUTHORIZED)

    @property
    def user_settings(self):
        return self.get_model('UserSettings')

    @property
    def node_settings(self):
        return self.get_model('NodeSettings')
