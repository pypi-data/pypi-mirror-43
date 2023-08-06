from flask import make_response, request
from datetime import datetime
from functools import wraps
import sys
import traceback
import requests
import asyncio
import aiohttp
import socket


class Logger:
	"""
	An instance of the :class:`Logger` object is created in the main module or the `__init__` file like this::
	
		logger = Logger(app, accessKey, [config_object: optional])

	`app` is the instance of the current Flask application.
	`accessKey` is the generated key associated with the Flask application.
	`config_object` is a dict that contains configuration values for the instance of the `Logger` object. It can be one or either of the following:
		config_object["LOG_TYPE"]
		config_object["DO_NOT_LOG"]

	The following Flask application configuration values MUST be set::

		app.config["LOGGING_URL"]
		app.config["LOG_AUTH_KEY"]
	Without the above configuration values, the object shall not be successfully created and an exception shall be raised.
	"""
	
	def log(self):
		"""
		This is responsible for actually posting the logging data to the external service.\
		Depending on the "LOG_TYPE" set, it is either implemented as a function wrapper or called in the `__init__` file.
		"""

		header_dict = dict(request.headers)

		try:
			tracker_id = header_dict["tracker_id"]
		except Exception:
			tracker_id = None
		
		try:
			user_agent = header_dict["User-Agent"]
		except Exception:
			user_agent = None

		try:
			language = header_dict["Accept-Language"]
		except Exception:
			language = None

		try:
			referer = header_dict["Referer"]
		except Exception:
			referer = None

		try:
			origin = header_dict["Origin"]
		except Exception:
			origin = None

		try:
			json_data = request.json
		except Exception:
			json_data = None

		try:
			platform = request.user_agent.platform.title()
		except Exception:
			platform = None

		try:
			browser = request.user_agent.browser.title()
		except Exception:
			browser = None

		try:
			auth_header_token = header_dict["Authorization"].split(" ")[1]
		except Exception:
			auth_header_token = None
		
		## If set to run before a request: This is the default setting
		if self.pre_request:
			@self.app.before_request()
			def run():
				## If the path accessed is in the do_not_log list, it is skipped
				if request.path in self.do_not_log:
					return
				## If the path accessed is not in the do_not_log list, it is posted
				else:
					post_data = {
						"error": None,
						"stack_trace": None,
						"method": request.method,
						"source_ip": request.remote_addr,
						"url": request.url,
						"status_code": 200, ## Assumed to be 200 due to the nature of the function
						"headers": str(header_dict),
						"user_agent": user_agent,
						"language": language,
						"platform": platform,
						"browser": browser,
						"referer": referer,
						"origin": origin,
						"auth_header": auth_header_token,
						"access_time": datetime.now().strftime("%A, %d %B %Y %H:%M:%S"),
						"logging_access_key": self.accessKey,
						"json": json_data,
						"request_params": str(dict(request.args))
					}

					self.startPost(post_data)

					return

			return run
		
		## If set to as a wrapper to a function
		else:
			def log_decorator(func):

				@wraps(func)
				def execute(*args, **kwargs):
					try:
						result = func(*args, **kwargs)

						result_response = make_response(result)

						post_data = {
							"error": None,
							"stack_trace": None,
							"method": request.method,
							"source_ip": request.remote_addr,
							"url": request.url,
							"status_code": result_response.status_code,
							"headers": str(header_dict),
							"user_agent": user_agent,
							"language": language,
							"platform": platform,
							"browser": browser,
							"referer": referer,
							"origin": origin,
							"auth_header": auth_header_token,
							"access_time": datetime.now().strftime("%A, %d %B %Y %H:%M:%S"),
							"logging_access_key": self.accessKey,
							"json": json_data,
							"request_params": str(dict(request.args))
						}

						self.startPost(post_data)

					except Exception as e:
						result = func(*args, **kwargs)
						
						trace = traceback.format_exc()

						kwargs = {
							"trace": trace,
							"exception": str(e)
						}
						
						post_data = {
							"error": str(e),
							"stack_trace": trace,
							"method": request.method,
							"source_ip": request.remote_addr,
							"url": request.url,
							"status_code": 500,
							"headers": str(header_dict),
							"user_agent": user_agent,
							"language": language,
							"platform": platform,
							"browser": browser,
							"referer": referer,
							"origin": origin,
							"auth_header": auth_header_token,
							"access_time": datetime.now().strftime("%A, %d %B %Y %H:%M:%S"),
							"logging_access_key": self.accessKey,
							"json": json_data,
							"request_params": str(dict(request.args))
						}

						self.startPost(post_data)
					
					return result
				
				return execute
			
			return log_decorator
	
	
	def startPost(self, postData):
		loop = asyncio.new_event_loop()
		asyncio.set_event_loop(loop)
		loop.run_until_complete(self.postAsyncData(postData))

	
	async def postAsyncData(self, postData):
		logging_url = self.app.config["LOGGING_URL"]
		headers = {
			"X-Api-Key": self.app.config["LOG_AUTH_KEY"],
			"Content-Type": "application/json",
			"Origin": request.remote_addr
		}
		
		async with aiohttp.ClientSession() as session:
			await session.post(logging_url, json=postData, headers=headers)


	def __init__(self, app = None, accessKey = None, config_object = None):
		if not app:
			raise ValueError("'app' must be an instance of a Flask application")

		if not "LOGGING_URL" in app.config:
			raise ValueError("The configuration variable 'LOGGING_URL' must be set.")

		if not "LOG_AUTH_KEY" in app.config:
			raise ValueError("The configuration variable 'LOG_AUTH_KEY' must be set.")

		if not isinstance(app.config["LOGGING_URL"], str):
			raise TypeError("'LOGGING_URL' must be an instance of type 'str'")

		if not isinstance(app.config["LOG_AUTH_KEY"], str):
			raise TypeError("'LOG_AUTH_KEY' must be an instance of type 'str'")

		if not config_object:
			self.pre_request = True
		
		else:
			allowed_values = ["wrapper", "pre_request"]

			if config_object["LOG_TYPE"].lower() not in allowed_values:
				raise ValueError("The value assigned to the config variable 'LOG_TYPE' is not allowed.")
			
			if config_object["LOG_TYPE"].lower() == "wrapper":
				self.pre_request = False
			elif config_object["LOG_TYPE"].lower() == "pre_request":
				self.pre_request = True

			if "DO_NOT_LOG" in config_object:
				do_not_log = []
			else:
				do_not_log = config_object["DO_NOT_LOG"]
		
		self.accessKey = accessKey
		self.app = app
		self.do_not_log = do_not_log