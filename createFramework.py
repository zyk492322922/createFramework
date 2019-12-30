# -*- coding:utf-8 -*-

import stat,os
import shutil
import time

# 复制源文件
source_path = os.path.abspath(r'D:\monster-admin')  
# 目标路径
target_path = os.path.abspath(r'D:\aaa\demo-admin')			
# 项目和文件夹名称
project_package_name = 'demo-admin'  # 项目主文件夹
# 项目缩写 
project_name_abridge = 'dm'          # 项目缩写 子模块用
# 项目顶级包名
project_top_package_name_old = "com.ms"  # 一般不用动
# 项目顶级包名(新)
project_top_package_name = "com.hyjf"    # 复制后希望的包名


# 以下 勿动
java_file_suffix = '.java'
pom_file_suffix = '.pom'
xml_file_suffix = '.xml'
txt_file_suffix = '.txt'
temp_file_suffix = '.temp'
git_dir_name = '.git'
iml_file_suffix = '.iml'
# 需要进行文件内容替换的文件后缀
replace_file_suffix = [java_file_suffix,pom_file_suffix,xml_file_suffix]
# 待删除文件夹 由shutil 忽略
#delete_file_name = ["target",".idea"]
# 待删除文件后缀
delete_file_suffix = [iml_file_suffix]


# 项目文件夹替换
replace_file_name_map = {
						    "monster-admin":project_package_name, #主pom artifactId替换
							"ms-admin":project_name_abridge + '-admin', #子pom 替换
							"ms-module-system": project_name_abridge + "-module-system",  # 子pom 替换
							"ms-ops":project_name_abridge + "-ops"
						}

# 文件内容替换
replace_file_content_map = replace_file_name_map
replace_file_content_map["com.monster"] = project_package_name
replace_file_content_map[project_top_package_name_old] = project_top_package_name


# 获取文件后缀
def getFileExtends(file_path):
	# 字符串翻转
	file_path = file_path[::-1]
	# 翻转后截取到第一个'.'的字符串，然后翻转回来
	return file_path[0:file_path.find('.') +1][::-1]

# 获取文件除后缀外的所有字符
def getFilePrefix(file_path):
	# 字符串翻转
	file_path = file_path[::-1]
	# 翻转后截取第一个'.'的后面的字符串，然后翻转回来
	return file_path[file_path.find('.') +1:][::-1]
	 

# 文件内容替换
# ① 创建同名的temp文件进行内容替换   
# ② 删除源文件
# ③ 把temp文件删除.temp后缀,变成源文件
def fileContentReplace(file_path):
	# 打开temp后缀文件, 相当于新建
	temp_file_path = file_path + temp_file_suffix
	#if getFileExtends(file_path) == pom_file_suffix:
	fp = open(temp_file_path,'w', encoding='utf-8')
	# 逐行读取替换，写到temp文件
	lines = open(file_path,'r', encoding='utf-8').readlines()
	for s in lines:
		# 循环待替换的map
		for key,value in replace_file_content_map.items():
			#print("文件内容替换：" + key + "--> " + value)
			s = s.replace(key,value)
		fp.write(s)
	fp.close()
	# 删除源文件
	os.remove(file_path)
	# 把temp文件重命名成源文件
	os.rename(temp_file_path,file_path)

def _ignore_copy_files(path,content):
	to_ignore = []
	for file_ in ('.git'):
		to_ignore.append(file_)
	return to_ignore

def create_file_tree(target_path):
	# 文件处理
	for root, dirs, files in os.walk(target_path):
		# 判断是文件，进行文件重命名
		for name in files:
			file_name = os.path.join(root,name)
			if os.path.isfile(file_name):
				# 文件后缀
				suffix = getFileExtends(file_name)
				# 文件内容替换
				if suffix in replace_file_suffix:
					fileContentReplace(file_name)
				elif suffix in delete_file_suffix:
					print("删除文件：" + name)
					os.remove(file_name)
				else:
					pass


	#   由于递归循环中如果存在修改目录操作，会影响对包含的文件的后续操作，所以决定先对文件进行处理，然后循环处理文件夹

	# 文件夹处理
	for root, dirs, files in os.walk(target_path):
		for name in dirs:
			path_name = os.path.join(root,name)
			if name in replace_file_name_map:
				print("替换文件夹：" + name  + "--> " + replace_file_name_map[name])
				os.rename(path_name,os.path.join(root,replace_file_name_map[name]))

	# 文件夹处理
	for root, dirs, files in os.walk(target_path):
		for name in dirs:
			path_name = os.path.join(root,name)
			# 待替换包路径
			path_str = "\\" +project_top_package_name_old.replace(".","\\")
			if path_name.endswith(path_str):
				new_path_name = path_name.replace(path_str,"") + "\\" +project_top_package_name.replace(".","\\")
				print("替换包文件夹：" + path_name + "--->" + new_path_name)
				os.rename(path_name,new_path_name)

	print("create file tree finished！")


if __name__ == '__main__':
	# 创建目标
	if not os.path.exists(target_path):
		print('创建目标文件')
		os.makedirs(target_path)
	# 复制文件
	if os.path.exists(source_path):
		print('删除可能已经存在的目标树')
		shutil.rmtree(target_path)
		print('复制文件树')
		shutil.copytree(source_path, target_path, ignore=shutil.ignore_patterns('.git','target','.idea'))
	# 修改文件路径，名称和内容等等	
	create_file_tree(target_path)

