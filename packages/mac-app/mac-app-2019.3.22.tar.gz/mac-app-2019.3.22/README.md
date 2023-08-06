<!--
https://pypi.org/project/readme-generator/
-->

[![](https://img.shields.io/badge/OS-MacOS-blue.svg?longCache=True)]()
[![](https://img.shields.io/pypi/pyversions/mac-app.svg?longCache=True)](https://pypi.org/project/mac-app/)

#### Installation
```bash
$ [sudo] pip install mac-app
```

#### Classes
class|`__doc__`
-|-
`mac_app.App` |Mac app generator

#### Examples
create app from python file
```python
>>> mac_app.App(app_script="file.py", app_name="name").appify().mkalias("~/name.app")
```

create app from class
```python
>>> import mac_app
>>> class MyApp(mac_app.App):
        def run(self):
            pass

    if __name__ == "__main__":
        MyApp().run()
```

```python
>>> MyApp().appify().mkalias("~/MyApp.app")
```

<p align="center">
    <a href="https://pypi.org/project/readme-generator/">readme-generator</a>
</p>