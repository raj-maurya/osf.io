import os
import glob
import mimetypes

from django.apps import AppConfig

from mako.lookup import TemplateLookup
from website import settings


def _is_image(filename):
    mtype, _ = mimetypes.guess_type(filename)
    return mtype and mtype.startswith('image')

NODE_SETTINGS_TEMPLATE_DEFAULT = os.path.join(
    settings.TEMPLATES_PATH,
    'project',
    'addon',
    'node_settings_default.mako',
)

USER_SETTINGS_TEMPLATE_DEFAULT = os.path.join(
    settings.TEMPLATES_PATH,
    'profile',
    'user_settings_default.mako',
)


class BaseAddonConfig(AppConfig):
    name = 'addons.base'
    label = 'addons_base'

    actions = tuple()
    user_settings = None
    node_settings = None
    node_settings_template = NODE_SETTINGS_TEMPLATE_DEFAULT
    user_settings_template = USER_SETTINGS_TEMPLATE_DEFAULT
    views = []
    added_default = []
    added_mandatory = []
    include_js = {}  # TODO: Deprecate these elsewhere and remove
    include_css = {}  # TODO: Deprecate these elsewhere and remove
    configs = []
    has_hgrid_files = False
    get_hgrid_data = None
    max_file_size = None
    accept_extensions = True

    def __init__(self, *args, **kwargs):
        ret = super(BaseAddonConfig, self).__init__(*args, **kwargs).__init__()
        # Build template lookup
        paths = [settings.TEMPLATES_PATH]
        if self.user_settings_template:
            paths.append(os.path.dirname(self.user_settings_template))
        if self.node_settings_template:
            paths.append(os.path.dirname(self.node_settings_template))
        template_dirs = list(
            set(
                [
                    path
                    for path in paths
                    if os.path.exists(path)
                ]
            )
        )
        if template_dirs:
            self.template_lookup = TemplateLookup(
                directories=template_dirs,
                default_filters=[
                    'unicode',  # default filter; must set explicitly when overriding
                    'temp_ampersand_fixer',
                    # FIXME: Temporary workaround for data stored in wrong format in DB. Unescape it before it gets re-escaped by Markupsafe. See [#OSF-4432]
                    'h',
                ],
                imports=[
                    'from website.util.sanitize import temp_ampersand_fixer',
                    # FIXME: Temporary workaround for data stored in wrong format in DB. Unescape it before it gets re-escaped by Markupsafe. See [#OSF-4432]
                ]
            )
        else:
            self.template_lookup = None
        return ret

    @property
    def full_name(self):
        raise NotImplementedError

    @property
    def short_name(self):
        raise NotImplementedError

    @property
    def icon(self):
        try:
            return self._icon
        except:
            static_path = os.path.join('website', 'addons', self.short_name, 'static')
            static_files = glob.glob(os.path.join(static_path, 'comicon.*'))
            image_files = [
                os.path.split(filename)[1]
                for filename in static_files
                if _is_image(filename)
            ]
            if len(image_files) == 1:
                self._icon = image_files[0]
            else:
                self._icon = None
            return self._icon

    @property
    def icon_url(self):
        return self._static_url(self.icon) if self.icon else None

    def _static_url(self, filename):
        """Build static URL for file; use the current addon if relative path,
        else the global static directory.

        :param str filename: Local path to file
        :return str: Static URL for file

        """
        if filename.startswith('/'):
            return filename
        return '/static/addons/{addon}/{filename}'.format(
            addon=self.short_name,
            filename=filename,
        )

    def to_json(self):
        return {
            'short_name': self.short_name,
            'full_name': self.full_name,
            'capabilities': self.short_name in settings.ADDON_CAPABILITIES,
            'addon_capabilities': settings.ADDON_CAPABILITIES.get(self.short_name),
            'icon': self.icon_url,
            'has_page': 'page' in self.views,
            'has_widget': 'widget' in self.views,
        }
