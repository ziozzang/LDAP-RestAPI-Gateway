# configurations...

# Your LDAP Server
SERVER = "ldap://foo.com"
# Basic DN
BASE_DN = "dc=foo,dc=com"
# Address to Listening
BIND_ADDR = "0.0.0.0"
# DEbug Flags
DEBUG = False

ADMIN = {
  "id": "admin",
  "pw": "password_here"
}

# Search Result's Keys for filtering.
# this keys will not shown in result set.
# Get /Users or /Users/[user_id] 's result filtering. (no passwrd or JPEG images showing)
KEYS_FILTER = ["jpegPhoto","userPassword"]

# ID's who Result Filters (For Managements ID or some.)
IDS_FILTER = ["system", ]

# Get /Users or /Users/[user_id] 's result filtering. (Only show person)
SEARCH_SCOPE='(objectclass=person)'

# Reference
# http://www.tldp.org/HOWTO/archived/LDAP-Implementation-HOWTO/schemas.html
ALLOWED_LDIF = [
	"mobile",    # Phone Number
	"telephonenumber", # Phone Number
	"mail",      # E-Mail
	"memberUid", # member uid
	"o",         # Oraganization / Company
	"ou",        # Organization Units / Departments
	"cn",        # Common Name
	"sn",        # Sur Name(Last Name/Familiy Name)
	"uid",		# User ID
	"givenName", # Given Name
	"title",     # Job Title
	"objectClass", # Object Class
	"displayName", # Full Name
	"uidNumber", # UNIX UID Number
	"gidNumber", # UNIX GroupID
	"description", # Description
	"nickname",  # nickname
	"homeDirectory", # home Directory for POSIX Account
	"userPassword", # Password
]

# IP based restriction
DENYED_FROM = [
	"0.0.0.0/0", # Deny from ALL
]
ALLOWED_FROM = [
	"1.2.3.4/32", # Accept From Only
]
