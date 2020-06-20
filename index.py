__license__ = 'GNU Public License Version 3, https://www.gnu.org/licenses/gpl-3.0.en.html'
__copyright__ = "Copyright (C) 2020, dev@BernCodes.com - Released under terms of the GPLv3 License"

from flask import Flask, render_template, request, after_this_request, send_file
import os.path
from tempfile import mkstemp
from pyDominoPDF import pyDominoPDF
from datetime import datetime
import time

#Fall back defaults
def_Page_Height = 8.5
def_Page_Width = 11
def_Page_Margin = 0.5
def_doc_RowSpacing = 2.5

build_var = time.strftime("%Y%m%d-%H%M", time.gmtime(os.path.getmtime("index.py")))


app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def index():
    if (request.method == "GET"):
        return render_template("form.html", build_var=build_var)

    if (request.method == "POST"):
        output = pyDominoPDF()


        #original real unit handling
        doc_Unit  = request.form.get('unit','inch', type=str)
        output.Units = doc_Unit

        page_Height =  request.form.get('pg_Height', 0, type=float)
        output.Page.Height = (page_Height)

        page_Width  = request.form.get('pg_Width', 0, type=float)
        output.Page.Width = (page_Width)

        page_Margin = request.form.get('pg_Margin', 0, type=float)
        if (page_Margin < 0): page_Margin = def_Page_Margin
        output.Page.Margin = (page_Margin)

        doc_PageCount  = request.form.get('pg_Pages', 1, type=int)
        if (doc_PageCount > 20): doc_PageCount = 20
        output.Page.Count = doc_PageCount

        doc_Rows  = request.form.get('doc_RowSpacing', def_doc_RowSpacing, type=float)
        output.RowSpacing = (doc_Rows)

        if (request.form.get('chk_DominoValues', '') == ''):
            output.PrintValues = False
        else:
            output.PrintValues = True

        if (request.form.get('chk_ScaleVerify', '') == ''):
            output.VerificationScale = False
        else:
            output.VerificationScale = True

        if  (request.form.get('chk_Random', '') == ''):
            output.Randomize = False
        else:
            output.Randomize = True

        if  (request.form.get('chk_Margin_Bounding', '') == ''):
            output.MarginBorder = False
        else:
            output.MarginBorder = True

        if  (request.form.get('chk_Radius_Corners', '') == ''):
            output.RadiusCorners = False
        else:
            output.RadiusCorners = True

        if  (request.form.get('chk_Download', '') == ''):
            bDownload = False
        else:
            bDownload = True

        x_measure = request.form.get('scale_measured_X', 1, type=float)
        x_stated = request.form.get('scale_stated_X', 1, type=float)
        output.Page.X_ScaleFactor = x_stated / x_measure

        y_measure = request.form.get('scale_measured_Y', 1, type=float)
        y_stated = request.form.get('scale_stated_Y', 1, type=float)
        output.Page.Y_ScaleFactor = y_stated / y_measure


        WDir = os.path.join(app.root_path, "output")
        temp_fd, temp_path = mkstemp(".pdf","", WDir)
        os.close(temp_fd)
        output.SavePDF(temp_path)
        del output

        date_time = datetime.now().strftime("%Y%m%d-%H%M")
        aname = ("Output-{}.pdf" . format(date_time))

        @after_this_request
        def delete_after_send(response):
            #Windows cannot delete the temp file as flask still has a handle on it
            #Folder will have to be cleaned up with a scheduled task
            if (os.name != 'nt'):
                 os.remove(temp_path)
            
            return response
        
        return send_file(filename_or_fp=temp_path, as_attachment=bDownload, attachment_filename=aname, mimetype='application/pdf', cache_timeout=-1)

        #return (temp_path)
    return ()