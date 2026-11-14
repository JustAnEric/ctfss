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
        const decoder = new TextDecoder();
        const enProg = document.getElementById("encode-progress");
        const enProgInline = enProg.querySelector(".progress-inline");
        const enProgPercent = enProg.querySelector(".percent");
        enProgInline.style.width = "0%";
        enProgPercent.textContent = "0%";
        let buffer = "";
        
        while (true) {
            const { value, done } = await reader.read();
            if (done) {
                buffer += decoder.decode();
                break;
            }

            buffer += decoder.decode(value, { stream: true });

            let boundary;

            while ((boundary = buffer.indexOf("\n\n")) !== -1) {
                const event = buffer.slice(0, boundary);
                buffer = buffer.slice(boundary + 2);

                if (!event.startsWith("data: ")) continue;

                const data = event.slice(6);
            
                if (data.startsWith("done,")) {
                    const downloadLink = document.createElement("a");
                    downloadLink.href = data.split(",")[1];
                    downloadLink.download = "steganograph.flac";
                    downloadLink.click();
                    break;
                } else {
                    let percent = data.trim();
                    let percentAsNum = parseFloat(percent);
                    enProgInline.style.width = `${percentAsNum.toFixed(1)}%`;
                    enProgPercent.textContent = `${percentAsNum.toFixed(1)}%`;
                }
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
        const decoder = new TextDecoder();
        const dcProg = document.getElementById("decode-progress");
        const dcProgInline = dcProg.querySelector(".progress-inline");
        const dcProgPercent = dcProg.querySelector(".percent");
        dcProgInline.style.width = "0%";
        dcProgPercent.textContent = "0%";
        let buffer = "";

        while (true) {
            const { value, done } = await reader.read();
            if (done) {
                buffer += decoder.decode();
                break;
            }

            buffer += decoder.decode(value, { stream: true });

            let boundary;

            while ((boundary = buffer.indexOf("\n\n")) !== -1) {
                const event = buffer.slice(0, boundary);
                buffer = buffer.slice(boundary + 2);

                if (!event.startsWith("data: ")) continue;

                const data = event.slice(6);
                
                if (data.startsWith("done,")) {
                    const downloadLink = document.createElement("a");
                    downloadLink.href = data.split(",")[1];
                    downloadLink.download = data.split(",")[1].split('/').at(-1);
                    downloadLink.click();
                    break;
                } else {
                    let percent = data.trim();
                    let percentAsNum = parseFloat(percent);
                    dcProgInline.style.width = `${percentAsNum.toFixed(1)}%`;
                    dcProgPercent.textContent = `${percentAsNum.toFixed(1)}%`;
                }
            }
        }
    }
});