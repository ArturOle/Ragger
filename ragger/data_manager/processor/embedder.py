import torch
import spacy
from transformers import AutoModel, AutoTokenizer


@spacy.language.Language.component("RaggerDefaultEmbedder")
def RaggerDefaultEmbedder(doc):
    return Embedder(doc)


class Embedder:
    def __init__(self, model_id="intfloat/e5-base-v2"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModel.from_pretrained(model_id).to(self.device)
        self.model.eval()

    def embed(self, text):
        with torch.no_grad():
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True
            ).to(self.device)
            outputs = self.model(**inputs)
            squeezed_output = outputs.last_hidden_state.mean(dim=1).squeeze()
            return squeezed_output.cpu().numpy()

    def __call__(self, doc):
        doc._.embedding = self.embed(doc.text)
        return doc

    def __name__(self):
        return "RaggerDefaultEmbedder"


if __name__ == "__main__":
    embedder = Embedder()
    text = "This is a test sentence."
    print(embedder.embed(text))
