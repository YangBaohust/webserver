import os
import time
from flask import Flask,render_template,url_for,redirect,send_from_directory
# 共享文件夹的根目录
rootdir = r'C:\Users\Administrator\Downloads\zlkt'

app = Flask(__name__)

@app.route('/doc/')
@app.route('/doc/<subdir>/')
def document(subdir=''):
    if subdir == '':
        # 名字为空，切换到根目录
        os.chdir(rootdir)
    else:
        fullname = rootdir + os.sep + subdir
        #  如果是文件，则下载
        if os.path.isfile(fullname):
            return redirect(url_for('downloader', fullname=fullname))
        #  如果是目录，切换到该目录下面
        else:
            os.chdir(fullname)
    current_dir = os.getcwd()
    current_list = os.listdir(current_dir)
    contents = []
    for i in sorted(current_list):
        fullpath = current_dir + os.sep + i
        # 如果是目录，在后面添加一个sep
        if os.path.isdir(fullpath):
            extra = os.sep
        else:
            extra = ''
        content = {}
        content['filename'] = i + extra
        content['mtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.stat(fullpath).st_mtime))
        content['size'] = str(round(os.path.getsize(fullpath) / 1024)) + 'k'
        contents.append(content)
    return render_template('shared.html', contents=contents, subdir=subdir, ossep=os.sep)

@app.route('/download/<fullname>')
def downloader(fullname):
    filename = fullname.split(os.sep)[-1]
    dirpath = fullname[:-len(filename)]
    return send_from_directory(dirpath, filename, as_attachment=True)

if __name__ == '__main__':
    app.run()
