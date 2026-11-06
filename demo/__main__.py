import os, asyncio, tempfile, io, shutil
from pathlib import Path
from uvicorn import run

from __init__ import c_stream_async, d_stream_async, magicunpack, magicpack
from quart import Quart, render_template, request, jsonify, Response
from aiofiles import open as openasync

basedir = Path(os.path.abspath(os.path.dirname(__file__)))

SERVER_MAX_FILE_UPLOAD_SIZE = 1024.0 # MB
SERVER_MAX_FILE_ENCODE_UPLOAD_SIZE = 1.0
SERVER_MAX_FILE_DECODE_UPLOAD_SIZE = 1024.0
CONVERTED_FOLDER = basedir / "static" / "userassets" / "converted"
UPLOADS_FOLDER = basedir / "uploads"

app = Quart(__name__, template_folder=basedir / "templates", static_folder=basedir / "static", static_url_path="/")

app.config["MAX_CONTENT_LENGTH"] = SERVER_MAX_FILE_UPLOAD_SIZE * 1024 * 1024
app.config["UPLOAD_FOLDER"] = UPLOADS_FOLDER
app.config["CONVERTED_FOLDER"] = CONVERTED_FOLDER
app.config["SECRET_KEY"] = "this_is_a_secret_change_this_please"

@app.route("/")
async def index():
    return await render_template("index.html", max_filesize=app.config["MAX_CONTENT_LENGTH"], max_encode_filesize=SERVER_MAX_FILE_ENCODE_UPLOAD_SIZE * 1024 * 1024, max_decode_filesize=SERVER_MAX_FILE_DECODE_UPLOAD_SIZE * 1024 * 1024)

@app.post("/api/encode")
async def encode_api():
    if request.content_length > SERVER_MAX_FILE_ENCODE_UPLOAD_SIZE * 1024 * 1024:
        return jsonify({"error": "File size exceeds the maximum allowed size for encoding"}), 400
    
    if "file" not in (await request.files):
        return jsonify({"error": "No file part"}), 400

    file = (await request.files)["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    temp = tempfile.NamedTemporaryFile(
        mode="w+b",
        delete=False,
        suffix=".bin",
    )

    if file:
        try:
            shutil.copyfileobj(file.stream, temp)
            temp.close()
        
            async def generate():
                try:
                    output_file_path = CONVERTED_FOLDER / f"encoded_{file.filename}.flac"
                    user_path = f"/userassets/converted/encoded_{file.filename}.flac"
                    with open(temp.name, "rb") as input_file:
                        with open(output_file_path, "wb") as output_file:
                            async for percent in c_stream_async(input_file, output_file):
                                yield f"data: {percent}\n\n"
                            
                            yield f"data: done,{user_path}\n\n" # give over the encoded file
                        
                        with open(output_file_path, "rb") as output_file:
                            # add magic to the start of the file
                            data = output_file.read()
                            packed_data = magicpack(data, p=file.filename)
                            with open(output_file_path, "wb") as final_output_file:
                                final_output_file.write(packed_data)
                finally: os.unlink(temp.name)
        
            return Response(generate(), mimetype="text/event-stream")
        except Exception:
            temp.close()
            os.unlink(temp.name)
            raise

    return jsonify({"error": "File encoding failed"}), 500

@app.post("/api/decode")
async def decode_api():
    if request.content_length > SERVER_MAX_FILE_DECODE_UPLOAD_SIZE * 1024 * 1024:
        return jsonify({"error": "File size exceeds the maximum allowed size for decoding"}), 400
    
    if "file" not in (await request.files):
        return jsonify({"error": "No file part"}), 400

    file = (await request.files)["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    elif not file.filename.lower().strip().endswith((".flac", ".ctfss")):
        return jsonify({"error": "Invalid file type for decoding"}), 400
    
    temp = tempfile.NamedTemporaryFile(
        mode="w+b",
        delete=False,
        suffix=".flac",
    )
    temp2 = None

    if file:
        try:
            shutil.copyfileobj(file.stream, temp)
            temp.close()
        
            async def generate():
                try:
                    with open(temp.name, "rb") as input_file:
                        global n,d
                        try:
                            n, d = magicunpack(input_file.read())
                        except ValueError as e:
                            print(f"Error unpacking magic: {e}")
                            yield "data: error,Invalid file format for decoding\n\n"
                            return
                        
                        temp2 = tempfile.NamedTemporaryFile(
                            mode="w+b",
                            delete=False,
                            suffix=".flac",
                        )
                        
                        shutil.copyfileobj(io.BytesIO(d), temp2)
                        temp2.flush()
                        temp2.close()
                        
                        output_file_path = CONVERTED_FOLDER / f"decoded_{n}"
                        user_path = f"/userassets/converted/decoded_{n}"
                        
                        with open(output_file_path, "wb") as output_file:
                            async for percent in d_stream_async(temp2.name, output_file):
                                yield f"data: {percent}\n\n"
                            
                            yield f"data: done,{user_path}\n\n" # give over the decoded file
                finally: 
                    os.unlink(temp.name)
                    os.unlink(temp2.name)

            return Response(generate(), mimetype="text/event-stream")
        except Exception:
            temp.close()
            temp2.close()
            os.unlink(temp.name)
            os.unlink(temp2.name)
            raise

    return jsonify({"error": "File decoding failed"}), 500

run(app, host="0.0.0.0", port=5000)