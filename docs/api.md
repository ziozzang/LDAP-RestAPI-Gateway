# TL; DR
API Lists for LDAP to RESTful API Server



# Get
## Get All user lists
* PATH: /Users
* Method: GET
* Params: No Params
* Request Example
```
curl -X GET http://foo.com:5000/Users
```

* Result: JSON type
```
[
	[
		"cn=Jioh Jung,ou=People,dc=foo,dc=local",
		{
			"cn": [
				"Jioh Jung"
			],
			"departmentNumber": [
				"Dev PM."
			],
			"description": [
				"Desc"
			],
			"gidNumber": [
				"10000"
			],
			"givenName": [
				"Jioh"
			],
			"homeDirectory": [
				"/home/ziozzang"
			],
			"initials": [
				"Mr"
			],
			"loginShell": [
				"/bin/bash"
			],
			"mail": [
				"asdf@foo.com"
			],
			"mobile": [
				"010-0000-0000"
			],
			"objectClass": [
				"posixAccount",
				"inetOrgPerson",
				"organizationalPerson",
				"person"
			],
			"sn": [
				"Jung"
			],
			"title": [
				"CM"
			],
			"uid": [
				"ziozzang"
			],
			"uidNumber": [
				"12345678"
			]
		}
	],
	[
		"uid=qqq,ou=People,dc=foo,dc=local",
		{
			"cn": [
				"qqq"
			],
			"gidNumber": [
				"10000"
			],
			"homeDirectory": [
				"/home/qqq"
			],
			"objectClass": [
				"person",
				"posixAccount",
				"inetOrgPerson",
				"organizationalPerson"
			],
			"sn": [
				"qqq"
			],
			"uid": [
				"qqq"
			],
			"uidNumber": [
				"405394"
			]
		}
	]
]
......
```

## Get Specfic user by ID
* PATH: /Users/[user_id]
* Method: GET
* Params: No Params
* Request Example
```
curl -X GET http://foo.com:5000/Users/[user_id]
```

* Result: JSON type
```
[
	[
		"uid=qqq,ou=People,dc=foo,dc=local",
		{
			"cn": [
				"qqq"
			],
			"gidNumber": [
				"10000"
			],
			"homeDirectory": [
				"/home/qqq"
			],
			"objectClass": [
				"person",
				"posixAccount",
				"inetOrgPerson",
				"organizationalPerson"
			],
			"sn": [
				"qqq"
			],
			"uid": [
				"qqq"
			],
			"uidNumber": [
				"400000"
			]
		}
	]
]
```

# Delete
## Delete Users
* PATH: /Users/[user_id]
* Method: DELETE
* Params: No Params
* Request Example
```
curl -X DELETE http://foo.com:5000/Users/[user_id]
```

* Result: JSON type
```
# Success
{
	"message": "OK"
}

# Failed
{
	"message": "Failed - No such User"
}
```

# Password
## Password Check
* PATH: /Password/[user_id]
* Method: POST
* Params *WARNING: Case Sensetive*
  * userPassword : PlainText Password.
* Request Example
```
curl -X POST http://foo.com:5000/Password/[user_id]
```

* Result: JSON type
```
# Success
{
	"message": "OK"
}
# Failed
{
	"message": "FAILED - Login Error: Invalid credentials"
}
```

## Change Password
* PATH: /Password/[user_id]
* Method: PUT
* Params *WARNING: Case Sensetive*
  * userPassword : PlainText Password.
* Request Example
```
curl -X PUT http://foo.com:5000/Password/[user_id]
```

* Result: JSON type
```
# Success
{
        "message": "OK"
}
# Failed
{
        "message": "FAILED -" // Error Messages..
}
```

# Create/Add
## Add User
* PATH: /Users
* Method: PUT
* Params *WARNING: Case Sensetive*
  * cn :  (mandatory) Common Name
  * uid :  (mandatory) User ID
  * displayName :  (mandatory) Full Name
  * uidNumber :  (mandatory) UNIX UID Number
  * userPassword :  (mandatory) Password
  * mobile :Phone Number
  * telephonenumber :  Phone Number
  * mail : E-Mail
  * memberUid : member uid
  * o : Oraganization / Company
  * ou : Organization Units / Departments
  * sn :  Sur Name(Last Name/Familiy Name)
  * givenName :  Given Name
  * title :  Job Title
  * objectClass :  Object Class
  * gidNumber :  UNIX GroupID
  * description : Description
  * nickname :  nickname
  * homeDirectory :  home Directory for POSIX Account

* Request Example

```
curl -X PUT http://foo.com:5000/Users
```

* Result: JSON type
```
# Success
{
	"message": "OK"
}

# Failed
{
	"message": "Failed - No such User"
}

```
