VERSION_PATH = 'client/VERSION'

version_parts = open(VERSION_PATH).read().split('.')
version_parts[-1] = str(int(version_parts[-1]) +1)
open(VERSION_PATH, 'w').write(".".join(version_parts))
