import os
from hmd_tf_bartleby.hmd_tf_bartleby import render_puml

if __name__ == "__main__":
    render_puml(os.environ.get("PUML_FILES").split(","))
