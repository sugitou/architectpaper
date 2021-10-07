import eel
from common import desktop
from main.aij_run import main


app_name="aij_web"
end_point="index.html"
size=(650,600)

@ eel.expose
def rakuten_system(kw_search, csv_name, box_name, select_api):
    output_data = main()
    return output_data


desktop.start(app_name,end_point,size)