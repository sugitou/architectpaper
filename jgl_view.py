import eel
from common import desktop
from main.jgl_run import main


app_name="jgl_web"
end_point="index.html"
size=(650,700)

@ eel.expose
def jgl_system(csv_name, box_name):
    output_data = main(csv_name, box_name)
    return output_data


desktop.start(app_name,end_point,size)