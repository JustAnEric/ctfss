const encodeForm = document.querySelector("#encode-form");
const decodeForm = document.querySelector("#decode-form");

encodeForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(encodeForm);
    const response = await fetch("/api/encode", {
        method: "POST",
        body: formData,
    });

    if (response.ok) {
        // data stream

        const reader = response.body.getReader();
        const { value: firstChunk, done: firstDone } = await reader.read();
        if (firstDone) {
            console.error("No data received from the server.");
            return;
        }
        document.getElementById("encode-progress").textContent = "0%";
        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            const dd = new TextDecoder().decode(value);
            if (dd.startsWith("data: done")) {
                const downloadLink = document.createElement("a");
                downloadLink.href = dd.split(",")[1];
                downloadLink.download = "steganograph.flac";
                downloadLink.click();
                break;
            } else {
                document.getElementById("encode-progress").textContent = `${dd.split(":",2)[1]}%`;
            }
        }
    }
});

decodeForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(decodeForm);

    const response = await fetch("/api/decode", {
        method: "POST",
        body: formData,
    });

    if (response.ok) {
        // data stream

        const reader = response.body.getReader();
        const { value: firstChunk, done: firstDone } = await reader.read();
        if (firstDone) {
            console.error("No data received from the server.");
            return;
        }

        document.getElementById("decode-progress").textContent = "0%";
        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            const dd = new TextDecoder().decode(value);
            if (dd.startsWith("data: done")) {
                const downloadLink = document.createElement("a");
                downloadLink.href = dd.split(",")[1];
                downloadLink.download = dd.split(",")[1].split('/').at(-1);
                downloadLink.click();
                break;
            } else {
                document.getElementById("decode-progress").textContent = `${dd.split(":",2)[1]}%`;
            }
        }
    }
});