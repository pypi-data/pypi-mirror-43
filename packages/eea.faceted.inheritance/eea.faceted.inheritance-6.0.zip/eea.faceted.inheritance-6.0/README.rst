=======================
EEA Faceted Inheritance
=======================
.. image:: https://ci.eionet.europa.eu/buildStatus/icon?job=eea/eea.faceted.inheritance/develop
  :target: https://ci.eionet.europa.eu/job/eea/job/eea.faceted.inheritance/job/develop/display/redirect
  :alt: Develop
.. image:: https://ci.eionet.europa.eu/buildStatus/icon?job=eea/eea.faceted.inheritance/master
  :target: https://ci.eionet.europa.eu/job/eea/job/eea.faceted.inheritance/job/master/display/redirect
  :alt: Master

An extension to be used within eea.facetednavigation in order to allow objects
to inherit faceted configuration from another faceted navigable object. This way
one can define a global faceted navigable folder and reuse this configuration
for multiple heritors.


Install
=======

* Add **eea.faceted.inheritance** to your **eggs** section in your buildout and
  re-run buildout::

    [buildout]
    eggs +=
      eea.faceted.inheritance

* You can download a sample buildout from:

  - https://github.com/eea/eea.faceted.inheritance/tree/master/buildouts/plone4
  - https://github.com/eea/eea.faceted.inheritance/tree/master/buildouts/plone5

* Or via docker::

    $ docker run --rm -p 8080:8080 -e ADDONS="eea.faceted.inheritance" plone

* Install **EEA Faceted Inheritance** within **Site Setup > Add-ons**


Getting started
===============

* Go to your working space and add a **Folder** and within **Actions** menu
  click on **Enable Faceted Inheritance**.
* See more on `EEA Faceted Navigation`_


Source code
===========

Latest source code in EEA GitHub:

* https://github.com/eea/eea.faceted.inheritance


Copyright and license
=====================
The Initial Owner of the Original Code is European Environment Agency (EEA).
All Rights Reserved.

The EEA Faceted Inheritance (the Original Code) is free software;
you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation;
either version 2 of the License, or (at your option) any later
version.

Contributor(s): Alin Voinea (Eau de Web),
                Antonio De Marinis (European Environment Agency),

More details under docs/License.txt

Funding
=======

EEA_ - European Enviroment Agency (EU)

.. _EEA: https://www.eea.europa.eu/
.. _`EEA Faceted Navigation`: https://github.com/eea/eea.facetednavigation
