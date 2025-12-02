# import os
# import yaml
# import streamlit as st
# import streamlit_authenticator as stauth
# from yaml.loader import SafeLoader

# class AuthService:
#     def __init__(self, config_path: str):
#         self._config_path = config_path
#         self._load_config()
#         # Create the authenticator
#         self.authenticator = stauth.Authenticate(
#             self.config['credentials'],
#             self.config['cookie']['name'],
#             self.config['cookie']['key'],
#             self.config['cookie']['expiry_days']
#         )

#     def _load_config(self):
#         if not os.path.exists(self._config_path):
#             raise FileNotFoundError(f"Config file not found: {self._config_path}")
#         with open(self._config_path, 'r') as file:
#             self.config = yaml.load(file, Loader=SafeLoader)

#     def login(self, location: str = 'main'):
#         name, authentication_status, username = self.authenticator.login(location=location)
#         return name, authentication_status, username

#     def logout(self, button_name: str = 'Logout', location: str = 'main'):
#         self.authenticator.logout(button_name=button_name, location=location)

#     def register(self, pre_authorized: list = None, location: str = 'main'):
#         # returns (email, username, name) or (None, None, None)
#         return self.authenticator.register_user(pre_authorized=pre_authorized, location=location)

#     def forgot_password(self, send_email: bool = False, two_factor_auth: bool = False, location: str = 'main'):
#         return self.authenticator.forgot_password(send_email=send_email, two_factor_auth=two_factor_auth, location=location)

#     def reset_password(self, username: str, location: str = 'main'):
#         return self.authenticator.reset_password(username=username, location=location)

#     def update_user_details(self, username: str, location: str = 'main'):
#         return self.authenticator.update_user_details(username=username, location=location)

#     def get_roles(self):
#         return st.session_state.get('roles')

#     def is_authenticated(self):
#         return st.session_state.get('authentication_status') is True
