import sys
import copy

from django.apps import apps as django_apps
from django.core.management.color import color_style
from django.utils.module_loading import module_has_submodule
from importlib import import_module

from .navbar import NavbarError


class AlreadyRegistered(Exception):
    pass


class NavbarCollection:

    """A class to contain a dictionary of navbars. See Navbar.
    """

    name = 'default'

    def __init__(self):
        self.registry = {}

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    def register(self, navbar=None):
        if navbar.name not in self.registry:
            self.registry.update({navbar.name: navbar})
        else:
            raise AlreadyRegistered(
                f'Navbar with name {navbar.name} is already registered.')

    def context(self, name=None, selected_item=None):
        """Returns the named navbar in the collection as context.
        """
        return dict(
            navbar_item_selected=selected_item,
            navbar=self.get_navbar(
                name=name, selected_item=selected_item),
            navbar_name=name)

    def get_navbar(self, name=None, selected_item=None):
        """Returns a selected navbar in the collection.
        """
        # does navbar exist?
        try:
            navbar = self.registry[name]
        except KeyError:
            raise NavbarError(
                f'Navbar \'{name}\' does not exist. Expected one of '
                f'{list(self.registry.keys())}. See {repr(self)}.')
        else:
            # does navbar have items?
            if not [item.name for item in navbar]:
                raise NavbarError(
                    f'Navbar \'{navbar.name}\' has no items. Expected \'{selected_item}\'. See {repr(self)}')
            # does selected item exist?
            if selected_item:
                if selected_item not in [navbar_item.name for navbar_item in navbar]:
                    navbar_item_names = [item.name for item in navbar]
                    raise NavbarError(
                        f'Navbar item name does not exist. Got \'{selected_item}\'. '
                        f'Expected one of {navbar_item_names}. See navbar \'{navbar.name}\'.')
        return navbar

    def autodiscover(self, module_name=None, verbose=True):
        module_name = module_name or 'navbars'
        writer = sys.stdout.write if verbose else lambda x: x
        style = color_style()
        writer(' * checking for site {} ...\n'.format(module_name))
        for app in django_apps.app_configs:
            writer(' * searching {}           \r'.format(app))
            try:
                mod = import_module(app)
                try:
                    before_import_registry = copy.copy(site_navbars.registry)
                    import_module('{}.{}'.format(app, module_name))
                    writer(
                        ' * registered navbars \'{}\' from \'{}\'\n'.format(
                            module_name, app))
                except NavbarError as e:
                    writer('   - loading {}.navbars ... '.format(app))
                    writer(style.ERROR('ERROR! {}\n'.format(str(e))))
                except ImportError as e:
                    site_navbars.registry = before_import_registry
                    if module_has_submodule(mod, module_name):
                        raise NavbarError(str(e))
            except ImportError:
                pass
            except Exception as e:
                raise NavbarError(
                    f'An {e.__class__.__name__} was raised when loading navbars. '
                    f'Got {e} See {app}.navbars')


site_navbars = NavbarCollection()

# class Navbar:
#
#     def __init__(self, selected_item=None, navbar_name=None):
#         self._navbars = {}
#         self.selected_item = selected_item
#         self.navbar_name = navbar_name
#         if self.selected_item:
#             if self.selected_item not in [navbar_item.name for navbar_item in self.navbar]:
#                 navbar_item_names = [item.name for item in self.navbar]
#                 raise NavbarError(
#                     f'Navbar item name does not exist. Got \'{self.navbar_item_selected}\'. '
#                     f'Expected one of {navbar_item_names}. See navbar \'{self.navbar_name}\'.')
#
#     @property
#     def context(self, name=None, selected_item=None):
#         return dict(
#             navbar_item_selected=self.selected_item,
#             navbar=self.navbar,
#             navbar_name=self.navbar_name)
#
#     @property
#     def navbar(self):
#         return navbars.get(self.navbar_name)
#
#     def add(self, name=None, navbar_items=None):
#         self.navbars.update({name: navbar_items})
#
#
# navbars = Navbars.update(
#     {'edc_base': Navbar(selected_item='home', navbar_name='default')})
