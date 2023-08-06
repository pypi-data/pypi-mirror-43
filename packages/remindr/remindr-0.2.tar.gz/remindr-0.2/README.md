### Remindr

Remindr automatically sends reminders about last blog entries on social networks, like the [Mastodon](https://joinmastodon.org) or ([Twitter](https://twitter.com)).
For the full documentation, [read it online](https://remindr.readthedocs.org/en/latest/).

If you would like, you can [support the development of this project on Liberapay](https://liberapay.com/carlchenet/).
Alternatively you can donate cryptocurrencies:

- BTC: 1A7Uj24MpoEkzywPtmPffNvC7SfF4EiWEL
- XMR: 43GGv8KzVhxehv832FWPTF7FSVuWjuBarFd17QP163uxMaFyoqwmDf1aiRtS5jWgCiRsi73yqedNJJ6V1La2joznKHGAhDi

### Quick Install

* Install Remindr from PyPI

        # pip3 install remindr

* Install Remindr from sources
  *(see the installation guide for full details)
  [Installation Guide](http://remindr.readthedocs.org/en/latest/install.html)*


        # tar zxvf remindr-0.3.tar.gz
        # cd remindr
        # python3 setup.py install
        # # or
        # python3 setup.py install --install-scripts=/usr/bin

### Create the authorization for the Remindr app

* Just launch the following command::

        $ register_remindr_app

### Use Remindr

* Create or modify remindr.ini file in order to configure remindr:

        [mastodon]
        instance_url=https://mastodon.social
        user_credentials=remindr_usercred.txt
        client_credentials=remindr_clientcred.txt
        ; Default visibility is public, but you can override it:
        toot_visibility=public
        ; image=false

        [twitter]
        consumer_key=o6lv2gZxkzk6UbQ30N4vFmlwP
        consumer_secret=j4VxU2slv0Ud4rbgZeGbBzPG1zoauBGLiUkOX0MGF6nsjcyn4a
        access_token=1234567897-Npq5fYybhacYxnTqb42Kbb3A0bKgmB3wm2hGczB
        access_token_secret=HU1snUif010DkcQ3SmUAdObAST14dZQZpuuWxGAV0xFnC
        ; image=false

        [image]
        ; if you only need on image for all tweets/toots
        path_to_image=/home/chaica/blog-carl-chenet.png
        ; for using different images given the language
        ; fr_image_path=/home/chaica/fr-blog-carl-chenet.png
        ; en_image_path=/home/chaica/en-blog-carl-chenet.png

        [entrylist]
        path_to_list=/etc/remindr/list.txt

        [prefix]
        en_prefix=Still On My Blog:
        fr_prefix=Toujours sur mon blog:

* Launch Remindr

        $ remindr -c /path/to/remindr.ini

### Authors

* Copyright 2017-2019 © Carl Chenet <chaica@ohmytux.com>

### License

This software comes under the terms of the GPLv3+.
