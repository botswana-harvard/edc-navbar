# edc_navbar

Simple Navbar class for edc

### Installation

Include `edc_navbar.apps.AppConfig` in `INSTALLED_APPS`.

### Overiew

Navbars are declared in your apps `navbars.py` and will be autodiscovered by `edc_navbar` and stored in the  site global `site_navbars`.

By default, a basic navbar is added to the site global. For it to load you need to define the named urls for `home_url`, `administration_url` and `logout_url` in your main project `urls.py`. The named urls defined in the default navbar do not include a namespace.

For example, in the "main" project app `urls.py`:

    urlpatterns = [
        ...
        path('login', LoginView.as_view(), name='login_url'),
        path('logout', LogoutView.as_view(
            pattern_name='login_url'), name='logout_url'),
        path('admininistration/', AdministrationView.as_view(),
             name='administration_url'),
        path('', HomeView.as_view(manual_revision='1.0'), name='home_url'),
        ...
        ]

You can change the `default` navbar to another navbar by setting `settings.DEFAULT_NAVBAR` to the name of your custom navbar. You will need to declare and register your custom navbar manually. See `edc_navbar.navbars`. 

### Declaring and registering a navbar

A navbar is defined and registered to the site global in the `navbars.py` module of each app that needs a navbar.

An example `navbars.py`:

    from edc_navbar import NavbarItem, site_navbars, Navbar
    
    url_namespace = 'edc_pharmacy_dashboard'
    
    # instantiate a Navbar
    pharmacy_dashboard = Navbar(name='pharmacy_dashboard')
    
    # add items to the navbar
    pharmacy_dashboard.append_item(
        NavbarItem(
            name='prescribe',
            title='Prescribe',
            label='prescribe',
            glyphicon='glyphicon-edit',
            url_name=f'{url_namespace}:prescribe_listboard_url'))
    
    pharmacy_dashboard.append_item(
        NavbarItem(
            name='dispense',
            title='Dispense',
            label='dispense',
            glyphicon='glyphicon-share',
            url_name=f'{url_namespace}:dispense_listboard_url'))
    
    # register the navbar to the site
    site_navbars.register(pharmacy_dashboard)
 
### Accessing the navbar in your views

Next, add `NavbarViewMixin` to your views and set the navbar by name. The navbar will be rendered to string and added to the view context.
 
    ...
    from edc_navbar import NavbarViewMixin

    class HomeView(EdcBaseViewMixin, NavbarViewMixin, TemplateView):

        navbar_name = 'pharmacy_dashboard'
        navbar_selected_item = 'prescribe'


### Rendering Navbar items

The default template for `NavbarItem` is `navbar_item.html`. You can declare a custom template on the `NavbarItem`.
