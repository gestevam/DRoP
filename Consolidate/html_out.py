import re, os
def gather_comments():
	def get_comment(line):
		return re.search('^\s*#(.*)$', line)
	def is_blank(line):
		return re.search('^\s*$', line)
	def is_starred(line):
		return re.search('^\s*#\s*\*', line)
	
	file_list = open('file_list', 'r').read().split('\n')
	
	for listing in file_list[:]:
		(head, tail) = os.path.split(listing)
		if('*' in tail):
			tail = '^' + re.sub('\*', '.*', tail) + '$'
			filenames = os.listdir(head)
			for filename in filenames:
				if(re.search(tail, filename)):
					file_list.append(os.path.join(head, filename))
			file_list.pop(file_list.index(listing))
	comments = {}
	for filename in file_list:
		if(filename==''):
			continue
		if(not os.path.exists(filename)):
			comments[filename] = 'FILE NOT FOUND'
			continue
		file = open(filename, 'r')
		comments[filename] = ''
		state = 'wait'
		for line in file.readlines():
			line = re.sub('\r', '', line)
			if(state=='wait'):
				if(is_starred(line)):
					state = 'go'
					continue
			if(state=='go'):
				if(is_starred(line)):
					break
				if(is_blank(line)):
					comments[filename] += '<p>\n'
					continue
				search = get_comment(line)
				if(search):
					comment = search.groups()[0]
					if(is_blank(comment)):
						comments[filename] += '<p>\n'
					else:
						comments[filename] += comment
					continue
				break
	return comments

def print_html(comments):
	outfile = open('out.html', 'w')
	def write(str):
		outfile.write(str)
	files = []
	keys = comments.keys()
	for filename in keys:
		(head, tail) = os.path.split(filename)
		files.append(dict(path=filename, name=tail, dir=head+'/', comment=comments[filename]))
	files.sort(lambda x,y: cmp(x['name'].lower(), y['name'].lower()))
	write( """
	<html>
	<head>
	<title>Mattos Lab Scripts</title>
	<style>
	td {
		vertical-align: top;
		font-family: Courier;
		font-size: 14;
	}
	td.where {
		text-align: center;
		font-size: 12;
	}
	</style>
	</head>
	<body>
	<a name='top'></a>
	""")
	for file in files:
		write( "<a href='#%s'>%s</a><br>" % (file['path'], file['name']) )
	
	write( "<table>" )
	
	for file in files:

		write( """
		<tr>
		<th>
		""" + ("<a name='%s'>%s</a>" % (file['path'], file['name'])) + """ <a href='#top'>^</a>
		<tr>
		<td class='where'>
		""" + ("<a href='%s'>%s</a>" % (file['path'], file['path'])) + """
		<tr>
		<td>
		""" + file['comment'] + """
		""" )
		
	
	write( "</table>" )
	
	write( """
	</body>
	</html>
	""" )
	
if(__name__=='__main__'):
	print_html(gather_comments())