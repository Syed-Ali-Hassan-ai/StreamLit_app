import wget
def bar_custom (current, total, width=80):
    percentage = current * 100 / total
    arrow = '-' * int(percentage / 2) + '>' + '-' * (width - int(percentage / 2) - 1)
    print(f'\r{arrow}', end='')
    if current == total:
        print()

model_url = "https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q8_0.gguf"
wget.download(model_url, bar=bar_custom)