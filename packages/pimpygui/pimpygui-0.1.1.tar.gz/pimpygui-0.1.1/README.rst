pimpygui
========

*pimpygui* is a tool that demonstrates some functions of the *pimpy* package. It installs the command line tool
``pimpy_gallery``, which is a GUI for applying image processing functions.

Installing
----------

Install from pip::

    python -m pip install pimpygui

Usage:
------

If binaries of installed python packages are added to the PATH, you can call ``pimpy_gallery`` directly from the shell::

    pimpy_gallery

Otherwise, it can be invoked using python::

    python -m pimpygui.gallery

Overview:
---------

The ``pimpy_gallery`` GUI contains the following effects:

* *Smooth:* Applies a gaussian filter which blurs the image.
* *Main colors:* Reduces the image to a given number of colors. The colors can be set by the user or guessed
  algorithmically using k-means clustering.
* *Edges:* Finds all edges of the given image. It adds an edge between two neighboring pixels if their color values are
  different. You should apply the *main colors* effect before creating the edge image, since an edge is inserted even if
  the colors are visually identical but slightly different.
* *Paint by number:* Applies the *edge* effect and additionally inserts labels in the image segments. This can be used
  to create prototype images for the popular *paint by number* artworks. Usually, you first need to apply the *smooth*
  and *main colors* effects, since images are often too noisy for useful results.
