# PyBan
Python IBAN validation tool. Checks general format, various country-based 
formatting rules, and includes general mod-97 validation.

## Basic usage
```
from pyban.iban import IBAN

try:
    iban = IBAN('BG18RZBB91550123456789')
except ValueError as e:
    # Handle error
    pass
    
return iban.formatted  # Return readable IBAN number
```