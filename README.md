# sprea-utils
Tools for interact with sprea.it

I've create this small library to check/download automaticaly the ebooks
purchased on the site sprea.it

This library for navigate the site use *mechanicalsoup* library.
*requests* and *urllib* is used for other small things. 

** Install
```
git clone git@github.com:matteogaito/sprea-utils.git
cd sprea-utils
python3 setup.py install
```
pip module has coming
But if you want put it in your requirements txt
```
git+https://github.com/matteogaito/sprea-utils.git
```

** Usage

Example File
```
from sprea_utils import Sprea

USER="xxxxxxxxx"
PASSWORD="xxxxx"

#Give you your digital purchased subscription
Sprea(USER,PASSWORD).listCampaigns()

# Download the pdf 0 of given campaign
Sprea(USER,PASSWORD).downloadOnePdfOfCampaign("/digitali/campagna/952",0)
```

Feel free to fork this module or write me to tell me how improve it.
