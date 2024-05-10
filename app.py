import gradio as gr
from dotenv import load_dotenv

from models import get_all_models, get_random_models

load_dotenv()


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


def handle_message(
    llms, user_input, temperature, top_p, max_output_tokens, states1, states2
):
    history1 = states1.value if states1 else []
    history2 = states2.value if states2 else []
    states = [states1, states2]
    history = [history1, history2]
    for hist in history:
        hist.append((user_input, None))
    for (
        updated_history1,
        updated_history2,
        updated_states1,
        updated_states2,
    ) in process_responses(
        llms, temperature, top_p, max_output_tokens, history, states
    ):
        yield updated_history1, updated_history2, updated_states1, updated_states2


def regenerate_message(llms, temperature, top_p, max_output_tokens, states1, states2):
    history1 = states1.value if states1 else []
    history2 = states2.value if states2 else []
    user_input = (
        history1.pop()[0] if history1 else None
    )  # Assumes regeneration is needed so there is at least one input
    if history2:
        history2.pop()
    states = [states1, states2]
    history = [history1, history2]
    for hist in history:
        hist.append((user_input, None))
    for (
        updated_history1,
        updated_history2,
        updated_states1,
        updated_states2,
    ) in process_responses(
        llms, temperature, top_p, max_output_tokens, history, states
    ):
        yield updated_history1, updated_history2, updated_states1, updated_states2


def process_responses(llms, temperature, top_p, max_output_tokens, history, states):
    generators = [
        llms[i]["model"](history[i], temperature, top_p, max_output_tokens)
        for i in range(2)
    ]
    responses = [[], []]
    done = [False, False]

    while not all(done):
        for i in range(2):
            if not done[i]:
                try:
                    response = next(generators[i])
                    if response:
                        responses[i].append(response)
                        history[i][-1] = (history[i][-1][0], "".join(responses[i]))
                        states[i] = gr.State(history[i])
                    yield history[0], history[1], states[0], states[1]
                except StopIteration:
                    done[i] = True
    yield history[0], history[1], states[0], states[1]


with gr.Blocks(
    title="Chatbot Arena",
    theme=gr.themes.Soft(secondary_hue=gr.themes.colors.sky),
) as demo:
    num_sides = 2
    states = [gr.State() for _ in range(num_sides)]
    chatbots = [None] * num_sides
    models = gr.State(get_random_models)
    all_models = get_all_models()
    gr.Markdown(
        "# Chatbot Arena\n\nChat with multiple models at the same time and compare their responses. "
    )
    with gr.Group(elem_id="share-region-annoy"):
        with gr.Accordion(f"🔍 Expand to see the {len(all_models)} models", open=False):
            model_description_md = """| | | |\n| ---- | ---- | ---- |\n"""
            count = 0
            for model in all_models:
                if count % 3 == 0:
                    model_description_md += "|"
                model_description_md += f" {model['name']} |"
                if count % 3 == 2:
                    model_description_md += "\n"
                count += 1
            gr.Markdown(model_description_md, elem_id="model_description_markdown")
        with gr.Row():
            for i in range(num_sides):
                label = models.value[i]["name"]
                with gr.Column():
                    chatbots[i] = gr.Chatbot(
                        label=label,
                        elem_id=f"chatbot",
                        height=550,
                        show_copy_button=True,
                    )

    with gr.Row():
        textbox = gr.Textbox(
            show_label=False,
            placeholder="Enter your query and press ENTER",
            elem_id="input_box",
            scale=4,
        )
        send_btn = gr.Button(value="Send", variant="primary", scale=0)

    with gr.Row() as button_row:
        clear_btn = gr.ClearButton(
            value="🎲 New Round",
            elem_id="clear_btn",
            interactive=False,
            components=chatbots + states,
        )
        regenerate_btn = gr.Button(
            value="🔄 Regenerate", interactive=False, elem_id="regenerate_btn"
        )
        share_btn = gr.Button(value="📷 Share Image")

    with gr.Row():
        examples = gr.Examples(
            [
                "Can you tell me about the weather?",
                "What is the capital of France?",
                "What is the meaning of life?",
            ],
            inputs=[textbox],
            label="Example inputs",
        )

    with gr.Accordion("Parameters", open=False) as parameter_row:
        temperature = gr.Slider(
            minimum=0.0,
            maximum=2.0,
            value=0.0,
            step=0.1,
            interactive=True,
            label="Temperature",
        )
        top_p = gr.Slider(
            minimum=0.0,
            maximum=1.0,
            value=1.0,
            step=0.1,
            interactive=True,
            label="Top P",
        )
        max_output_tokens = gr.Slider(
            minimum=16,
            maximum=4096,
            value=1024,
            step=64,
            interactive=True,
            label="Max output tokens",
        )

    textbox.submit(
        handle_message,
        inputs=[
            models,
            textbox,
            temperature,
            top_p,
            max_output_tokens,
            states[0],
            states[1],
        ],
        outputs=[chatbots[0], chatbots[1], states[0], states[1]],
    ).then(
        activate_chat_buttons,
        inputs=[],
        outputs=[regenerate_btn, clear_btn],
    )

    send_btn.click(
        handle_message,
        inputs=[
            models,
            textbox,
            temperature,
            top_p,
            max_output_tokens,
            states[0],
            states[1],
        ],
        outputs=[chatbots[0], chatbots[1], states[0], states[1]],
    ).then(
        activate_chat_buttons,
        inputs=[],
        outputs=[regenerate_btn, clear_btn],
    )

    regenerate_btn.click(
        regenerate_message,
        inputs=[
            models,
            temperature,
            top_p,
            max_output_tokens,
            states[0],
            states[1],
        ],
        outputs=[chatbots[0], chatbots[1], states[0], states[1]],
    )

    clear_btn.click(
        deactivate_chat_buttons,
        inputs=[],
        outputs=[regenerate_btn, clear_btn],
    ).then(lambda: get_random_models(), inputs=None, outputs=[models])

    share_btn.click(None, inputs=[], outputs=[], js=share_js)

if __name__ == "__main__":
    demo.queue(default_concurrency_limit=10)
    demo.launch()
