zc.buildout recipe
============================

Introduction
------------
The recipe extension helps to download pinned eggs quickly. It uses python
multiprocessing module.

Installation
------------
Build with
python setup.py build install

add below configuration to buildout.cfg:

::

   [download-eggs-first]
   recipe = buildout.recipe.download
   pkgurl = ${pkgserver:fullurl}
   cache-folder = ${buildout:directory}/download-cache
   versions-files = ${buildout:directory}/versions/versions.cfg

Optinally we can pass threads, it is defaulted to 50
