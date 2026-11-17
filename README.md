# plugins-themes
Themes other than the GTK/Windows theme which aren't specific to a particular OS or Windowing system.

Darkness includes an isometric cube computer icon and matching charcoal folder
icons for ordinary folders, home, applications, GNUstep system directories,
documents, downloads, libraries, pictures, music, and videos. The transparent
48×48 TIFF assets use GNUstep's standard image names in
`Darkness.theme/Resources/ThemeImages` and are installed with the theme.

Editable SVG sources live in `Darkness.theme/Resources/Artwork`. To regenerate the sources and
TIFFs after changing the shared artwork in `Tools/generate-darkness-icons.py`,
install CairoSVG and Pillow and run:

```sh
python3 Tools/generate-darkness-icons.py
```

These tools are only needed to regenerate icons; the theme uses the committed
TIFF files directly.
