import markdown
from flask import Flask, flash, redirect, url_for
from flask import render_template, safe_join
from flask import Markup
from patch import Proxied
import os
_cdir="content"
conf={ 
    '_cdir' : "content" 
}

app = Flask(__name__)
app.wsgi_app = Proxied(app.wsgi_app)
app.secret_key='tell me muse of the man of so many ways'
## rendering dirs
def norm_path(_dir="/", initial_req=None, conf=conf):
    """takes a path and return in the directory of the
    content: 
    * category: all the categories;
    * _status   if filled, tell something
    * cur_dir:  the current working dir
    * url       the url for rendering"""

    full_path=os.path.join(conf["_cdir"], _dir)
    okay=False
    if os.path.isdir(full_path):
        cur_dir=full_path
        md=os.path.join(full_path, "index.md") 
        url=_dir
        okay=True
    
    # not a dir, is it a partial path to a md?

    if not okay and os.path.exists("%s.md"%full_path):
        md="%s.md"% full_path
        cur_dir=os.path.dirname(full_path)
        url=full_path
        okay=True
    if okay:
        category =  [ 
            uri for uri in os.listdir(cur_dir) if
            os.path.isdir( os.path.join(cur_dir,uri))] 
        return dict(
            md=md,
            url=url,
            cur_dir=cur_dir,
            category = category,
            _error=initial_req
            )
    else:
        return norm_path(os.path.dirname(_dir), initial_req or _dir)
            

    
@app.route("/r/")
@app.route('/r/<path:_path>') 
def markdown(conf=conf,_path="/index"):
    dir_info=norm_path(_path) 
    content=";)"
    try: 
        with open(dir_info["md"]) as md_c:
            content=md_c.read()
    except:
        flash("bouhouhouh","error")
    return content + str(dir_info)
    


if '__main__' == __name__ :
    app.run(port=5005,debug=False)
