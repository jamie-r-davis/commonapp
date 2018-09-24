# commonapp

Interface for scripting actions typically conducted via the CommonApp Control Center.

```python
from commonapp import CommonApp

cap = CommonApp(username, password)
filename = 'CommonAppApplications_12312018'
cap.retrieve_file(filename, local_path=os.path.join('output', filename))
```
