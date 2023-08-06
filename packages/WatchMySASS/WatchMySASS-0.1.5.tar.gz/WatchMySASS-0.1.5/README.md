# WatchMySASS
_(Okay fine, it's really SCSS... but that's not as catchy, is it?)_

WatchMySASS bridges the gap between SCSS and HTML `<style>` tags. Since SCSS doesn't know how to compile HTML files, WatchMySASS allows you to compile style tags by using the attributes `type="text/scss"` or `lang="scss"`.

***

# Installation
WatchMySass is available on PyPi for download:
https://pypi.org/project/WatchMySASS/

Install WatchMySASS from the command line via pip:
```
pip install WatchMySASS
```
  
***

# Useage
WatchMySASS can be called from anywhere in the command line and, just like SCSS, takes the files/paths to compile as an argument. 
```
WatchMySASS index.html subdirectory/file.html
```

If no arguments are passed, WatchMySASS assumes the current working directory.
```
WatchMySASS
```


WatchMySASS also has a few options:

### --watch [-w] 
Continuously watch directory(s)/file(s) for changes.
```
WatchMySASS frequently-updated.html --watch
```

### --uncompressed [-u]
By default, WatchMySASS minifies the CSS output. Passing the `-u` flag overrides this feature.
```
WatchMySASS uncompressed1.html uncompressed2.html --uncompressed
```

### --destructive [-d]
By default, WatchMySASS saves compiled HTML files as `<filename>-compiled.html`. Pass the `-u` flag to save changes directly to the original HTML file.
```
WatchMySASS destructive.html --destructive
```

***

### Notes:
- WatchMySASS recursively searches directories to compile. There is currently no option for a "shallow" search.
- The `-u` flag is tempermental and doesn't always work. If you need clean, readable CSS you can always beautify your code in your text editor after compilation, and re-save.
