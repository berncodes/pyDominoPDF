__license__ = 'GNU Public License Version 3, https://www.gnu.org/licenses/gpl-3.0.en.html'
__copyright__ = "Copyright (C) 2020, dev@BernCodes.com - Released under terms of the GPLv3 License"

from flask import Flask, render_template, request, after_this_request, send_file
import os
from tempfile import mkstemp
from pyDominoPDF import pyDominoPDF
from datetime import datetime
import time

#Fall back defaults
def_Page_Height = 8.5
def_Page_Width = 11
def_Page_Margin = 0.5
def_doc_RowSpacing = 2.5
cookie_max_age = 360*24*60*60


index_py = os.path.realpath(__file__)
build_var = time.strftime("%Y%m%d-%H%M", time.gmtime(os.path.getmtime(index_py)))


app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def index():
    if (request.method == "GET"):
        cookies = request.cookies.to_dict()
        variable_list = {'build_var':build_var} 
        
        if ('remember' not in cookies): 
            variable_list['remember'] = str(False)
        elif cookies['remember'] == 'True':
            variable_list.update(cookies)

        #Sets Defaults if not found (either not saved or not remembered)
        if ('page_height' not in variable_list) : variable_list['page_height'] = str(def_Page_Height)
        if ('page_width' not in variable_list) : variable_list['page_width'] = str(def_Page_Width)

        if ('page_margin_top' not in variable_list) : variable_list['page_margin_top'] = str(def_Page_Margin)
        if ('page_margin_left' not in variable_list) : variable_list['page_margin_left'] = str(def_Page_Margin)
        if ('page_margin_right' not in variable_list) : variable_list['page_margin_right'] = str(def_Page_Margin)
        if ('page_margin_bottom' not in variable_list) : variable_list['page_margin_bottom'] = str(def_Page_Margin)

        if ('center_horizontal' not in variable_list) : variable_list['center_horizontal'] = "False"
        if ('center_vertical' not in variable_list) : variable_list['center_vertical'] = "False"

        if ('page_count' not in variable_list) : variable_list['page_count'] = str(1)
        if ('page_unit' not in variable_list) : variable_list['page_unit'] = "inch"
        if ('row_spacing' not in variable_list) : variable_list['row_spacing'] = str(def_doc_RowSpacing)
        if ('randomize' not in variable_list) : variable_list['randomize'] = "True"
        if ('scale_verification' not in variable_list) : variable_list['scale_verification'] = "False"
        if ('margin_bounding' not in variable_list) : variable_list['margin_bounding'] = "False"
        if ('radius_corners' not in variable_list) : variable_list['radius_corners'] = "True"
        if ('download' not in variable_list) : variable_list['download'] = "True"

        if ('x_stated' not in variable_list) : variable_list['x_stated'] = str(1.7)
        if ('x_measured' not in variable_list) : variable_list['x_measured'] = str(1.7)
        if ('y_stated' not in variable_list) : variable_list['y_stated'] = str(0.5)
        if ('y_measured' not in variable_list) : variable_list['y_measured'] = str(0.5)

        return render_template("form.html", **variable_list)

    if (request.method == "POST"):
        output = pyDominoPDF()


        #original real unit handling
        doc_Unit  = request.form.get('unit','inch', type=str)
        output.Units = doc_Unit

        page_Height =  request.form.get('pg_Height', 0, type=float)
        output.Page.Height = (page_Height)

        page_Width  = request.form.get('pg_Width', 0, type=float)
        output.Page.Width = (page_Width)

        page_margin_top = request.form.get('pg_margin_top', 0, type=float)
        if (page_margin_top < 0): page_margin_top = def_Page_Margin
        output.Page.Margin.Top = (page_margin_top)

        page_margin_left = request.form.get('pg_margin_left', 0, type=float)
        if (page_margin_left < 0): page_margin_left = def_Page_Margin
        output.Page.Margin.Left = (page_margin_left)

        page_margin_right = request.form.get('pg_margin_right', 0, type=float)
        if (page_margin_right < 0): page_margin_right = page_margin_right
        output.Page.Margin.Right = (page_margin_right)

        page_margin_bottom = request.form.get('pg_margin_bottom', 0, type=float)
        if (page_margin_bottom < 0): page_margin_bottom = def_Page_Margin
        output.Page.Margin.Bottom = (page_margin_bottom)

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

        if (request.form.get('chk_center_vertical', '') == ''):
            output.Page.Center_Vertical = False
        else:
            output.Page.Center_Vertical = True

        if (request.form.get('chk_center_horizontal', '') == ''):
            output.Page.Center_Horizontal = False
        else:
            output.Page.Center_Horizontal = True

        if (request.form.get('chk_Remember', '') == ''):
            bCookies = False
        else:
            bCookies = True


        x_measure = request.form.get('scale_measured_X', 1, type=float)
        x_stated = request.form.get('scale_stated_X', 1, type=float)

        if (x_measure > 0) & (x_stated > 0):
             x_scale = x_stated / x_measure
        else:
            x_scale = 1.0

        if (x_scale > 2): x_scale = 2

        output.Page.X_ScaleFactor = x_scale

        y_measure = request.form.get('scale_measured_Y', 1, type=float)
        y_stated = request.form.get('scale_stated_Y', 1, type=float)
        
        if (y_measure > 0) & (y_stated > 0):
             y_scale = y_stated / y_measure
        else:
            y_scale = 1.0

        if (y_scale > 2): y_scale = 2

        output.Page.Y_ScaleFactor = y_scale

        WDir = os.path.join(app.root_path, "output")
        temp_fd, temp_path = mkstemp(".pdf","", WDir)
        os.close(temp_fd)
        output.SavePDF(temp_path)
        

        date_time = datetime.now().strftime("%Y%m%d-%H%M")
        aname = ("Output-{}.pdf" . format(date_time))

        @after_this_request
        def delete_after_send(response):
            #Windows cannot delete the temp file as flask still has a handle on it
            #Folder will have to be cleaned up with a scheduled task
            if (os.name != 'nt'):
                 os.remove(temp_path)

            
            if (bCookies == True):
                response.set_cookie("page_height", str(page_Height), cookie_max_age)
                response.set_cookie("page_width", str(page_Width), cookie_max_age)

                response.set_cookie("page_margin_top", str(output.Page.Margin.Top), cookie_max_age)
                response.set_cookie("page_margin_left", str(output.Page.Margin.Left), cookie_max_age)
                response.set_cookie("page_margin_right", str(output.Page.Margin.Right), cookie_max_age)
                response.set_cookie("page_margin_bottom", str(output.Page.Margin.Bottom), cookie_max_age)

                response.set_cookie("center_vertical", str(output.Page.Center_Vertical), cookie_max_age)
                response.set_cookie("center_horizontal", str(output.Page.Center_Horizontal), cookie_max_age)

                response.set_cookie("page_count", str(doc_PageCount), cookie_max_age)
                response.set_cookie("page_unit", str(doc_Unit), cookie_max_age)
                response.set_cookie("row_spacing", str(doc_Rows), cookie_max_age)
                response.set_cookie("randomize", str(output.Randomize), cookie_max_age)
                response.set_cookie("scale_verification", str(output.VerificationScale), cookie_max_age)
                response.set_cookie("margin_bounding", str(output.MarginBorder), cookie_max_age)
                response.set_cookie("radius_corners", str(output.RadiusCorners), cookie_max_age)
                response.set_cookie("download", str(bDownload), cookie_max_age)
                response.set_cookie("remember", str(bCookies), cookie_max_age)

                response.set_cookie("x_stated", str(x_stated), cookie_max_age)
                response.set_cookie("x_measured", str(x_measure), cookie_max_age)

                response.set_cookie("y_stated", str(y_stated), cookie_max_age)
                response.set_cookie("y_measured", str(y_measure), cookie_max_age)

            else:
                dcookies = request.cookies.to_dict()
                for d in (dcookies):
                    response.set_cookie(d, expires=0)




            return response
        
        return download_file(temp_path, bDownload, aname)

        del output


        

def download_file(path, attachment, filename):
    response = send_file(filename_or_fp=path, as_attachment=attachment, attachment_filename=filename, mimetype='application/pdf', cache_timeout=-1)
    
    return response

    