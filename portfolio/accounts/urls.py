from django.conf.urls import patterns, url


urlpatterns = patterns(
    '',
    url(r'^login/$', 'django.contrib.auth.views.login',
        {
            'template_name': 'login.html',
            'redirect_field_name': 'next'
        },
        name='accounts.login'),

    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {
            'next_page': 'portfolio.home'
        },
        name='accounts.logout'),
)
