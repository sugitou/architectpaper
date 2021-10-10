import eel
from common import desktop
from main.aij_run import main


app_name="aij_web"
end_point="index.html"
size=(650,700)

@ eel.expose
def aij_system(id_search, csv_name, box_name):
    output_data = main(id_search, csv_name, box_name)
    return output_data


desktop.start(app_name,end_point,size)