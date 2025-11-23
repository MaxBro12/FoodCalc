## Backend

### DB

#### Keys

|name|type|desc|
|----|----|----|
|id|INT PRYMARY KEY| - |
|hash|VARCHAR UNIQUE| - |
|is_admin|BOOLEAN| - |
|is_guest|BOOLEAN| - |
|is_user|BOOLEAN| - |

#### Users

|name|type|desc|
|----|----|----|
|id|INT PRYMARY KEY|-|
|name|VARCHAR UNIQUE|save only hashed|
|password|VARCHAR|save only hashed|
|is_admin|BOOLEAN|-|
|last_active|DATETIME|-|

#### Minerals & Vitamins

|name|type|desc|
|----|----|----|
|id|INT PRYMARY KEY|-|
|name|VARCHAR|-|
|description|TEXT|-|

#### Products

|name|type|desc|
|----|----|----|
|code|INT PRYMARY KEY|-|
|name|VARCHAR|-|
|description|TEXT||
