import jwt
import bcrypt
import streamlit as st
from datetime import datetime, timedelta
import extra_streamlit_components as stx
from .hasher import Hasher
from .validator import Validator
from .utils import generate_random_pw

from .exceptions import CredentialsError, ForgotError, RegisterError, ResetError, UpdateError
from pymongo.collection import Collection

class Authenticate:
    """
    This class will create login, logout, register user, reset password, forgot password, 
    forgot email, and modify user details widgets.
    """
    def __init__(self, mongoCollection:Collection, cookie_name: str, key: str, cookie_expiry_days: float=30.0, 
        preauthorized: list=None, validator: Validator=None):
        """
        Create a new instance of "Authenticate".

        Parameters
        ----------

        cookie_name: str
            The name of the JWT cookie stored on the client's browser for passwordless reauthentication.
        key: str
            The key to be used for hashing the signature of the JWT cookie.
        cookie_expiry_days: float
            The number of days before the cookie expires on the client's browser.
        preauthorized: list
            The list of emails of unregistered users authorized to register.
        validator: Validator
            A Validator object that checks the validity of the name, and email fields.
        """

        self.collection = mongoCollection
        self.cookie_name = cookie_name
        self.key = key
        self.cookie_expiry_days = cookie_expiry_days
        self.preauthorized = preauthorized
        self.cookie_manager = stx.CookieManager()
        self.validator = validator if validator is not None else Validator()

        if 'name' not in st.session_state:
            st.session_state['name'] = None
        if 'authentication_status' not in st.session_state:
            st.session_state['authentication_status'] = None
        if 'email' not in st.session_state:
            st.session_state['email'] = None
        if 'logout' not in st.session_state:
            st.session_state['logout'] = None
        if 'trace_id' not in st.session_state:
            st.session_state['trace_id'] = None
        if 'session_id' not in st.session_state:
            st.session_state['session_id'] = None
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "answer" not in st.session_state:
            st.session_state.answer = None
        if "answer_image" not in st.session_state:
            st.session_state.answer_image = None
        if "hints" not in st.session_state:
            st.session_state.hints = []
        if "marks" not in st.session_state:
            st.session_state.marks = None
        if "explanation" not in st.session_state:
            st.session_state.explanation = None
        if "marking_scheme" not in st.session_state:
            st.session_state.marking_scheme = None
        if "improvement" not in st.session_state:
            st.session_state.improvement = None
        if "similar_problems" not in st.session_state:
            st.session_state.similar_problems = None
        if "question" not in st.session_state:
            st.session_state.question = None
        if "question_text" not in st.session_state:
            st.session_state.question_text = None
            

    def _token_encode(self) -> str:
        """
        Encodes the contents of the reauthentication cookie.

        Returns
        -------
        str
            The JWT cookie for passwordless reauthentication.
        """
        return jwt.encode({'name':st.session_state['name'],
            'email':st.session_state['email'],
            'exp_date':self.exp_date}, self.key, algorithm='HS256')

    def _token_decode(self) -> str:
        """
        Decodes the contents of the reauthentication cookie.

        Returns
        -------
        str
            The decoded JWT cookie for passwordless reauthentication.
        """
        try:
            return jwt.decode(self.token, self.key, algorithms=['HS256'])
        except:
            return False

    def _set_exp_date(self) -> float:
        """
        Creates the reauthentication cookie's expiry date.

        Returns
        -------
        float
            The JWT cookie's expiry timestamp in Unix epoch.
        """
        return (datetime.utcnow() + timedelta(days=self.cookie_expiry_days)).timestamp()

    def _check_pw(self,password:str) -> bool:
        """
        Checks the validity of the entered password.

        Returns
        -------
        bool
            The validity of the entered password by comparing it to the hashed password on disk.
        """
        return bcrypt.checkpw(self.password.encode(), password.encode())

    def _check_cookie(self):
        """
        Checks the validity of the reauthentication cookie.
        """
        self.token = self.cookie_manager.get(self.cookie_name)
        if self.token is not None:
            self.token = self._token_decode()
            if self.token is not False:
                if not st.session_state['logout']:
                    if self.token['exp_date'] > datetime.utcnow().timestamp():
                        if 'name' and 'email' in self.token:
                            st.session_state['name'] = self.token['name']
                            st.session_state['email'] = self.token['email']
                            st.session_state['authentication_status'] = True
    
    def _check_credentials(self, inplace: bool=True) -> bool:
        """
        Checks the validity of the entered credentials.

        Parameters
        ----------
        inplace: bool
            Inplace setting, True: authentication status will be stored in session state, 
            False: authentication status will be returned as bool.
        Returns
        -------
        bool
            Validity of entered credentials.
        """
        try:
            user_document = self.collection.find_one({"email": self.email})
            password = user_document['password']
        except Exception as e:
            return False
           

        if user_document:
            try:
                if self._check_pw(password):
                    if inplace:
                        st.session_state['name'] = user_document['name']
                        self.exp_date = self._set_exp_date()
                        self.token = self._token_encode()
                        self.cookie_manager.set(self.cookie_name, self.token,
                            expires_at=datetime.now() + timedelta(days=self.cookie_expiry_days))
                        st.session_state['authentication_status'] = True
                    else:
                        return True
                else:
                    if inplace:
                        st.session_state['authentication_status'] = False
                    else:
                        return False
            except Exception as e:
                print(e)
        else:
            if inplace:
                st.session_state['authentication_status'] = False
            else:
                return False

    def login(self, form_name: str, location: str='main') -> tuple:
        """
        Creates a login widget.

        Parameters
        ----------
        form_name: str
            The rendered name of the login form.
        location: str
            The location of the login form i.e. main or sidebar.
        Returns
        -------
        str
            Name of the authenticated user.
        bool
            The status of authentication, None: no credentials entered, 
            False: incorrect credentials, True: correct credentials.
        str
            email of the authenticated user.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if not st.session_state['authentication_status']:
            self._check_cookie()
            if not st.session_state['authentication_status']:
                if location == 'main':
                    login_form = st.form('Login')
                elif location == 'sidebar':
                    login_form = st.sidebar.form('Login')

                login_form.subheader(form_name)
                self.email = login_form.text_input('Email')
                st.session_state['email'] = self.email
                self.password = login_form.text_input('Password', type='password')

                if login_form.form_submit_button('Login' ,icon=":material/login:"):
                    self._check_credentials()

        return st.session_state['name'], st.session_state['authentication_status'], st.session_state['email']

    # def logout(self, button_name: str, location: str='main', key: str=None):
    #     """
    #     Creates a logout button.

    #     Parameters
    #     ----------
    #     button_name: str
    #         The rendered name of the logout button.
    #     location: str
    #         The location of the logout button i.e. main or sidebar.
    #     """
    #     if location not in ['main', 'sidebar']:
    #         raise ValueError("Location must be one of 'main' or 'sidebar'")
    #     if location == 'main':
    #         if st.button(button_name, key):
    #             self.cookie_manager.delete(self.cookie_name)
    #             st.session_state['logout'] = True
    #             st.session_state['name'] = None
    #             st.session_state['email'] = None
    #             st.session_state['authentication_status'] = None
    #     elif location == 'sidebar':
    #         if st.sidebar.button(button_name, key):
    #             if self.cookie_name in self.cookie_manager.cookies:
    #                 self.cookie_manager.delete(self.cookie_name)
    #             st.session_state['logout'] = True
    #             st.session_state['name'] = None
    #             st.session_state['email'] = None
    #             st.session_state['authentication_status'] = None
    
    # def logout(self, button_name: str, location: str='main', key: str=None):
    #     """
    #     Creates a logout button.

    #     Parameters
    #     ----------
    #     button_name: str
    #         The rendered name of the logout button.
    #     location: str
    #         The location of the logout button i.e. main or sidebar.
    #     """
    #     if location not in ['main', 'sidebar']:
    #         raise ValueError("Location must be one of 'main' or 'sidebar'")
        
    #     try:
    #         if location == 'main':
    #             if st.button(button_name, key=key):
    #                 if self.cookie_name in self.cookie_manager.cookies:
    #                     self.cookie_manager.delete(self.cookie_name)
    #                 st.session_state['logout'] = True
    #                 st.session_state['name'] = None
    #                 st.session_state['email'] = None
    #                 st.session_state['authentication_status'] = None
    #         elif location == 'sidebar':
    #             if st.sidebar.button(button_name, key=key):
    #                 if self.cookie_name in self.cookie_manager.cookies:
    #                     self.cookie_manager.delete(self.cookie_name)
    #                 st.session_state['logout'] = True
    #                 st.session_state['name'] = None
    #                 st.session_state['email'] = None
    #                 st.session_state['authentication_status'] = None
    #     except KeyError as e:
    #         st.error(f"An error occurred: {str(e)}")
    def logout(self, button_name: str, location: str='main', key: str=None):
        """
        Creates a logout button.

        Parameters
        ----------
        button_name: str
            The rendered name of the logout button.
        location: str
            The location of the logout button i.e. main or sidebar.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")

        if location == 'main':
            if st.button(button_name, key=key, icon=":material/logout:"):
                if self.cookie_name in self.cookie_manager.cookies:
                    self.cookie_manager.delete(self.cookie_name)
                st.session_state['logout'] = True
                st.session_state['name'] = None
                st.session_state['email'] = None
                st.session_state['authentication_status'] = None
                st.session_state['session_id'] = None
                # Force a page reload
                st.rerun()
        elif location == 'sidebar':
            if st.sidebar.button(button_name, key=key):
                if self.cookie_name in self.cookie_manager.cookies:
                    self.cookie_manager.delete(self.cookie_name)
                st.session_state['logout'] = True
                st.session_state['name'] = None
                st.session_state['email'] = None
                st.session_state['authentication_status'] = None
                st.session_state['session_id'] = None
                # Force a page reload
                st.rerun()


    def _update_password(self, email: str, password: str):
        """
        Updates credentials dictionary with user's reset hashed password.

        Parameters
        ----------
        email: str
            The email of the user to update the password for.
        password: str
            The updated plain text password.
        """
        try:
            query = {"email": email}
            update_data = {"$set": {"password": Hasher([password]).generate()[0] }}
            self.collection.update_one(query, update_data)
        except Exception as e:
            st.error(e)

    def reset_password(self, email: str, form_name: str, location: str='main') -> bool:
        """
        Creates a password reset widget.

        Parameters
        ----------
        email: str
            The email of the user to reset the password for.
        form_name: str
            The rendered name of the password reset form.
        location: str
            The location of the password reset form i.e. main or sidebar.
        Returns
        -------
        str
            The status of resetting the password.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            reset_password_form = st.form('Reset password')
        elif location == 'sidebar':
            reset_password_form = st.sidebar.form('Reset password')
        
        reset_password_form.subheader(form_name)
        self.email = email.lower()
        self.password = reset_password_form.text_input('Current password', type='password')
        new_password = reset_password_form.text_input('New password', type='password')
        new_password_repeat = reset_password_form.text_input('Repeat password', type='password')

        if reset_password_form.form_submit_button('Reset'):
            if self._check_credentials(inplace=False):
                if len(new_password) > 0:
                    if new_password == new_password_repeat:
                        if self.password != new_password: 
                            self._update_password(self.email, new_password)
                            return True
                        else:
                            raise ResetError('New and current passwords are the same')
                    else:
                        raise ResetError('Passwords do not match')
                else:
                    raise ResetError('No new password provided')
            else:
                raise CredentialsError('password')
    
    def _register_credentials(self, email: str, name: str, password: str):
        """
        Adds to credentials dictionary the new user's information.

        Parameters
        ----------
        name: str
            The name of the new user.
        password: str
            The password of the new user.
        email: str
            The email of the new user.
        preauthorization: bool
            The preauthorization requirement, True: user must be preauthorized to register, 
            False: any user can register.
        """

        if not self.validator.validate_name(name):
            raise RegisterError('Name is not valid')
        if not self.validator.validate_email(email):
            raise RegisterError('Email is not valid')

        # self.credentials['usernames'][username] = {'name': name, 
        #     'password': Hasher([password]).generate()[0], 'email': email}
        
        try:
            self.collection.insert_one( {'password': Hasher([password]).generate()[0],'email':email, 'name':name} )
        except Exception as e :
           
            st.error(e)

  

    def register_user(self, form_name: str, location: str='main') -> bool:
        """
        Creates a register new user widget.

        Parameters
        ----------
        form_name: str
            The rendered name of the register new user form.
        location: str
            The location of the register new user form i.e. main or sidebar.
        preauthorization: bool
            The preauthorization requirement, True: user must be preauthorized to register, 
            False: any user can register.
        Returns
        -------
        bool
            The status of registering the new user, True: user registered successfully.
        """

        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            register_user_form = st.form('Register user')
        elif location == 'sidebar':
            register_user_form = st.sidebar.form('Register user')

        register_user_form.subheader(form_name)
        new_email = register_user_form.text_input('Email')
        new_name = register_user_form.text_input('Name')
        new_password = register_user_form.text_input('Password', type='password')
        new_password_repeat = register_user_form.text_input('Repeat password', type='password')

        if register_user_form.form_submit_button('Register', icon=":material/assignment_turned_in:"):
            user_document = self.collection.find_one({"email": new_email})
            if len(new_email)  and len(new_name) and len(new_password) > 0:
                if not user_document:
                    if new_password == new_password_repeat:         
                        self._register_credentials(new_email, new_name, new_password)
                        return True
                    else:
                        raise RegisterError('Passwords do not match')
                else:
                    raise RegisterError('Email already taken')
            else:
                raise RegisterError('Please enter an email, username, name, and password')

    def _set_random_password(self, email: str) -> str:
         """
         Updates credentials dictionary with user's hashed random password.

         Parameters
         ----------
         email: str
             Email of user to set random password for.
         Returns
         -------
         str
             New plain text password that should be transferred to user securely.
         """
         self.random_password = generate_random_pw()
         #self.credentials['usernames'][username]['password'] = Hasher([self.random_password]).generate()[0]
         return self.random_password

    def forgot_password(self, form_name: str, location: str='main') -> tuple:
        """
        Creates a forgot password widget.

        Parameters
        ----------
        form_name: str
            The rendered name of the forgot password form.
        location: str
            The location of the forgot password form i.e. main or sidebar.
        Returns
        -------

        str
            Email associated with forgotten password.
        str
            New plain text password that should be transferred to user securely.
        """
        if location not in ['main', 'sidebar']:
            raise ValueError("Location must be one of 'main' or 'sidebar'")
        if location == 'main':
            forgot_password_form = st.form('Forgot password')
        elif location == 'sidebar':
            forgot_password_form = st.sidebar.form('Forgot password')

        forgot_password_form.subheader(form_name)
        email = forgot_password_form.text_input('Email').lower()

        if forgot_password_form.form_submit_button('Submit'):
            if len(email) > 0:
                user_document = self.collection.find_one({"email": email})
                if user_document:
                    user_document['password'] = Hasher([self._set_random_password(email)]).generate()[0]
                    return email, user_document['password'], self._set_random_password(email)
                else:
                    return False, None, None
            else:
                raise ForgotError('Email not provided')
        return None, None, None

    # def _get_username(self, email: str) -> str:
    #     """
    #     Retrieves username based on a provided entry.

    #     Parameters
    #     ----------
    #     key: str
    #         Name of the credential to query i.e. "email".
    #     value: str
    #         Value of the queried credential i.e. "jsmith@gmail.com".
    #     Returns
    #     -------
    #     str
    #         Username associated with given key, value pair i.e. "jsmith".
    #     """

            
    #     user_document = self.collection.find_one({"email": email})
    #     return user_document['username']
        


    # def forgot_username(self, form_name: str, location: str='main') -> tuple:
    #     """
    #     Creates a forgot username widget.

    #     Parameters
    #     ----------
    #     form_name: str
    #         The rendered name of the forgot username form.
    #     location: str
    #         The location of the forgot username form i.e. main or sidebar.
    #     Returns
    #     -------
    #     str
    #         Forgotten username that should be transferred to user securely.
    #     str
    #         Email associated with forgotten username.
    #     """
    #     if location not in ['main', 'sidebar']:
    #         raise ValueError("Location must be one of 'main' or 'sidebar'")
    #     if location == 'main':
    #         forgot_username_form = st.form('Forgot username')
    #     elif location == 'sidebar':
    #         forgot_username_form = st.sidebar.form('Forgot username')

    #     forgot_username_form.subheader(form_name)
    #     email = forgot_username_form.text_input('Email')

    #     if forgot_username_form.form_submit_button('Submit'):
    #         if len(email) > 0:
    #             return self._get_username(email), email
    #         else:
    #             raise ForgotError('Email not provided')
    #     return None, email

    # def _update_entry(self, username: str, key: str, value: str):
    #     """
    #     Updates credentials dictionary with user's updated entry.

    #     Parameters
    #     ----------
    #     username: str
    #         The username of the user to update the entry for.
    #     key: str
    #         The updated entry key i.e. "email".
    #     value: str
    #         The updated entry value i.e. "jsmith@gmail.com".
    #     """
    #     self.credentials['usernames'][username][key] = value

    # def update_user_details(self, username: str, form_name: str, location: str='main') -> bool:
    #     """
    #     Creates a update user details widget.

    #     Parameters
    #     ----------
    #     username: str
    #         The username of the user to update user details for.
    #     form_name: str
    #         The rendered name of the update user details form.
    #     location: str
    #         The location of the update user details form i.e. main or sidebar.
    #     Returns
    #     -------
    #     str
    #         The status of updating user details.
    #     """
    #     if location not in ['main', 'sidebar']:
    #         raise ValueError("Location must be one of 'main' or 'sidebar'")
    #     if location == 'main':
    #         update_user_details_form = st.form('Update user details')
    #     elif location == 'sidebar':
    #         update_user_details_form = st.sidebar.form('Update user details')
        
    #     update_user_details_form.subheader(form_name)
    #     self.username = username.lower()
    #     field = update_user_details_form.selectbox('Field', ['Name', 'Email']).lower()
    #     new_value = update_user_details_form.text_input('New value')

    #     if update_user_details_form.form_submit_button('Update'):
    #         if len(new_value) > 0:
    #             if new_value != self.credentials['usernames'][self.username][field]:
    #                 self._update_entry(self.username, field, new_value)
    #                 if field == 'name':
    #                         st.session_state['name'] = new_value
    #                         self.exp_date = self._set_exp_date()
    #                         self.token = self._token_encode()
    #                         self.cookie_manager.set(self.cookie_name, self.token,
    #                         expires_at=datetime.now() + timedelta(days=self.cookie_expiry_days))
    #                 return True
    #             else:
    #                 raise UpdateError('New and current values are the same')
    #         if len(new_value) == 0:
    #             raise UpdateError('New value not provided')