# SDK Dominator
Based on `Dominator` gun from `Psycho-Pass`, it reads and analyzes user data to determine the risk of user on financial systems.

### Automatic lock user account
If you want to validate user `Tax ID` and lock his account if is fake, you can pass a `Django Model` as parameter and `Dominator` will lock it.

Sample:

```python
from dominator import Dominator
from core.models import User

Dominator().validate_tax_id("...", user=User)
```

`Dominator` will try call `lock_account()` method inside the given model. So you just need create a method to execute anything you may need do if account need be locked. 