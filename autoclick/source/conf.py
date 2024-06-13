# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
project = "ATC's Auto-Clicker"
copyright = '2024, AmandeTheCat'
author = 'AmandeTheCat'
release = '1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',  # Permet de générer la documentation automatique à partir des docstrings
    # Ajoutez d'autres extensions si nécessaire
]

templates_path = ['_templates']
exclude_patterns = []

# Ajoutez ici le chemin vers vos répertoires de templates et de fichiers statiques si nécessaire
html_static_path = ['_static']

# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'  # Changer le thème si nécessaire (ex: 'sphinx_rtd_theme')

# Ajoutez ici d'autres configurations spécifiques au thème HTML si nécessaire

# -- Path configuration ------------------------------------------------------
import os
import sys
sys.path.insert(0, os.path.abspath('.'))  # Ajoute le répertoire racine de votre projet

# -- Autodoc configuration ---------------------------------------------------
# Ajoutez ici des configurations spécifiques pour autodoc si nécessaire

# -- Extension configuration -------------------------------------------------
# Ajoutez ici des configurations spécifiques pour les extensions si nécessaire
