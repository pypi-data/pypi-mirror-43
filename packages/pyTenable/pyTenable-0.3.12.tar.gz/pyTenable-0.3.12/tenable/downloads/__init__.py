'''
.. autoclass:: Downloads
.. 

Raw HTTP Calls
==============

Even though the ``Downloads`` object pythonizes the downloads API for 
you, there may still bee the occasional need to make raw HTTP calls to the 
Downloads portal API.  The methods listed below aren't run through any 
naturalization by the library aside from the response code checking.  These 
methods effectively route directly into the requests session.  The responses 
will be Response objects from the ``requests`` library.  In all cases, the path 
is appended to the base ``url`` parameter that the ``Downloads`` object was
instantiated with.

Example:

.. code-block:: python

   resp = sc.get('feed')

.. py:module:: tenable.sc
.. rst-class:: hide-signature
.. autoclass:: TenableSC

    .. automethod:: get
    .. automethod:: post
    .. automethod:: put
    .. automethod:: delete
'''
from tenable.base import APISession, APIEndpoint

class Downloads(APISession):
    '''
    The Downloads object is the primary interaction point for users to
    interface with downloads API via the pyTenable library.  All of the API
    endpoint classes that have been written will be grafted onto this class.

    Args:
        api_key (str, optional):
            The user's API access key for Tenable.io  If an access key isn't
            specified, then the library will attempt to read the environment
            variable ``TIO_ACCESS_KEY`` to acquire the key.
        url (str, optional):
            The base URL that the paths will be appended onto.  The default
            is ``https://tenable.com/downloads/api/v2`` 
        retries (int, optional):
            The number of retries to make before failing a request.  The
            default is ``3``.
        backoff (float, optional):
            If a 429 response is returned, how much do we want to backoff
            if the response didn't send a Retry-After header.  The default
            backoff is ``1`` second.
        ua_identity (str, optional):
            An application identifier to be added into the User-Agent string
            for the purposes of application identification.

    Examples:
        >>> from tenable.io import TenableIO
        >>> tio = TenableIO('ACCESS_KEY', 'SECRET_KEY')
    '''
    _url = 'https://tenable.com/downloads/api/v2'

    def __init__(self, api_key=None, url=None, retries=None, backoff=None, 
                 ua_identity=None, session=None):
        self._api_key = api_key
        APISession.__init__(self, url, retries, backoff, ua_identity, session)
    
    def _build_session(self):
        '''
        Build the session and add the API Keys into the session
        '''
        APISession._build_session(self)
        self._session.trust_env = False
        self._session.headers.update({
            'Authorization': 'Bearer {}'.format(self._api_key)})
    
    @property
    def pages(self):
        return DownloadPages(self)


class DownloadPages(APIEndpoint):
    def list(self):
        return self._api.get('pages').json()
    
    def details(self, page):
        return self._api.get('pages/{}'.format(
            self._check('page', page, str))).json()
    
    def download(self, page, package, fobj=None):
        if not fobj:
            fobj = BytesIO()

        # Now that the status has reported back as "ready", we can actually
        # download the file.
        resp = self._api.get('pages/{}/files/{}'.format(
            self._check('page', page, str), 
            self._check('package', package, str)), stream=True)

        # Lets stream the file into the file-like object...
        for chunk in resp.iter_content(chunk_size=1024):
            if chunk:
                fobj.write(chunk)
        fobj.seek(0)

        # Lastly lets return the FileObject to the caller.
        return fobj