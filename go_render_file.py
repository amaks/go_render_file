import os, sublime, sublime_plugin

class GoRenderFileCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    region    = self.view.sel()[0]
    line      = self.view.line(region)
    line_text = self.view.substr(line)

    if '"' in line_text:
      file_name = line_text.split('"')[1]
    else:
      file_name = line_text.split('\'')[1]

    if len(file_name) > 0:
      source          = self.view.file_name()
      source_path     = os.path.dirname(source)
      rails_view_path = os.path.dirname(source_path)

      if '/' in file_name:
        split_file_name = file_name.split('/')

        if len(split_file_name) == 2:
          new_file_name = split_file_name[0] + '/_' + split_file_name[1]
        else:
          new_file_name = split_file_name[0] + '/' + split_file_name[1] + '/_' + split_file_name[2]

        if split_file_name[0] in rails_view_path:
          file_path = rails_view_path.replace(split_file_name[0], '') + '/' + new_file_name
        else:
          if rails_view_path.split('/')[-2] == 'views':
            file_path = rails_view_path.replace(rails_view_path.split('/')[-1], '') + '/' + new_file_name
          else:
            file_path = rails_view_path + '/' + new_file_name
      else:
        new_file_name = file_name
        file_path = source_path + '/_' + new_file_name

      extensions = ['haml', 'html.erb', 'html.slim']

      for i in extensions:
        if os.path.exists(file_path + '.' + i):
          self.view.window().open_file(file_path + '.' + i)