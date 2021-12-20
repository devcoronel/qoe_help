from flask.templating import render_template

def when_upload_runs(function):

    def verify_upload(*args, **kwargs):

        with open("templates\\index.html", "r") as f:
            lines = f.readlines()
            f.close()
        
        if lines[-1] == '1':
            return render_template('index.html', route = 7)
        
        else:
            return function(*args, **kwargs)

    verify_upload.__name__ = function.__name__
    return verify_upload