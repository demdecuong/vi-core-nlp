import os
import gdown
import torch
from vma_nlu.ner.pername_deeplearning import MODEL_DIR, BASE_URL, CHECKPOINT, CHAR_VOCAB, LABEL_SET

def get_mask(max_seq_len, seq_len):
    mask = [[1]*seq_len[i]+[0]*(max_seq_len-seq_len[i]) for i in range(len(seq_len))]
    mask = torch.tensor(mask)
    mask = mask.unsqueeze(1).expand(-1, mask.shape[-1], -1)
    mask = torch.triu(mask)
    return mask

def get_useful_ones(out, label, mask):
    # get mask, mask the padding and down triangle

    mask = mask.reshape(-1)
    tmp_out = out.reshape(-1, out.shape[-1])
    tmp_label = label.reshape(-1)
    # index select, for gpu speed
    indices = mask.nonzero(as_tuple=False).squeeze(-1).long()
    tmp_out = tmp_out.index_select(0, indices)
    tmp_label = tmp_label.index_select(0, indices)

    return tmp_out, tmp_label

def load_model(path):
    checkpoint = torch.load(path, map_location=torch.device('cpu'))
    model = checkpoint['model']
    model.load_state_dict(checkpoint['state_dict'])
    return model

def initializeFolder():
	if not os.path.exists(MODEL_DIR):
		os.mkdir(MODEL_DIR)
		print("Directory ", MODEL_DIR," created")

def download_model():
    checkpoint = MODEL_DIR + CHECKPOINT
    label_set_path = MODEL_DIR + LABEL_SET
    char_vocab_path = MODEL_DIR + CHAR_VOCAB

    if os.path.isfile(checkpoint) != True:
        print(f"{CHECKPOINT} will be downloaded...")
        gdown.download(BASE_URL + CHECKPOINT, checkpoint, quiet=False)

    if os.path.isfile(label_set_path) != True:
        print(f"{LABEL_SET} will be downloaded...")
        gdown.download(BASE_URL + LABEL_SET, label_set_path, quiet=False)

    if os.path.isfile(char_vocab_path) != True:
        print(f"{CHAR_VOCAB} will be downloaded...")
        gdown.download(BASE_URL + CHAR_VOCAB, char_vocab_path, quiet=False)

    return checkpoint, label_set_path, char_vocab_path
