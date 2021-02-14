import sys
from resources.lib.addon_paths_manager import AddonPathManager

if __name__ == '__main__':
    widget_path = sys.listitem.getPath()
    path_label = sys.listitem.getLabel()
    apm = AddonPathManager()
    apm.addPath(widget_path, path_label)
