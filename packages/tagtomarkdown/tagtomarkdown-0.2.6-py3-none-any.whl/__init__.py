# Christians first attempt to make a Python3 package
import pkg_resources

class ToolSet(object):
  pass

try_pack = ToolSet()
#named_objects =  {}
for ep in pkg_resources.iter_entry_points(group='markdown.extensions'):
  #print('ep.name: %s' % ep.name)
  setattr(try_pack, ep.name, ep.load())
  #print('ep.name: %s, ep.load(): %s' % (ep.name, ep.load()))
  #named_objects.update({ep.name, ep.load()})
