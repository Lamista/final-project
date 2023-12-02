document.addEventListener("DOMContentLoaded", (event) => {
    document.querySelectorAll(".markdown-preview").forEach((div) => {
        const markdown = div.getAttribute("data-markdown");
        div.innerHTML = marked.parse(markdown);
    });
});

function updatePreview() {
    const entryText = document.getElementById("entry").value;
    document.getElementById("markdownPreview").innerHTML = marked.parse(entryText);
}