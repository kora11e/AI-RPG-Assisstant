import torch
import torch.nn as nn
from torch.autograd import Variable

class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size, n_layers=1):
        super(RNN, self).__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        self.n_layers = n_layers
        
        self.encoder = nn.Embedding(input_size, hidden_size)
        self.gru = nn.GRU(hidden_size*2, hidden_size, n_layers,batch_first=True,
                          bidirectional=False)
        self.decoder = nn.Linear(hidden_size, output_size)
    
    def forward(self, input, hidden):
        input = self.encoder(input.view(1, -1))
        output, hidden = self.gru(input.view(1, 1, -1), hidden)
        output = self.decoder(output.view(1, -1))
        return output, hidden

    def init_hidden(self):
        return Variable(torch.zeros(self.n_layers, 1, self.hidden_size))

hidden_size = 100
n_layers = 1

# vocabulary definition. Check attention.ipynb for more details
def define_words_ix(path:str) -> dict[str, int]:
    with open (path, 'r', encoding='utf-8') as f:
        text = f.read()

    len(text.split())

    test_sentence = text.split()

    trigrams = [([test_sentence[i], test_sentence[i + 1]], test_sentence[i + 2])
                for i in range(len(test_sentence) - 2)]
    chunk_len=len(trigrams)

    vocab = set(test_sentence)
    voc_len=len(vocab)
    word_to_ix = {word: i for i, word in enumerate(vocab)}
    return word_to_ix, voc_len

word_to_ix, voc_len = define_words_ix('./data/text_data/other/csv/text_1.txt')

# don't load optimizer, we don't awnt to continue traiingg process
checkpoint = torch.load('./Image_GAN/model_architecture/checkpoint.pth')
decoder = RNN(voc_len, hidden_size, voc_len, n_layers)
decoder.load_state_dict(checkpoint['model_state_dict'])
decoder.eval()
# decoder_optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
epoch = checkpoint['epoch']
loss = checkpoint['loss']

# function to b e used as a final output
def evaluate(prime_str:str, predict_len:int=100, temperature:float=0.8) -> str:
    hidden = decoder.init_hidden()

    for p in range(predict_len):
        
        prime_input = torch.tensor([word_to_ix[w] for w in prime_str.split()], dtype=torch.long)
        inp = prime_input[-2:] #last two words as input
        output, hidden = decoder(inp, hidden)
        
        # Sample from the network as a multinomial distribution
        output_dist = output.data.view(-1).div(temperature).exp()
        top_i = torch.multinomial(output_dist, 1)[0]
        
        # Add predicted word to string and use as next input
        predicted_word = list(word_to_ix.keys())[list(word_to_ix.values()).index(top_i)]
        prime_str += " " + predicted_word

    return prime_str

#for testing only
#print(evaluate('nie lakier'))
