
class Config(object):
    def __init__(self) -> None:
        super().__init__()

        self.model_name_or_path = 'vinai/phobert-base'
        self.pos_tag_set_path = None
        self.label_set_path = './vma_nlu/data/label_set.txt'
        self.char_vocab_path = './vma_nlu/data/charindex.json'
        self.fasttext_path = './data/cc.vi.300.bin'
        self.save_folder = 'save_checkpoint'
        self.checkpoint = './checkpoint.pth'

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
        self.max_seq_len = 160

        self.num_labels = 2

        
        # train
        self.iteration = 1
        self.batch_size = 64
        self.num_epochs = 10
        self.learning_rate = 5e-5
        self.adam_epsilon = 1e-8
        self.weight_decay = 0.01
        self.warmup_steps = 0
        self.max_grad_norm = 1

        # data
        self.train_data = './data/train.json'
        self.dev_data = './data/test.json'
        self.test_data = './data/test.json'

        #
        self.do_train = True
        self.do_eval = True

