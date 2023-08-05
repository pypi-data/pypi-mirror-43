import os
import platform
from zybats.ext.datasupport import pbjson
import simplejson

class PBUtil(object):
	# 编译pb文件到pyhon文件
	def compilePbToPy(pb_file_Path):
		def _UsePlatform():
			sys_str = platform.system()
			return sys_str

		current_dir = os.getcwd()
		if os.path.isfile(pb_file_Path):
			file_path, file_name = os.path.split(pb_file_Path)
			sys_name = _UsePlatform()

			if (sys_name == "Windows"):
				cmd = "%s\protoc.exe -I=%s --python_out=%s %s" % (current_dir, file_path, file_path, pb_file_Path)
				os.system(cmd)
				return True
			elif (sys_name == "Linux"):
				return True
			else:
				print("Other System tasks")

		return False

	# json转换为pb
	def jsonToPb(json_file_path, pb_dict_):
		try:
			file = open(json_file_path, 'r')
			str = simplejson.load(file)
			file.close
			t = pbjson.dict2pb(pb_dict_, str)
			data = t.SerializePartialToString()
			return data
		except Exception as e:
			print("JsonToPb error!", e)
			return

if __name__ =='__main__':
	PBUtil.compilePbToPy("E:\\c++\\dsp\\addyer.proto")