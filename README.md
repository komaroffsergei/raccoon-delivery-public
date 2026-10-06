# Raccoon Delivery
## Based at KivyMD framework (python)
### MUST HAVE docs for kivymd developer
   1) [Really easy tutorial for beginners about Kivy Framework (YouTube) ](https://www.youtube.com/watch?v=VIy3hktYKwE&ab_channel=%D0%A5%D0%B0%D1%83%D0%B4%D0%B8%D0%A5%D0%BE%E2%84%A2-%D0%9F%D1%80%D0%BE%D1%81%D1%82%D0%BE%D0%BE%D0%BC%D0%B8%D1%80%D0%B5IT%21)
   2) [KivyMD framework (Kivy with Material Designer by Google)](https://github.com/kivymd/KivyMD)
   3) [KivyMD official documentation fot screens, themes, components ported to KivyMD from Material Design ](https://kivymd.readthedocs.io/en/latest/)
## Install:
```sh
python -m pip install -r .\requirements.txt
```



## Docs
### Add new screen:
1) Add new folder in `screens` directory
2) Add `ctrl.py` and `ui.kv` files into created directory
#### ctrl.py

  ```python 
  from kivy.properties import ObjectProperty
  from screens.common.ctrl import CommonScreen


  class NewScreen(CommonScreen):
    action: ObjectProperty(None)

    def action(self):
        print('Action')
  ```
#### ui.kv

  ```python 
  <NewScreen@Screen>:
      name: "new_screen"
      MDRaisedButton:
          text:'Go Home'
          pos_hint : {'center_x':0.4,'center_y':0.3}
          size_hint: (0.13,0.1)
          on_release:
              # transition setups (see docs for ScreenManager)
              app.root.transition.direction = 'left'
              app.root.current = 'home_screen''
              # method from class
              root.action()
   ```

3) Add new line with screen class into `main.py` class `AppScreenManager`
   ```python
    from screens.home.ctrl import HomeScreen
    from screens.auth.signin.ctrl import SignIn
    from screens.newscreen.ctrl import NewScreen
   ...
    class AppScreenManager(ScreenManager):
        home_screen: HomeScreen
        login_screen: SignIn
        new_screen: NewScreen # <- new screen class
    ```

4) Add new screen to `ui.kv` in root directory (near `main.py` file)
   ```kv
    #:kivy 2.0.0
    #:include screens/home/ui.kv
    #:include screens/login/ui.kv
    #:include screens/new/ui.kv
    ScreenManager:
        id: screen_manager
        current: 'new_screen' # <- to be insure screen created
    
        LoginScreen:
        HomeScreen:
        NewScreen: # <- new screen
5) ```



## Public snapshot

Firebase credentials and history containing them are excluded. Copy config.example.ini to config.ini and configure your own Firebase project. Never commit config.ini or service account keys. Original source history is retained in the private repository.
