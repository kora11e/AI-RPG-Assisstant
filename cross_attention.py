import torch.nn as nn
import torch

class CrossAttention(nn.Module):
    def __init__(self, d_in, d_out_kq, d_out_v):
        super().__init__()
        self.d_out_kq=d_out_kq
        self.W_query=nn.Parameter(torch.rand(d_in, d_out_kq))
        self.W_key  = nn.Parameter(torch.rand(d_in, d_out_kq))
        self.W_value=nn.Parameter(torch.rand(d_in, d_out_v))
    
    def forward(self, x_1, x_2):
        queries_1=x_1.matmul(self.W_query)
        keys_2=x_2.matmul(self.W_key)
        values_2=x_2.matmul(self.W_value)
        
        attn_scores=queries_1.matmul(keys_2.T)
        attn_weights=torch.softmax(
            attn_scores/self.d_out_kq**0.5, dim=-1
        )
        
        context_vec=attn_weights.matmul(values_2)
        return context_vec

torch.manual_seed(123)

d_in, d_out_kq, d_out_v = 16,2,4

crossattn=CrossAttention(d_in, d_out_kq, d_out_v)
