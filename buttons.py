import gradio as gr

share_js = """
function () {
    const captureElement = document.querySelector('#share-region-annoy');
    // console.log(captureElement);
    html2canvas(captureElement)
        .then(canvas => {
            canvas.style.display = 'none'
            document.body.appendChild(canvas)
            return canvas
        })
        .then(canvas => {
            const image = canvas.toDataURL('image/png')
            const a = document.createElement('a')
            a.setAttribute('download', 'guardrails-arena.png')
            a.setAttribute('href', image)
            a.click()
            canvas.remove()
        });
    return [];
}
"""


def activate_chat_buttons():
    regenerate_btn = gr.Button(
        value="🔄  Regenerate", interactive=True, elem_id="regenerate_btn"
    )
    clear_btn = gr.ClearButton(
        elem_id="clear_btn",
        interactive=True,
    )
    return regenerate_btn, clear_btn


def deactivate_chat_buttons():
    regenerate_btn = gr.Button(
        value="🔄  Regenerate", interactive=False, elem_id="regenerate_btn"
    )
    clear_btn = gr.ClearButton(
        elem_id="clear_btn",
        interactive=False,
    )
    return regenerate_btn, clear_btn
