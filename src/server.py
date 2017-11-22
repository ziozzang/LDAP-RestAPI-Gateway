#!/usr/bin/env python
##################################################
#
# Code by Jioh L. Jung <ziozzang@gmail.com>
#
##################################################

# Import Flask Restful API library
from flask import Flask, request, abort
from flask_restful import Resource, Api
from flask_restful import reqparse

# Import Python-LDAP library
import ldap
import ldap.modlist as modlist

# Import Password String Generator
import hashlib
import os

# Process JSON
import json

# Process Network Masking
from netaddr import IPNetwork, IPAddress

# Configuration Add from conf.py file
from conf import *

# for Debugging Purpose
import pickle

####################################################
# Base Shared Connection.
def do_connect():
	con.simple_bind("cn=%s,%s" % (ADMIN["id"], BASE_DN), ADMIN["pw"])

# Basic LDAP Server Connection
con = ldap.initialize(SERVER)
con.protocol_version = ldap.VERSION3
do_connect()

app = Flask(__name__)
api = Api(app)

# Request Parsing
parser = reqparse.RequestParser()
parser.add_argument('user_id')
for i in ALLOWED_LDIF:
	parser.add_argument(i)

####################################################
# IP Filtering Functions
# Get Real IP, Behind Reverse Proxy.
def get_real_ip():
	ipaddr = request.remote_addr
	if "X-Forwarded-For" in request.headers.keys():
		if ipaddr != request.headers["X-Forwarded-For"]:
			ipaddr = request.headers["X-Forwarded-For"].strip()
	if "X-Real-Ip" in request.headers.keys():
		if ipaddr != request.headers["X-Real-Ip"]:
			ipaddr = request.headers["X-Real-Ip"].strip()
	return ipaddr

# Check if IP is restricted
def check_allowed_ip():
	ipaddr = get_real_ip()
	for i in ALLOWED_FROM:
		if IPAddress(ipaddr) in IPNetwork(i):
			return True
	for i in DENYED_FROM:
		if IPAddress(ipaddr) in IPNetwork(i):
			return False
	return False

def abort_if_ip_not_allowed():
	if not  check_allowed_ip():
		detected_ip = get_real_ip()
		abort(403, "Your IP is not allowed to call API: (Detected IP - {})".format(detected_ip))
	do_connect()
####################################################
#  Shared LDAP related functions
# Password Generation
def make_secret(password):
	# Encodes the given password as a base64 SSHA hash+salt buffer
	salt = os.urandom(4)

	# hash the password and append the salt
	sha = hashlib.sha1(password)
	sha.update(salt)

	# create a base64 encoded string of the concatenated digest + salt
	digest_salt_b64 = '{}{}'.format(sha.digest(), salt).encode('base64').strip()

	# now tag the digest above with the {SSHA} tag
	tagged_digest_salt = '{{SSHA}}{}'.format(digest_salt_b64)

	return tagged_digest_salt

# Exclude Ldif field from result.
def filter_result(lists):
	res = []
	for i in lists:
		# To set case insensative matching
		k = { x.lower():x for  x in i[1].keys() }
		for j in KEYS_FILTER:
			if j.lower() in k.keys():
				del i[1][k[j.lower()]]
		res.append(i)
	return res

# Generate user field
def gernerate_ldif(user_id):
	args = parser.parse_args()

	attrs = {}

	# Set User ID
	attrs["uid"] = user_id

	# Params

	for i in ALLOWED_LDIF:
		if i in args.keys():
			if  args[i] is not None:
				attrs[i] = []
				attrs[i].append(str(args[i]))

	# Mandatory: RECORD TYPE
	if (not attrs.has_key("objectClass")) or (args["objectClass"] is None):
		attrs['objectClass'] = ['person','posixAccount', 'inetOrgPerson', 'organizationalPerson']

	if (not attrs.has_key("gidNumber")) or (args["gidNumber"] is None):
		attrs['gidNumber'] = ["10000",]

	if (not attrs.has_key("homeDirectory")) or (args["homeDirectory"] is None):
		attrs['homeDirectory'] = ["/home/%s" % (user_id),]

	if (not attrs.has_key("loginShell")) or (args["loginShell"] is None):
		attrs['loginShell'] = ["/bin/false",]

	# Add Password
	attrs['userPassword'] = [make_secret(args["userPassword"]), ]

	mlist = modlist.addModlist(attrs)

	res = []
	for i in mlist:
		res.append((i[0], i[1]))
	return res

# Update Passwords
def update_password(user_id):
	args = parser.parse_args()
	old = {'userPassword':''} # Remove Old Password
	new = {'userPassword':make_secret(args["userPassword"])} # Set New Password

	return modlist.modifyModlist(old,new)

# Get LDAP DN string.
def get_dn(user_id):
	return filter_result(con.search_s(BASE_DN, ldap.SCOPE_SUBTREE, "(uid=%s)" % (user_id,)))

class LDAPUsers(Resource):
	# User info get
	def get(self, user_id):
		abort_if_ip_not_allowed()
		return get_dn(user_id)

	def put(self, user_id):
		abort_if_ip_not_allowed()
		args = parser.parse_args()
		ldif = gernerate_ldif(args['uid'])
		#pickle.dump(ldif, open("data", "wb"))
		try:
			con.add_s("uid=%s,ou=People,%s" % (args['uid'], BASE_DN), ldif)
			return {'message':"OK"}
		except Exception as e:
			abort(500, "FAILED - %s" % (e.message,))

	def delete(self, user_id):
		abort_if_ip_not_allowed()
		try:
			# Acquire Targeting DN from searching.
			dn = get_dn(user_id)[0][0]
		except:
			abort(500, "Failed - No such User")
		try:
			con.delete_s(dn) #,204
			return {'message':"OK"}
		except Exception as e:
			abort(500, "FAILED - %s" % (e.message,))

class LDAPUsersAll(Resource):
	def get(self):
		abort_if_ip_not_allowed()
		res = con.search_s(BASE_DN, ldap.SCOPE_SUBTREE, SEARCH_SCOPE)
		return filter_result(res)
	def put(self):
		abort_if_ip_not_allowed()
		args = parser.parse_args()
		ldif = gernerate_ldif(args['uid'])
		try:
			con.add_s("uid=%s,ou=People,%s" % (args['uid'], BASE_DN), ldif)
			return {'message':"OK"}
		except Exception as e:
			abort(500, "FAILED - %s" % (e.message,))

# Password Update
class LDAPPassword(Resource):
	def put(self, user_id):
		abort_if_ip_not_allowed()
		args = parser.parse_args()
		try:
			dn = get_dn(user_id)[0][0]
		except:
			abort(500, "Failed - No such User")
		try:
			#ldif = update_password(user_id)
			ldif = [(ldap.MOD_REPLACE, 'userPassword', str(make_secret(args["userPassword"])))]
			con.modify_s(dn,ldif)
			return {'message':"OK"}
		except Exception as e:
			abort(500, "FAILED - %s" % (e.message,))

	def post(self, user_id):
		abort_if_ip_not_allowed()
		args = parser.parse_args()
		try:
			dn = get_dn(user_id)[0][0]
		except:
			abort(500, "Failed - No such User")
		try:
			tc = ldap.initialize(SERVER)
			tc.simple_bind_s(dn, str(args['userPassword']))
			tc.unbind_s()
			return {'message':"OK"}
		except Exception as e:
			abort(500, "FAILED - Login Error: " + str(e.message["desc"]))

#api.add_resource(LDAPUsersAll,'/Users')
api.add_resource(LDAPUsers, '/Users/<string:user_id>')
api.add_resource(LDAPUsersAll,'/Users')
api.add_resource(LDAPPassword, '/Password/<string:user_id>')

if __name__ == '__main__':
    app.run(host=BIND_ADDR, debug=DEBUG)

