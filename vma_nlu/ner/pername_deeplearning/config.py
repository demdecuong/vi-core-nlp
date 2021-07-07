
class Config(object):
    def __init__(self) -> None:
        super().__init__()

        self.model_name_or_path = 'vinai/phobert-base'
        self.pos_tag_set_path = None
        # self.label_set_path = label_set_path
        # self.char_vocab_path = char_vocab_path
        # self.checkpoint = checkpoint

        self.use_pretrained = False

        # optional features
        self.use_pos = False
        self.use_char = True
        self.use_fasttext = False

        # Tuning Hyperparameters
        self.num_layer_bert = 4
        self.char_hidden_dim = 128
        self.char_embedding_dim = 100
        self.feature_embed_dim = 128
        self.hidden_dim = 728
        self.hidden_dim_ffw = 300
        self.char_vocab_size = 108
        self.pos_vocab_size = 23
        
        self.max_char_len = 20
        self.max_seq_len = 100

        self.num_labels = 2