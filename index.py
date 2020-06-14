from flask import Flask, render_template, request, after_this_request, send_file
import os.path
from tempfile import mkstemp
from pyDominoPDF import pyDominoPDF

#Fall back defaults
def_Page_Height = 8.5
def_Page_Width = 11
def_Page_Margin = 0.5
def_doc_RowSpacing = 2.5


app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if (request.method == "GET"):
        return render_template("form.html")

    if (request.method == "POST"):
        output = pyDominoPDF()


        #original real unit handling
        doc_Unit  = request.form.get('unit','inch', type=str)
        output.Units = doc_Unit

        page_Height =  request.form.get('pg_Height', 0, type=float)
        #if (page_Height <= 0): page_Height = def_Page_Height
        #if (page_Height > 96): page_Height = 96
        output.Page.Height = (page_Height)

        page_Width  = request.form.get('pg_Width', 0, type=float)
        #if (page_Width <= 0): page_Width = def_Page_Width
        #if (page_Width > 96): page_Width = 96
        output.Page.Width = (page_Width)

        page_Margin = request.form.get('pg_Margin', 0, type=float)
        if (page_Margin < 0): page_Margin = def_Page_Margin
        output.Page.Margin = (page_Margin)

        doc_PageCount  = request.form.get('pg_Pages', 1, type=int)
        if (doc_PageCount > 20): doc_PageCount = 25
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

        x_measure = request.form.get('scale_measured_X', 1, type=float)
        x_stated = request.form.get('scale_stated_X', 1, type=float)
        output.Page.X_ScaleFactor = x_stated / x_measure

        y_measure = request.form.get('scale_measured_Y', 1, type=float)
        y_stated = request.form.get('scale_stated_Y', 1, type=float)
        output.Page.Y_ScaleFactor = y_stated / y_measure


        WDir = os.path.join(app.root_path, "output")
        fd, tpath = mkstemp(".pdf","", WDir)

        output.SavePDF(tpath)
        del output

        @after_this_request
        def remove_file(response):
            os.close(fd)
            os.remove(tpath)
            return response
        return send_file(tpath, cache_timeout=-1)


        return (tpath)
    return ()