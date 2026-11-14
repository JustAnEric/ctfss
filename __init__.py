if __name__ == "__main__":
    print("This is the ctfss package. It is not meant to be run directly.")
    exit(1)

import asyncio
import threading
import soundfile
import numpy
import os
import sys
import math
import io
import zlib
import struct
from _utils import bcolors
from typing import Generator


def magicpack(b: bytes, p: str = ""):
    # adds magic to the start of bytes
    MAGIC = b"CTFSS"
    encname = p.encode("utf-8")
    if len(encname) > 255:
        raise ValueError("path is too long")
    H = MAGIC + struct.pack(">BI", len(encname), len(b)) + encname
    return H + b


def magicunpack(b: bytes):
    if b[:5] != b"CTFSS":
        raise ValueError("invalid magic header")
    plen = struct.unpack(">B", b[5:6])[0]
    blen = struct.unpack(">I", b[6:10])[0]
    name = b[10 : 10 + plen].decode()
    data = b[10 + plen : 10 + plen + blen]
    if len(data) != blen:
        raise ValueError("invalid data length")
    return name, data


def i():
    print("Welcome to interactive mode. Type 'help' for a list of commands.")
    while True:
        prompt = input(f"{bcolors.GREEN}ctfss{bcolors.ENDC}> ").strip()
        args = prompt.split()
        args = [arg.lower() for i, arg in enumerate(args) if i == 0]
        if args[0] == "exit":
            print("Exiting interactive mode.")
            break
        elif args[0] == "help":
            commands = {
                "help": {
                    "description": "Show this help message",
                    "usage": "help",
                    "arguments": [],
                },
                "make": {
                    "description": "Create a new steganograph",
                    "usage": "make -i <input> -o <output>",
                    "arguments": [
                        {"name": "-i", "description": "Specify the input file"},
                        {"name": "-o", "description": "Specify the output file"},
                    ],
                },
                "decode": {
                    "description": "Decode a steganograph",
                    "usage": "decode -i <input> -o <output>",
                    "arguments": [
                        {"name": "-i", "description": "Specify the input file"},
                        {"name": "-o", "description": "Specify the output file"},
                    ],
                },
                "exit": {
                    "description": "Exit interactive mode",
                    "usage": "exit",
                    "arguments": [],
                },
            }
            print("Available commands:")
            for command, info in commands.items():
                print(
                    f"  {bcolors.BOLD+bcolors.HEADER}{command}{bcolors.ENDC}: {info['description']}"
                )
                print(f"    Usage: {info['usage']}")
                if info["arguments"]:
                    print("    Arguments:")
                    for arg in info["arguments"]:
                        print(f"      {arg['name']}: {arg['description']}")
        elif args[0] == "make":
            input_file = (
                args[1]
                if len(args) > 1
                else input("Enter the input file path: ").strip()
            )
            output_file = (
                args[2]
                if len(args) > 2
                else input("Enter the output file path: ").strip()
            )
            if not input_file:
                print(f"{bcolors.RED}Error: Input file is required.{bcolors.ENDC}")
                continue
            if not output_file:
                print(f"{bcolors.RED}Error: Output file is required.{bcolors.ENDC}")
                continue
            try:
                for percent in c_stream(
                    open(input_file, "rb"), open(output_file, "wb")
                ):
                    sys.stdout.write(
                        f"\r{bcolors.CYAN}Progress: {percent:.2f}%{bcolors.ENDC}"
                    )
                    sys.stdout.flush()
                print(
                    f"\n{bcolors.GREEN}Successfully created steganograph: {output_file}{bcolors.ENDC}"
                )
            except Exception as e:
                print(f"{bcolors.RED}Error: {e}{bcolors.ENDC}")
        elif args[0] == "decode":
            input_file = (
                args[1]
                if len(args) > 1
                else input("Enter the input file path: ").strip()
            )
            output_file = (
                args[2]
                if len(args) > 2
                else input("Enter the output file path: ").strip()
            )
            if not input_file:
                print(f"{bcolors.RED}Error: Input file is required.{bcolors.ENDC}")
                continue
            if not output_file:
                print(f"{bcolors.RED}Error: Output file is required.{bcolors.ENDC}")
                continue
            try:
                for percent in d_stream(
                    open(input_file, "rb"), open(output_file, "wb")
                ):
                    sys.stdout.write(
                        f"\r{bcolors.CYAN}Progress: {percent:.2f}%{bcolors.ENDC}"
                    )
                    sys.stdout.flush()
                print(
                    f"\n{bcolors.GREEN}Successfully decoded steganograph: {output_file}{bcolors.ENDC}"
                )
            except Exception as e:
                print(f"{bcolors.RED}Error: {e}{bcolors.ENDC}")
        else:
            print(f"{bcolors.RED}Unknown command: {args[0]}{bcolors.ENDC}")


def t(freq, dur, sr=44100):
    ns = int(sr * dur)
    t = numpy.linspace(0, dur, ns, endpoint=False)
    return numpy.sin(2 * numpy.pi * freq * t)


def cc(bytes_data: bytes):
    # had to do some digging for this function!! stupid ord
    bytes_data = zlib.compress(bytes_data)
    for byte in bytes_data:
        for i in range(8):
            yield (byte >> (7 - i)) & 1


def c(bits: list[int], sr=44100):
    samplespb = int(sr * 0.04)
    bta = numpy.fromiter(bits, dtype=numpy.uint8)
    if bta.size == 0:
        return b""
    t = numpy.arange(samplespb, dtype=numpy.float32) / sr
    wf = numpy.array(
        [
            500,
            1000,
            1500,
            2000,
            2500,
            3000,
            3500,
            4000,
            4500,
            5000,
            5500,
            6000,
            6500,
            7000,
            7500,
            8000,
            8500,
            9000,
            9500,
            10000,
            10500,
            11000,
            11500,
            12000,
            12500,
            13000,
            13500,
            14000,
            14500,
            15000,
            15500,
            16000,
            16500,
            17000,
            17500,
            18000,
            18500,
            19000,
            19500,
            20000,
        ]
    )

    waves = numpy.sin(2 * numpy.pi * wf[:, None] * t).astype(numpy.float32)
    padding = (-bta.size) % 40
    # a = numpy.empty((bta.size, samplespb), dtype=numpy.float32)
    if padding:
        bta = numpy.pad(bta, (0, padding))
    groups = bta.reshape(-1, 40)
    a = (groups.T[:, :, None] * waves[:, None, :]).sum(axis=0)
    a /= 40
    membuf = io.BytesIO()
    membuf.name = "audio.flac"
    soundfile.write(membuf, a.reshape(-1), sr, format="FLAC")
    fb = membuf.getvalue()
    return fb


def c_stream(
    input_file,
    output_file,
    sr=44100,
    sym_dur=0.04,
    chnk_size_bytes=65536,
    sym_per_batch=256,
) -> Generator[float, None, None]:
    total_size = os.fstat(input_file.fileno()).st_size
    processed = 0
    freq = numpy.arange(500, 20001, 500, dtype=numpy.float32)
    bch = len(freq)
    smpl_p_sym = int(sr * sym_dur)

    if smpl_p_sym <= 0:
        raise ValueError("invalid symbol duration")

    if freq[-1] >= sr / 2:
        raise ValueError("frequencies exceed the nyquist limit")

    t = numpy.arange(smpl_p_sym, dtype=numpy.float32) / sr

    w = numpy.sin(2 * numpy.pi * freq[:, None] * t).astype(numpy.float32)
    p = numpy.empty(0, dtype=numpy.uint8)
    compressor = zlib.compressobj()

    def encode(data, audio):
        nonlocal p
        if not data:
            return
        bits = numpy.unpackbits(numpy.frombuffer(data, dtype=numpy.uint8))
        if p.size:
            bits = numpy.concatenate((p, bits))

        complete_size = (bits.size // bch) * bch
        p = bits[complete_size:].copy()

        if complete_size == 0:
            return

        groups = bits[:complete_size].reshape(-1, bch)

        for start in range(0, groups.shape[0], sym_per_batch):
            batch = groups[start : start + sym_per_batch]

            audio_data = (batch.astype(numpy.float32) @ w) / bch

            audio.write(audio_data.reshape(-1))

    with soundfile.SoundFile(
        output_file,
        mode="w",
        samplerate=sr,
        channels=1,
        format="FLAC",
    ) as audio:
        while True:
            data = input_file.read(chnk_size_bytes)
            if not data:
                break
            processed += len(data)
            compressed = compressor.compress(data)
            encode(compressed, audio)
            yield (processed / total_size * 100) if total_size else 100

        encode(compressor.flush(), audio)

        if p.size:
            padded = numpy.pad(p, (0, bch - p.size))
            audio_data = (padded.reshape(1, bch).astype(numpy.float32) @ w) / bch
            audio.write(audio_data.reshape(-1))

    yield 100.0


def d_stream(
    input_file,
    output_file,
    sym_dur=0.04,
    sym_per_batch=256,
    rel_threshold=0.15,
    min_peak=5.0,
):
    freq = numpy.arange(500, 20001, 500, dtype=numpy.float32)
    bch = len(freq)
    decompressor = zlib.decompressobj()

    with soundfile.SoundFile(input_file, mode="r") as audio:
        sr = audio.samplerate
        if audio.channels != 1:
            raise ValueError("input audio must be mono")
        smpl_p_sym = int(sr * sym_dur)
        if smpl_p_sym <= 0:
            raise ValueError("invalid symbol duration")
        if freq[-1] >= sr / 2:
            raise ValueError("frequencies exceed the nyquist limit")

        total_frames = audio.frames
        processed_frames = 0

        window = numpy.hanning(smpl_p_sym).astype(numpy.float32)
        bins = numpy.rint(freq * smpl_p_sym / sr).astype(numpy.intp)

        while True:
            ss = audio.read(
                frames=smpl_p_sym * sym_per_batch, dtype="float32", always_2d=True
            )
            if ss.shape[0] == 0:
                break

            processed_frames += ss.shape[0]

            ss = ss[:, 0]
            complete_size = (ss.size // smpl_p_sym) * smpl_p_sym

            if complete_size == 0:
                yield (
                    min(processed_frames / total_frames * 100, 100)
                    if total_frames
                    else 100.0
                )
                continue

            groups = ss[:complete_size].reshape(-1, smpl_p_sym)
            spectrum = numpy.abs(
                numpy.fft.rfft(
                    groups * window[None, :],
                    axis=1,
                )
            )
            magnitudes = spectrum[:, bins]
            strongest = magnitudes.max(axis=1)

            threshold = numpy.maximum(
                strongest[:, None] * rel_threshold,
                min_peak,
            )
            bits = magnitudes > threshold
            packed = numpy.packbits(
                bits.reshape(-1).astype(numpy.uint8),
                bitorder="big",
            )
            decoded = decompressor.decompress(packed.tobytes())
            if decoded:
                output_file.write(decoded)

            yield (
                min(processed_frames / total_frames * 100, 100)
                if total_frames
                else 100.0
            )

        remaining = decompressor.flush()
        if remaining:
            output_file.write(remaining)
        if not decompressor.eof:
            raise ValueError("incomplete or corrupted zlib stream")

        yield 100.0


def d(input_data: bytes, output_file: str = None):
    ab = io.BytesIO(input_data)
    ab.name = "audio.flac"
    data, samplerate = soundfile.read(ab, dtype="float32", always_2d=False)
    samplespb = int(samplerate * 0.04)
    chl = len(data) // samplespb
    bb = []
    freq = [
        500,
        1000,
        1500,
        2000,
        2500,
        3000,
        3500,
        4000,
        4500,
        5000,
        5500,
        6000,
        6500,
        7000,
        7500,
        8000,
        8500,
        9000,
        9500,
        10000,
        10500,
        11000,
        11500,
        12000,
        12500,
        13000,
        13500,
        14000,
        14500,
        15000,
        15500,
        16000,
        16500,
        17000,
        17500,
        18000,
        18500,
        19000,
        19500,
        20000,
    ]
    for i in range(chl):
        chunk = data[i * samplespb : (i + 1) * samplespb]
        chunk = chunk * numpy.hanning(len(chunk))  # hann window
        spectrum = numpy.abs(numpy.fft.rfft(chunk))
        bins = numpy.fft.rfftfreq(len(chunk), d=1 / samplerate)
        magnitudes = []
        for f in freq:
            index = numpy.argmin(numpy.abs(bins - f))
            magnitudes.append(spectrum[index])

        strongest = max(magnitudes)
        if strongest < 10.0:
            bb.extend([0] * len(freq))
            continue
        for magnitude in magnitudes:
            bb.append(int(magnitude > strongest * 0.15))

    usable = (len(bb) // 40) * 40
    decoded = numpy.packbits(
        numpy.array(bb[:usable], dtype=numpy.uint8), bitorder="big"
    ).tobytes()
    decoded = zlib.decompress(decoded)

    if output_file:
        with open(output_file, "wb") as f:
            f.write(decoded)

    return decoded


async def d_stream_async(
    input_file,
    output_file,
    sym_dur=0.04,
    sym_per_batch=256,
    rel_threshold=0.15,
    min_peak=5.0,
):
    loop = asyncio.get_running_loop()
    queue = asyncio.Queue()

    def worker():
        try:
            for progress in d_stream(
                input_file, output_file, sym_dur, sym_per_batch, rel_threshold, min_peak
            ):
                asyncio.run_coroutine_threadsafe(
                    queue.put(("progress", progress)),
                    loop,
                ).result()
            asyncio.run_coroutine_threadsafe(
                queue.put(("done", None)),
                loop,
            ).result()
        except Exception as exc:
            asyncio.run_coroutine_threadsafe(
                queue.put(("error", exc)),
                loop,
            ).result()

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()

    while True:
        event, value = await queue.get()
        if event == "progress":
            yield value
        elif event == "error":
            raise value
        elif event == "done":
            break

    await asyncio.to_thread(thread.join)


async def c_stream_async(input_file, output_file, **kwargs):
    loop = asyncio.get_running_loop()
    queue = asyncio.Queue()

    def worker():
        try:
            for progress in c_stream(input_file, output_file, **kwargs):
                asyncio.run_coroutine_threadsafe(
                    queue.put(("progress", progress)),
                    loop,
                ).result()
            asyncio.run_coroutine_threadsafe(
                queue.put(("done", None)),
                loop,
            ).result()
        except Exception as exc:
            asyncio.run_coroutine_threadsafe(
                queue.put(("error", exc)),
                loop,
            ).result()

    thread = threading.Thread(target=worker, daemon=True)
    thread.start()

    while True:
        event, value = await queue.get()
        if event == "progress":
            yield value
        elif event == "error":
            raise value
        elif event == "done":
            break

    await asyncio.to_thread(thread.join)
