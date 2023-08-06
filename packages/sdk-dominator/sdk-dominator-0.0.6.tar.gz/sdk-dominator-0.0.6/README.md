# SDK Dominator
Based on `Dominator` gun from `Psycho-Pass`, it reads and analyzes user data to determine the risk of user on financial systems.

### Helper methods
If you want, you can send `User` model to `Dominator` and it will call few methods that you can use. 

Sample:

```python
from dominator import Dominator
from core.models import User

Dominator().validate_tax_id("...", user=User)
```

If `Tax ID` is invalid, `Dominator` will try call `dominator_lock_account()` method inside the given model. So you just need create a method to execute anything you may need do if account need be locked.

If `Tax ID` is valid, `Dominator` will call for `dominator_is_valid_tax_id` sending the `SERPRO` answer as parameter.

Sample `CPF` answer parameter:

```
{
    "tax_id": "077.703.749-10",
    "name": "RAPHAEL FILIPE SCHUBERT",
    "birthday": pendulum.date(year=1992, month=2, day=10),
    "raw": {
        "ni": "07770374910",
        "nome": "RAPHAEL FILIPE SCHUBERT",
        "nascimento": "10021992",
        "situacao": {
            "codigo": "0", "descricao": "Regular"
        }
    }
}
``` 

It will be sended as `serpro` parameter, so you will need an method like:
`def dominator_is_valid_tax_id(self, *args, **kwargs)` than you will be able to access it as `serpro['tax_id']` or any data inside it.

You can provide an `cpf_django_model` on `validate_tax_id` method that will try find and store SERPRO CPF on database. 