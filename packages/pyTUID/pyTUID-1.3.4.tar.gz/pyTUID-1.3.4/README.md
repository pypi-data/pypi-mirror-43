# pyTUID
pyTUID is a simple CAS client django app which, contrary to other apps like this, don't use the `django.contrib.auth` models nor middleware. So all data is saved to a own database table (or not att all).
pyTUID is fitted for our use case with the CAS of the TU Darmstadt (hence the name) but can probably be used with many other CAS servers with a similar configuration (CAS 2 with SAML 1).

Feel free to adapt this app to your needs. If you make changes compatible to the current behavior (or if it is configurable) I would be glad if you made a pull request.

## Setup
* To set up install this python library (for example with pip).
* In your `settings.py`:
  * Add `pyTUID` to your `INSTALLED_APPS`.
  * Add `pyTUID.middleware.TUIDMiddleware` to your `MIDDLEWARE_CLASSES`.
  * Set at least `TUID_SERVER_URL` to your CAS server URL.
* Include `pyTUID.urls` in your `urls.py` at any path you like.
* Apply the migrations.
* That's it!

## Configuration
Currently the following settings are available:
* `TUID_SERVER_URL` the CAS server URL (default: `None`)
* `TUID_CREATE_USER` sets whether the logged in users should be saved to the database (default: `True`)
* `TUID_LOGIN_DEFAULT_NEXT` sets the default page after login when no `next` is present in `POST` or `GET` parameters (default: `"/"`)
* `TUID_LOGOUT_DEFAULT_NEXT` sets the default page after logout when no `next` is present in `POST` or `GET` parameters (default: `"/"`)
* `TUID_MAPPING` sets the mapping from SAML attributes to model fields (key is model field, value is SAML attribute)
  The default is:

  ```python
  {'surname'   : 'surname',
   'given_name' : 'givenName',
   'email'      : 'mail',
   'groups'     : 'groupMembership'}
  ```
  Every key not provided in your config will be set to default.
* `TUID_FORCE_SERVICE_URL` sets the service url provided to CAS. If not set the
  request url is used as service url.

## Usage
There are three different ways to use this app:

### Decorators
For function based views the easiest interaction with this app is using the view function decorators:

#### tuid_login_required
The [`@tuid_login_required`](https://github.com/d120/pyTUID/blob/240d5c6/pyTUID/decorators.py#L35) decorator checks whether the user is logged in (with TUID) and redirects it to the login page otherwise.

#### tuid_user_in_group
The [`@tuid_user_in_group(group[, permission_denied_message])`](https://github.com/d120/pyTUID/blob/240d5c6/pyTUID/decorators.py#L49) decorator first checks whether the user is logged in (with TUID) and displays the login page otherwise. If the user is already logged in it is checked whether it is in the given `group` and a `PermissionDenied` is risen with the optional `permission_denied_message`.

#### tuid_user_passes_test
The [`@tuid_user_passes_test(test_func[, raise_exception[, permission_denied_message]])`](https://github.com/d120/pyTUID/blob/240d5c6/pyTUID/decorators.py#L10) decorator applies the `test_func` on the `TUIDUser` object. If `True` is returned the view will be displayed as usual. If `False` is returned and `raise_exception` is `True` a `PermissionDenied`exception with the optional `permission_denied_message` will be risen. If `raisle_exceptio` is `False` (the default) the login page will be displayed.

### Mixins
For class based views the following two mixins exists:

#### TUIDLoginRequiredMixin
The [`TUIDLoginRequiredMixin`](https://github.com/d120/pyTUID/blob/240d5c6/pyTUID/mixins.py#L6) works exactly like the `tuid_login_required` decorator.

#### TUIDUserInGroupMixin
The [`TUIDUserInGroupMixin`](https://github.com/d120/pyTUID/blob/240d5c6/pyTUID/mixins.py#L20) works like the `tuid_user_in_group` decorator except that the parameters have to be specified as fields of the view class. The `group_required` field acts like the group parameter of the decorator and the `permission_denied_message` (optional) acts also like the `permission_denied_message`of the decorator.

### TUIDUser
For more specific use-cases you may use the `TUIDUser` object of the `request`, which is an instance of [`models.TUIDUSER`](https://github.com/d120/pyTUID/blob/240d5c6/pyTUID/models.py#L4).
