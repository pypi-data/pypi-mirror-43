========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - | |travis| |dependabot| |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |travis| image:: https://travis-ci.org/danclaudiupop/selenium-elements.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/danclaudiupop/selenium-elements

.. |dependabot| image:: https://api.dependabot.com/badges/status?host=github&repo=danclaudiupop/selenium-elements
   :alt: Dependabot
   :target: https://dependabot.com

.. |codecov| image:: https://codecov.io/github/danclaudiupop/selenium-elements/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/danclaudiupop/selenium-elements

.. |version| image:: https://img.shields.io/pypi/v/selenium-elements.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/selenium-elements

.. |commits-since| image:: https://img.shields.io/github/commits-since/danclaudiupop/selenium-elements/v0.0.1.svg
    :alt: Commits since latest release
    :target: https://github.com/danclaudiupop/selenium-elements/compare/v0.0.1...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/selenium-elements.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/selenium-elements

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/selenium-elements.svg
    :alt: Supported versions
    :target: https://pypi.org/project/selenium-elements

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/selenium-elements.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/selenium-elements


.. end-badges

Page object model made easy.

* Free software: BSD 2-Clause License

Installation
============

::

    pip install selenium-elements

Documentation
=============


To use the project:

.. code-block:: python

    import pytest
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    from src.page import Region, Page
    from .elements import PageElement, PageElements
    from .validators import title_matches, url_contains
    from .elements import RegionElements, RegionElement


    class Show(Page):
        path = '/show/{show_slug}/'
        page_title_pattern = '^[A-az-Z] | PBS$'


    class PromoShowRegion(Region):
        title_element = PageElement(By.CLASS_NAME, 'carousel--show-strip__image-link')

        def open(self):
            self.title_element.click()
            return Show(driver=self.driver, base_url=self.base_url, visit=False)

        def title(self):
            return self.title_element.get_attribute('data-gtm-label')


    class Home(Page):
        path = '/'
        load_timeout = 30
        validators = [
            title_matches('^PBS: Public Broadcasting Service$'),
            url_contains('pbs.org/'),
        ]

        promo_show_elements = PageElements(By.CLASS_NAME, 'show-promo')
        promo_shows = RegionElements(
            region_class=PromoShowRegion, root_element=promo_show_elements
        )


    @pytest.fixture
    def driver():
        driver = webdriver.Chrome()
        yield driver
        driver.quit()


    def test_foo(driver):
        home = Home(driver=driver, base_url='https://www.pbs.org')
        breakpoint()
        for show in home.promo_shows:
            print(show.title())
        # show = home.promo_shows[0].open()
        # show_page = Show(driver, base_url='https://www.pbs.org', show_slug='frontline')
        breakpoint()
        assert True


