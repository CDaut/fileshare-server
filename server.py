from flask import Flask, render_template, send_from_directory
import os
import netifaces

app = Flask(__name__)

##############
FILEDIR = './uploads'
PORT = 8080
##############

iface_blacklist = ['lo']


@app.route('/')
def index():
    if not os.path.exists(FILEDIR):
        return "Please create a \"uploads\" directory in this directory, containing the files you whish to upload."
    files = os.listdir(FILEDIR)
    files.sort()
    interface_dict = {}

    interfaces = netifaces.interfaces()
    for interface in interfaces:
        if interface not in iface_blacklist:
            addrs = netifaces.ifaddresses(interface)

            if netifaces.AF_INET in addrs:
                inet_addresses = addrs[netifaces.AF_INET]

                for address in inet_addresses:
                    interface_dict[interface] = address['addr']

    print(interface_dict)
    return render_template('index.html', files=files, ifaces=interface_dict)


@app.route('/<path:filename>')
def file(filename):
    uploads = os.path.join(app.root_path, 'uploads')
    return send_from_directory(uploads, filename)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
